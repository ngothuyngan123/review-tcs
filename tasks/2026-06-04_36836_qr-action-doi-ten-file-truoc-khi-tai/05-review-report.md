# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | `#36836 — [QR Landing] Đổi tên file / chỉ định nơi lưu trước khi tải QR (QRコードアクション)` |
| Reviewer (Leader) | `<Leader điền>` |
| Tester được review | `<member điền>` (sheet cột Assignee trống) |
| Ngày review | `2026-06-04` |
| Version TCs | `v1` (fetch từ Redmine Link TCs qua /new-task) |
| Vòng review | `Round 1` |

> Spec reference: dùng `templates/LME-SYSTEM-SPEC.md` tổng — **không có** `02-spec-reference.md` riêng cho task này.
> Nguồn file 04: `/new-task` fetch từ tab "Improve 2026/05/13" (gid 412698763), range A241:J260. Layout sheet **không chuẩn 10 cột** → mapping cột đã ghi trong header file 04.

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — Có issue BLOCKER/MAJOR, cần fix và review lại

**Lý do ngắn gọn**: Bộ TC cover tốt happy-path đa trình duyệt, NHƯNG (1) **bỏ lọt hoàn toàn nhánh "Hủy"** (AbortError / hủy prompt) — một behavior được code rõ trong cách fix; (2) **expected của 6 TC Firefox (TC013–018) mâu thuẫn cách fix** (mô tả "Save As + chọn thư mục" trong khi Firefox dùng fallback `window.prompt` chỉ đổi tên). Cả hai đều có nguy cơ bỏ lọt bug hoặc verify nhầm.

---

## 2. Tóm tắt cho member

Bộ TC làm tốt phần **ma trận đa trình duyệt** (Chrome/Edge/Firefox/Mac) và đã nghĩ tới double-click, tên file ký tự đặc biệt/JP, tải lặp — rất đáng khen. Tuy nhiên còn 2 lỗ hổng nghiêm trọng cần sửa trước khi chạy: **(a)** chưa có TC nào test **bấm Hủy** ở hộp thoại Save As / prompt (cách fix có xử lý nhánh này), và **(b)** expected của nhóm **Firefox** đang bê nguyên văn bản "Save As + chọn thư mục" của Chrome — sai, vì Firefox đi nhánh fallback `window.prompt` chỉ cho đổi tên, không chọn được thư mục. Ngoài ra cần verify 2 file auto-fill (tick checkbox), bổ sung TC cho **AJAX lỗi sau khi mở picker**, và tách regression theo từng màn dùng chung endpoint.

---

## 3. Coverage Matrix

> File 04 không có cột "Map to Impact" → mapping dưới đây **suy luận** từ Title / Precondition / Steps / Expected.

| Impact | Loại | Priority | TCs map | # TC | Status |
|---|---|---|---|---|---|
| BUG — Save As (đổi tên + chọn nơi lưu) trước khi tải | Fix | — | TC001, TC007, TC013 (+ các TC rename: 006/012/018) | 6 | **RISK** — thiếu nhánh Cancel; expected Firefox sai |
| F1 — `downloadQr()` (`public/js/layout_v2_header.js`) | Function | Direct | TC001–TC019 (toàn bộ exercise nút tải) | 19 | **RISK** — nhánh Cancel (AbortError/hủy prompt) + AJAX-fail chưa cover |
| (Data) — không có | Data | — | N/A | — | N/A (Dev: "k có") |
| T1 — Tải QR thêm bạn từ popup QRコード header v2 | Feature | Medium | TC001–TC019 | 19 | **OK** — happy path đa browser đầy đủ |
| T2 — màn dùng chung endpoint `/ajax/download-file-chat11` (qr_code v2, chat-v2, setting add friend) | Feature | Low | TC004, TC010, TC016 | 3 | **RISK** — generic "các màn", không nêu tên 3 màn, chỉ happy-path (AP-3) |

### ORPHAN TCs

| TC ID | Title | Lý do orphan | Hành động đề xuất |
|---|---|---|---|
| TC006, TC012 | [Chrome/Edge] đổi tên + chọn nơi lưu (setting OFF) | Với nhánh `showSaveFilePicker`, browser setting "Ask where to save" KHÔNG ảnh hưởng (picker luôn hiện) → expected giống hệt TC001/007 → có thể **redundant** | Xác nhận ý nghĩa ON/OFF; nếu không khác → gộp hoặc giữ 1 làm smoke |

(Không có TC lạc chủ đề ngoài scope — toàn bộ map về F1/T1/T2.)

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| Fix shape (đọc mục 2 dev-impact) | **Conditional fallback theo browser-capability** (feature-detection branch) + **cancel handling**. Không phải generic catch-all error, nhưng nhiều nhánh bắt buộc cover. |
| Trigger space cần cover | **(A)** Browser hỗ trợ File System Access API → Save As [Chrome, Edge]; **(B)** Browser KHÔNG hỗ trợ → fallback `window.prompt` + blob URL [Firefox, Safari]; **(C)** Hủy picker Save As (AbortError) → dừng; **(D)** Hủy `window.prompt` → dừng; **(E)** AJAX `/ajax/download-file-chat11` fail/timeout SAU khi picker đã mở (picker mở trước AJAX). |
| Số trigger TCs hiện cover | **~1.5 / 5** — (A) ✓ Chrome/Edge; (B) có TC nhưng **expected SAI** (mô tả Save As thay vì prompt); (C) ✗; (D) ✗; (E) ✗ |
| KH report dạng | **Có root cause cụ thể** (SpecImprove, không phải symptom-only) → AP-2 N/A |
| Alternative root causes cần verify | N/A |
| Anti-patterns dính | **AP-3** (regression generic happy-path: TC004/010/016), **AP-4** (PR link trống → không verify được fix shape thực tế) |

> Trigger space cover < tổng → flag **[BLOCKER] FIX-SHAPE** ở §4.1.

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- **[BLOCKER] FIX-SHAPE / GAP-1 — nhánh "Hủy" chưa cover**: Mục 2 ghi rõ *"Bấm Hủy ở hộp thoại (AbortError) hoặc hủy ở prompt → dừng, không tải"* — đây là behavior được code, nhưng **không TC nào** trong 19 TC verify. Rủi ro: hủy không dừng được / file vẫn tải / JS lỗi không nuốt AbortError. → Thêm ≥ 2 TC (Cancel Save As cho Chrome/Edge; Cancel prompt cho Firefox/Safari) — xem TC-NEW-01, TC-NEW-02.
- **[BLOCKER] FIX-SHAPE — TC013–TC018 (Firefox) expected mâu thuẫn cách fix**: Steps + Expected mô tả *"hộp thoại Save As của trình duyệt"* và *"chọn thư mục khác Download mặc định"*. Nhưng theo mục 2, Firefox **không hỗ trợ** File System Access API → đi nhánh fallback `window.prompt` (chỉ **đổi tên**, **KHÔNG** chọn được thư mục), tải qua blob URL. Expected hiện tại sai → tester sẽ verify nhầm (đánh pass cho behavior sai, hoặc fail cho behavior đúng). TC019 (Mac) mô tả ĐÚNG nhánh này — dùng làm chuẩn để sửa TC013–018. → Sửa Steps/Expected của nhóm Firefox theo nhánh prompt (xem TC-NEW-03).

### 4.2 Major (nên fix)

- **[MAJOR] SYMPTOM/AUTO-FILL — 01 chưa verify**: `01-bug-task.md` auto-filled `2026-06-04 by /new-task` nhưng checkbox **"Tester verify auto-fill chính xác" CHƯA tick**. Yêu cầu tester đọc lại Redmine #36836 (description + journal) và tick trước khi review có giá trị.
- **[MAJOR] AUTO-FILL — 03 chưa verify**: `03-dev-impact.md` auto-filled nhưng checkbox CHƯA tick → F/D/T có thể thiếu/mapping sai. Đặc biệt: mức risk T1 (Medium) là **suy luận của /new-task**, Dev không ghi → tester confirm lại với Dev.
- **[MAJOR] FIX-SHAPE — AJAX fail sau khi mở picker (trigger E)**: Picker được mở **trước** khi gọi AJAX `/ajax/download-file-chat11`. Không có TC cho case AJAX lỗi/timeout/500 **sau khi** user đã chọn/đặt tên file. Rủi ro: tạo file 0 byte / file hỏng / treo không báo lỗi. → Thêm TC-NEW-04.
- **[MAJOR] [AP-3] Regression generic — TC004/010/016**: "Truy cập được các màn => thực hiện chức năng tải file" không nêu tên **3 màn cụ thể** từ mục 3 (qr_code v2, chat-v2, setting add friend) và chỉ test clean state. → Tách regression theo từng màn + thêm edge state (data lớn/empty). Xem TC-NEW-05.
- **[MAJOR] [AP-4] PR link trống**: Mục "Commit / Pull Request" = `<chưa có>` → **không verify được fix shape thực tế** (cancel handling, folder-choose ở fallback có thật không, xử lý AJAX-fail). Yêu cầu Dev cung cấp PR link.
- **[MAJOR] TC019 thiếu Steps**: Sheet để trống cột Steps cho TC019 (Mac cross-browser) → không reproducible. → Viết steps rõ cho từng browser (Chrome/Edge: Save As; Firefox/Safari: prompt) trên macOS.

### 4.3 Minor (có thể fix sau)

- **[MINOR] Type/Priority trống toàn bộ 19 TC**: sheet nguồn không có 2 cột này. → Member điền (gợi ý: rename/save = Positive; double-click/special-char = Boundary; "các màn khác" = Regression; cancel/AJAX-fail = Negative).
- **[MINOR] Trùng lặp cross-browser**: 6 case × 3 browser → chấp nhận cho test matrix, nhưng nên đánh Priority để biết case nào bắt buộc full-matrix vs case nào chỉ cần 1 browser (vd special-char filename không cần lặp 3 lần).
- **[MINOR] TC ID/Title do /new-task sinh** (sheet gốc không có cột TC ID; Title suy từ Browser + Steps) → member confirm naming theo chuẩn team.

### 4.4 Nit (gợi ý)

- **[NIT] Secure-context / iframe**: `window.showSaveFilePicker` yêu cầu HTTPS + không bị chặn trong iframe sandbox. Nếu popup QRコード render trong iframe → có thể fail. Thêm 1 smoke check.
- **[NIT] Ghi đè file trùng tên**: Chọn lại đúng tên file đã tồn tại ở Save As → verify dialog confirm overwrite của OS hoạt động, file ghi đè đúng.

---

## 5. TCs đề xuất bổ sung

> Member copy vào `04-tc-list.md` ở round tiếp theo.

| TC ID gợi ý | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| TC-NEW-01 | [Chrome/Edge] Hủy hộp thoại Save As → không tải | Browser Chrome/Edge; popup QRコード mở | 1. Mở popup QRコード trên header.<br>2. Bấm nút tải QR.<br>3. Ở hộp thoại Save As bấm **Cancel/Esc**. | Không tải file nào về máy.<br>Không lỗi JS (AbortError được nuốt êm).<br>Bấm tải lại lần nữa → picker mở bình thường, tải được. | High | Negative | BUG, F1 (nhánh Cancel mục 2) |
| TC-NEW-02 | [Firefox/Safari] Hủy prompt đổi tên → không tải | Browser Firefox/Safari | 1. Mở popup QRコード → bấm tải QR.<br>2. Ở `window.prompt` đổi tên bấm **Cancel**. | Không tải file.<br>Không lỗi JS.<br>Tải lại được bình thường. | High | Negative | BUG, F1 (fallback cancel) |
| TC-NEW-03 | [Firefox/Safari] Fallback prompt — đổi tên rồi tải (sửa expected sai của TC013–018) | Browser Firefox/Safari | 1. Mở popup QRコード → bấm tải.<br>2. **`window.prompt` hiện** (KHÔNG phải Save As) → nhập tên qr-vip.png → OK. | Hiện **prompt đổi tên**, không phải hộp thoại Save As native.<br>File tải về thư mục Download mặc định (hoặc theo setting trình duyệt) với tên đã nhập.<br>**KHÔNG** có bước chọn thư mục.<br>Mở file → đúng ảnh QR. | High | Positive | BUG, F1 (fallback branch B) |
| TC-NEW-04 | [Chrome] AJAX download-file-chat11 lỗi/timeout sau khi confirm Save As | Browser Chrome; chặn/mock endpoint trả 500 hoặc ngắt mạng sau khi mở picker | 1. Mở popup QRコード → bấm tải.<br>2. Ở Save As chọn file + Lưu.<br>3. (AJAX `/ajax/download-file-chat11` fail). | Hiển thị **báo lỗi rõ ràng** cho user.<br>KHÔNG tạo file 0 byte / file hỏng tại nơi đã chọn (hoặc nếu đã tạo → có cleanup/thông báo).<br>User thử lại được. | High | Negative | F1, BUG (async ordering picker-before-AJAX) |
| TC-NEW-05 | [Regression] Tải file ở từng màn dùng chung endpoint | Lần lượt: qr_code v2 / chat-v2 / setting add friend (mỗi màn 1 TC) | 1. Vào từng màn.<br>2. Thực hiện chức năng tải file của màn đó (cả trạng thái thường + data lớn/empty). | Mỗi màn tải file **bình thường như trước fix** (dùng hàm tải riêng, không bị `downloadQr()` mới ảnh hưởng).<br>Không lỗi JS. | Medium | Regression | T2 |

---

## 6. Spec update needed

- [ ] Không cần update spec
- [x] **Cần update spec** — chi tiết:
  - **Section**: QR code action (QRコードアクション) — luồng tải QR từ popup QRコード header v2.
  - **Nội dung cần update**: Ghi rõ behavior mới + **khác biệt giữa 2 nhánh trình duyệt**:
    - Chrome/Edge (hỗ trợ File System Access API): hiện **Save As** → đổi tên + chọn nơi lưu.
    - Firefox/Safari (không hỗ trợ): fallback **`window.prompt`** → chỉ đổi tên, tải về thư mục mặc định (KHÔNG chọn được nơi lưu).
    - Nhánh **Hủy** (AbortError / hủy prompt) → dừng, không tải.
    - Làm rõ tương tác với setting trình duyệt "Ask where to save each file before downloading" (ON/OFF) trên từng nhánh.
  - **Người chịu trách nhiệm update**: PM/Dev (đây là SpecImprove #36836).

---

## 7. Checklist đã chạy

- [x] A. Coverage — A.1 BUG (RISK), A.2 F1 (RISK), A.3 Data (N/A), A.4 Feature (T1 OK / T2 RISK), A.5 gap/orphan, **A.6 fix-shape (fail — 2 BLOCKER)**
- [x] B. Chất lượng từng TC — TC019 thiếu steps; regression generic
- [x] C. Chất lượng bộ TC tổng thể — lệch về Positive, thiếu Negative (cancel/AJAX-fail); trùng lặp cross-browser
- [x] D. Spec alignment — không có 02-spec-reference; cần update spec (xem §6)
- [x] E. Hành chính — TC ID/Title sinh tự động; Assignee/Status/version trống (chờ member)
- [x] F. Base checklist LME
  - [x] F.1 Checklist web — **CL5 double-click** ✓ (TC002/008/014); **CL6 data input ký tự đặc biệt/JP** ✓ (TC003/009/015); CL16 (file rác) **N/A** (download client-side, không tạo file server); CL13 (line friend QR) **N/A** (đây là admin tải QR, không phải line user access); CL22 (upload path) N/A. **A.2 Compatibility** ✓ Win (Chrome/Edge/Firefox) + Mac (TC019).
  - [x] F.2 Checklist job — **N/A** (không chạm job)
  - [x] F.3 Các tính năng chung — **N/A** (không chạm C.1–C.8; QR action chỉ tải ảnh, không send message/bill/friend-info)

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | | |
| Tester | (đã đọc & hiểu feedback) | |
