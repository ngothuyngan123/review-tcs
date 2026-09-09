# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | `#36203 — [01-05-2026][Khác] Panel/Button — 2 yêu cầu fix UX (panel right-side menu bị che; delete cần modal confirm)` |
| Reviewer (Leader) | `<Leader verify>` |
| Tester được review | `<chưa điền trong file 04>` |
| Ngày review | `2026-06-02` |
| Version TCs | `<chưa điền trong file 04>` |
| Vòng review | `Round 1` |

> **Spec reference**: dùng `templates/LME-SYSTEM-SPEC.md` tổng (Template/Panel-Button), **không có** `02-spec-reference.md` riêng cho task này.

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — Có nhiều issue MAJOR cần fix và review lại Round 2.

**Lý do ngắn gọn**: Coverage cơ học cho **2 fix chính** (① menu panel right-side, ② modal confirm xóa) **khá tốt** — có TC reproduce đúng cả 2. NHƯNG: (a) cả `01` + `03` auto-fill từ Redmine **chưa được tester verify** (checkbox chưa tick); (b) mục 1 (nguyên nhân) + mục 3 (caller đã check) trong dev-impact **trống** trong khi fix ② "lấy modal theo component" (dùng chung) → **chưa có TC regression** cho các nơi khác xài chung modal đó; (c) fix ① là **CSS layout** nhưng **thiếu test đa trình duyệt/responsive** — đúng chiều dễ tái phát nhất.

---

## 2. Tóm tắt cho member

Bộ TCs bám sát 2 yêu cầu UX rất tốt: bạn đã reproduce đúng case menu panel bên phải (5–10 panel × 3 loại button) và cover khá đủ luồng modal xóa (confirm/cancel × panel có/không thông tin × xóa liên tục) — đây là phần lõi, làm tốt. 3 điểm cần bổ sung trước khi pass: (1) tester đọc lại Redmine và **tick 2 checkbox verify** ở `01` + `03`; (2) thêm TC **regression cho component modal dùng chung** (fix ② "lấy modal theo component" có thể ảnh hưởng các màn khác cùng xài modal đó — hỏi Dev list ra) và **test đa trình duyệt/độ rộng màn hình** cho fix CSS ①; (3) bỏ/đánh dấu 2 TC Quick Reply (TC040–041) vì lạc scope. Lưu ý 26/41 TC đang `Not test` (color + image) — cần chạy thật vì fix CSS/JS có thể khác nhau giữa các loại button.

---

## 3. Coverage Matrix

> Suy luận map (file 04 không có cột Map to Impact). Nhóm TC: **standard** = TC001–013 (đã test OK), **color** = TC014–026 (Not test), **image** = TC027–039 (Not test), **Quick Reply** = TC040–041 (Not test, orphan).

| Impact | Loại | Priority | TCs map (suy luận) | # TC | Status |
|---|---|---|---|---|---|
| BUG① — menu panel right-side hiển thị không cần dịch panel | Fix | — | TC001–006, TC014–019, TC027–032 | 18 | **RISK** — đủ chiều chức năng nhưng thiếu test responsive/đa trình duyệt (chiều cốt lõi của fix CSS) |
| BUG② — modal confirm trước khi xóa panel | Fix | — | TC008–013, TC021–026, TC034–039 | 18 | **RISK** — đủ confirm/cancel/liên tục nhưng thiếu regression component modal dùng chung |
| F1 — `public/css/template_v2/create.css` (CSS panel right-side menu) | Function | Direct | TC001–006, TC014–019, TC027–032 | 18 | **RISK** — thiếu Compatibility (Win/Mac, Safari) + responsive width |
| F2 — `public/js/template_v2/messages/button.js` (hàm confirm xóa + JS panel) | Function | Direct | TC008–013, TC021–026, TC034–039 | 18 | **RISK** — thiếu double-click trên nút 削除する + regression hàm dùng chung |
| F3 — `resources/views/basic/template_v2/components/button.blade.php` (markup modal/panel) | Function | Direct | TC008–013, TC021–026, TC034–039 (verify "modal hiển thị giống ở component") | 18 | **RISK** — component modal dùng chung: chưa test nơi khác có bị ảnh hưởng |
| D1 — `<không có data>` | Data | — | — | — | **N/A** — Dev xác nhận fix không chạm data layer |
| T1 — Màn add/edit template button | Feature | Medium | Toàn bộ TC001–039 (thao tác trong màn) + TC007/020/033 (send template cho user — regression) | 39 | **RISK** — chỉ nhóm standard `OK`; color + image `Not test`; thiếu regression edge-state (reload, chuyển tab, double-click) |

### ORPHAN TCs

| TC ID | Title | Lý do orphan | Hành động đề xuất |
|---|---|---|---|
| TC040 | Check tạo template Quick Reply (Dạng ảnh) | Quick Reply không thuộc scope fix Panel/Button (#36203) — nằm cuối range 1575-1617 nhưng khác feature | Map lại sang task Quick Reply riêng / Remove khỏi scope review này |
| TC041 | Check tạo template Quick Reply (Dạng text) | Như trên (lại còn Expected trống) | Map lại / Remove |

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| Fix shape (đọc mục 2 dev-impact) | **UI/CSS layout fix** (① sửa CSS panel right-side menu) + **Thêm UI component** (② thêm modal confirm xóa, "lấy modal theo component" dùng chung + sửa JS thêm hàm confirm). KHÔNG phải generic-catch / validation / race / migration / payment. |
| Trigger space cần cover | ① Menu right-side: × {loại button: standard/color/image} × {số panel 5,6,7,8,9,10+} × {trình duyệt Win-Chrome, Mac-Safari} × {độ rộng màn hình hẹp/rộng}. ② Modal xóa: × {panel có/không thông tin, xóa liên tục, confirm/cancel} × {double-click nút xóa} × {các màn khác dùng chung component modal}. |
| Số trigger TCs hiện cover | ① **2/4 chiều** (loại button ✔ 3 loại, số panel ✔ 5–10; **trình duyệt ✘, responsive width ✘**). ② **3/5 chiều** (có/không thông tin ✔, liên tục ✔, confirm/cancel ✔; **double-click ✘, regression component dùng chung ✘**). |
| KH report dạng | **Có yêu cầu cụ thể** (feature improvement, không phải symptom-only bug) → KHÔNG cần cover alternative root cause. |
| Alternative root causes cần verify | N/A |
| Anti-patterns dính | **AP-6** (mục 3 dev-impact trống) ; **AP-4** (mục Commit/PR trống → không verify được fix shape thực tế của hàm confirm dùng chung) ; nhẹ **AP-3** (regression T1 chủ yếu happy-path, thiếu edge-state) |

> Vì fix ② tái sử dụng **component modal dùng chung** mà mục 3 (caller đã check) trống + không có PR link → **không thể xác định scope regression** → flag MAJOR §4.2.

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- _Không có BLOCKER._ Cả 2 fix root cause (① menu right-side, ② modal confirm) đều có TC verify trực tiếp đúng flow reproduce → không GAP root cause. (Các rủi ro còn lại ở mức MAJOR bên dưới.)

### 4.2 Major (nên fix)

- `[MAJOR] PROCESS` — `01-bug-task.md` auto-filled `2026-06-02 by /new-task` nhưng checkbox **"Tester verify auto-fill chính xác" CHƯA tick** — review chưa có giá trị cho tới khi tester đọc lại detail Redmine (description + journal "Tái hiện case KH") và tick. **Fix**: tester verify + tick checkbox.
- `[MAJOR] PROCESS` — `03-dev-impact.md` auto-filled `2026-06-02 by /new-task` nhưng checkbox **"Tester verify auto-fill chính xác" CHƯA tick** — F/D/T có thể chưa đầy đủ. **Fix**: tester đọc lại journal đánh giá Dev (2026-05-23) + tick checkbox.
- `[MAJOR] FIX-SHAPE / AP-6` — Mục 3 dev-impact (caller đã check) **trống** + mục 1 (nguyên nhân) **trống**. Fix ② ghi rõ "**lấy modal theo component**" (component dùng chung) → nếu component/hàm confirm này còn được các màn khác gọi, sửa JS có thể gây regression. Hiện **không có TC** cover các nơi khác. **Fix**: yêu cầu Dev (a) điền nguyên nhân CSS cụ thể (overflow/positioning gì?), (b) list nơi dùng chung component modal → thêm regression TC cho từng nơi.
- `[MAJOR] FIX-SHAPE` — Fix ① là **CSS layout** cho menu sát mép phải, nhưng **thiếu test Compatibility/responsive** (checklist-lme A.2: Win+Mac, Chrome+Safari; + độ rộng màn hình hẹp). Đây là chiều dễ tái phát nhất của lỗi clipping. **Fix**: thêm TC test menu right-side trên Mac-Safari + màn hình hẹp (xem TC-NEW-02).
- `[MAJOR] AP-4` — Mục "Commit / Pull Request" = `<chưa có>` → reviewer không verify được hàm confirm xóa là dùng chung component đến mức nào. **Fix**: yêu cầu Dev cung cấp PR link.
- `[MAJOR] EXECUTION` — 26/41 TC (`color` TC014–026 + `image` TC027–039) đang **`Not test`**; chỉ nhóm `standard` được chạy `OK`. Fix CSS/JS có thể khác nhau giữa loại button → coverage trên giấy nhưng chưa được verify. **Fix**: chạy đủ color + image (ít nhất các TC delete-modal + menu right-side).
- `[MAJOR] TC040–041 ORPHAN`: 2 TC Quick Reply lạc scope (#36203 chỉ về Panel/Button). **Fix**: tách sang task Quick Reply hoặc remove khỏi file 04 review này.

### 4.3 Minor (có thể fix sau)

- `[MINOR] CL5`: Chưa có TC **double-click** nút 削除する trong modal confirm (có thể double-fire xóa). Thêm 1 TC.
- `[MINOR] CL2`: Chưa có TC **reload** màn add/edit template sau khi xóa panel → verify state đúng.
- `[MINOR]` File 04 thiếu cột **Type / Priority** (sheet gốc không có) và thiếu **Tester/Version** ở phần "Thông tin" → khó đánh giá tỷ lệ Positive/Negative/Boundary/Regression. Bổ sung khi member chuẩn hóa.
- `[MINOR]` Nhiều TC Precondition rời rạc (ô C/D trống ở dòng confirm/cancel) do giữ nguyên layout sheet gốc — nên gộp Precondition cho rõ context khi chuẩn hóa.

### 4.4 Nit (gợi ý)

- `[NIT] AP-5`: TC007/020/033 (send template cho user) Dev ghi "k ảnh hưởng, k cần check kỹ" → giữ ở mức smoke/regression, đừng đầu tư sâu.
- `[NIT]`: Có thể thêm 1 TC kiểm tra menu right-side khi panel **cuối cùng** (panel ngoài cùng bên phải) thay vì chỉ panel 4/5 — đúng nguyên văn KH "右端にあるパネル".

---

## 5. TCs đề xuất bổ sung

| TC ID gợi ý | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| TC-NEW-01 | Regression component modal dùng chung sau khi thêm confirm xóa panel | Dev đã list các màn dùng chung component modal (hỏi Dev) | 1. Mở từng màn khác có dùng modal confirm cùng component (theo list Dev)<br>2. Thực hiện thao tác mở/đóng modal ở màn đó | Modal ở các màn khác **vẫn hiển thị & hoạt động bình thường**, không bị lỗi layout/JS sau thay đổi | High | Regression | F2, F3, BUG② |
| TC-NEW-02 | Menu panel right-side hiển thị đúng trên đa trình duyệt + màn hình hẹp | Template button có 5 panel, panel ngoài cùng bên phải (右端) | 1. Mở màn add/edit template button trên **Mac-Safari** và **Win-Chrome**<br>2. Thu hẹp cửa sổ trình duyệt (responsive)<br>3. Click/hover icon 3 chấm của panel **ngoài cùng bên phải** | Menu (sort/copy/đổi vị trí/xóa) **hiển thị đầy đủ không bị che**, không cần dịch panel — đồng nhất giữa các trình duyệt và độ rộng | High | Boundary/Compatibility | BUG①, F1 |
| TC-NEW-03 | Double-click nút 削除する trong modal confirm | Panel có thông tin, modal confirm xóa đang mở | 1. Double-click nhanh nút 削除する | Panel chỉ bị xóa **1 lần**, không double-fire / không lỗi JS | Medium | Negative | F2, BUG② |
| TC-NEW-04 | Reload sau khi xóa panel qua modal confirm | Đã xóa 1 panel thành công qua modal | 1. Reload màn add/edit template button | State đúng: panel đã xóa không còn, các panel còn lại + thứ tự đúng, không lỗi | Low | Regression | T1 |
| TC-NEW-05 | Menu right-side khi vượt số panel max (boundary) | Tạo số panel ở mức **max** cho phép của template button | 1. Kéo scroll tới panel ngoài cùng phải<br>2. Click icon 3 chấm | Menu hiển thị đầy đủ; không lỗi layout ở mức max panel | Medium | Boundary | BUG①, F1, T1 |

---

## 6. Spec update needed (nếu có)

- [x] Không cần update spec — đây là cải tiến UX (CSS + modal confirm), không đổi business rule. (Tham chiếu LME-SYSTEM-SPEC tổng, mục Template/Panel-Button.)
- [ ] Cần update spec

---

## 7. Checklist đã chạy

- [x] A. Coverage — thực hiện (suy luận map, ra RISK ở các impact do thiếu chiều regression/compat)
- [x] B. Chất lượng từng TC — Title nhóm hơi generic (theo loại button), Precondition rời rạc (giữ layout sheet gốc)
- [x] C. Chất lượng bộ TC tổng thể — thiếu cột Type/Priority để đánh giá tỷ lệ; thiếu compatibility/multi-device
- [x] D. Spec alignment — không mâu thuẫn
- [x] E. Hành chính — thiếu Tester/Version trong file 04
- [x] F. Base checklist LME
  - [x] F.1 Checklist web — **liên quan**: CL5 (double-click ✘), CL4 (thao tác liên tục — xóa liên tục ✔), CL2 (reload ✘), CL8/copy+sort (đổi vị trí/copy panel ✔), A.2 Compatibility (Win/Mac, responsive ✘ → MAJOR)
  - [x] F.2 Checklist job — **không liên quan** (fix chỉ CSS/JS/Blade, không chạm job/callback/google sync)
  - [x] F.3 Các tính năng chung — **C.8 Sort** liên quan (sort/đổi vị trí panel ✔ covered); C.1–C.7 không liên quan; D1 không có data
- [ ] _Lưu ý_: F.1/A.2 Compatibility & Regression chưa cover → đã flag MAJOR §4.2.

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | | |
| Tester | (đã đọc & hiểu feedback) | |
