# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | `#37396 — [QR Landing] QR code action 「保留：アルコールset*1m」 không hiển thị nút Spreadsheet` |
| Reviewer (Leader) | `<Leader verify>` |
| Tester được review | `<chưa điền trong file 04>` |
| Ngày review | `2026-06-13` |
| Version TCs | `v1` |
| Vòng review | `Round 1` |

> Spec reference: dùng `templates/LME-SYSTEM-SPEC.md` tổng (feature QR Landing) — **không có** `02-spec-reference.md` riêng cho task này.

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — Có issue MAJOR, cần fix và review lại

**Lý do ngắn gọn**: Bộ 18 TC cover **happy path job tạo sheet rất tốt** (nhiều trạng thái landing), nhưng (1) input `01` + `03` auto-fill từ Redmine **chưa được tester verify**; (2) fix là **Google Sheet sync job** mà **không có 1 TC negative nào** cho lỗi Google API / mất quyền / rate-limit (CLJ01 bắt buộc); (3) bug là **symptom-only + không tái hiện được** nhưng mọi TC chỉ giả định 1 root cause (missing `google_sheet_id`); (4) mục 3 dev-impact trống + mục 4.2 mâu thuẫn với cách fix.

---

## 2. Tóm tắt cho member

Bộ TC fetch từ Sheet rất chắc về **chiều rộng trạng thái landing** (tạo mới, đã có trước liên kết, xóa→khôi phục, xóa liên kết→liên kết lại, remote, recover data KH) — đây là điểm mạnh thật sự, gần như phủ hết positive path của job. Tuy nhiên bộ TC **thiếu hẳn chiều negative**: fix này đụng Google API tạo sheet nên **bắt buộc** có TC cho mất quyền / Google API lỗi / rate-limit khi job tạo nhiều sheet cùng lúc (TC003 đã nêu "nhiều landing" nhưng chưa verify retry). Ngoài ra cần tester tick verify auto-fill của file 01/03 và hỏi Dev bổ sung mục 3 + sửa mục 4.2 trước khi review có giá trị final.

---

## 3. Coverage Matrix

> File 04 không có cột "Map to Impact" — mapping dưới đây **suy luận** từ Title/Precondition/Steps/Expected. Source là bảng phân cấp đã convert (xem cảnh báo đầu file 04).

| Impact | Loại | Priority | TCs map (suy luận) | # TC | Status |
|---|---|---|---|---|---|
| BUG — missing `google_sheet_id` → icon Spreadsheet không hiển thị | Fix | — | TC001–TC012, TC015–TC018 (verify "hiển thị icon gg sheet" sau khi job tạo sheet) | 16 | **RISK** — symptom-only; chưa có TC cho case `google_sheet_id` ĐÃ có nhưng sheet bị xóa/mất quyền mà icon vẫn ẩn (alternative root cause) |
| F1 — `createSheetForLanding()` | Function | Direct | TC001–TC012, TC015–TC018 ("Sheet mới được tạo" + "google_sheet_id được cập nhật") | 16 | **RISK** — đủ positive, **thiếu negative**: Google API fail / mất quyền khi tạo sheet |
| F2 — `handle()` (entry job daily) | Function | Direct | TC003, TC004 (ép job chạy ở dev), TC015–TC018 ("sau khi job chạy") | 6 | **RISK** — thiếu rate-limit / retry khi job tạo **nhiều** sheet 1 lần (CLJ01) |
| D-implicit — `landing.google_sheet_id` UPDATE + sheet CREATE + data INSERT | Data | Dev ghi "Không có" (⚠️ SAI) | TC001–TC012, TC015–TC018 ("google_sheet_id được cập nhật", "data sync") | 16 | **RISK** — mục 4.2 dev khai sai; thiếu boundary/negative cho data (insert trùng, data rỗng vs có data) |
| T1 — job ghi data landing hàng ngày (regression) | Feature | Dev chưa ghi mức | TC002/004/006/009/011 ("data sync bình thường"), TC013 (bot không liên kết → không ảnh hưởng), TC014 (account staff) | 7 | **OK** |

### ORPHAN TCs

Không có TC lạc chủ đề rõ rệt — toàn bộ 18 TC map về BUG / F1 / F2 / D / T1 hoặc checklist (TC014 → CL1 staff). Lưu ý TC013/TC014 đóng vai regression/permission, nên giữ.

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| Fix shape (mục 2 dev-impact) | **Data-repair / backfill job** + **Google Sheet sync** (job daily check landing thiếu `google_sheet_id` → tạo sheet + insert data). KHÔNG phải generic catch-all error handler. |
| Trigger space cần cover | (A) Trạng thái landing thiếu `google_sheet_id`: mới tạo / nhiều landing cùng thiếu / đã có trước liên kết / OFF / xóa→khôi phục / remote / xóa liên kết→liên kết lại — **cover tốt**. (B) **Google API failure modes**: mất quyền sau liên kết, quota/rate-limit khi tạo nhiều sheet, sheet bị user xóa thủ công, filename ký tự đặc biệt — **chưa cover**. |
| Số trigger TCs hiện cover | Landing-state: ~12/12 ✅. Google-API-failure: **0/4** ❌ |
| KH report dạng | **Symptom-only** — KH chỉ thấy "nút Spreadsheet không hiển thị", không có error code/message; Dev **không tái hiện được** (journal Kim Cúc). |
| Alternative root causes cần verify | (1) `google_sheet_id` ĐÃ tồn tại nhưng sheet Google bị xóa / mất quyền → icon vẫn ẩn; (2) Frontend display-condition của icon trong QR code action (không phụ thuộc duy nhất `google_sheet_id`); (3) Action type của QR code action đó không config spreadsheet. |
| Anti-patterns dính | **AP-2** (symptom-only KH report), **AP-6** (mục 3 dev-impact trống). AP-1 KHÔNG dính (fix không phải generic error handler). |

> Trigger space Google-API-failure cover 0/4 → flag [MAJOR] FIX-SHAPE §4.2. Symptom-only + non-reproducible → [MAJOR] SYMPTOM-ONLY §4.2.

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- Không có GAP coverage tuyệt đối cho F1/F2/T1 (đều có ≥1 TC happy path) → **không có BLOCKER cứng**. Tuy nhiên các MAJOR bên dưới đủ để **REJECTED**, đặc biệt việc thiếu toàn bộ negative cho 1 fix đụng Google API.

### 4.2 Major (nên fix)

- `[MAJOR] FIX-SHAPE` GAP-1: Fix tạo sheet qua **Google API** nhưng **0 TC** verify khi Google API lỗi / mất quyền / quota. → Bổ sung TC-NEW-01, TC-NEW-02 (xem §5). Bắt buộc theo **checklist LME C.5** (mất quyền → alert) + **CLJ01** (job sync retry khi rate-limit).
- `[MAJOR] FIX-SHAPE` GAP-2: TC003 nêu "Nhiều landing cùng thiếu `google_sheet_id`" nhưng **không verify rate-limit / retry** khi job tạo **nhiều sheet** trong 1 lần chạy. → Thêm verify job không vượt Google API quota + có retry (CLJ01). Xem TC-NEW-03.
- `[MAJOR] SYMPTOM-ONLY` GAP-3: KH report symptom-only + Dev **không tái hiện được**. Mọi TC giả định root cause = missing `google_sheet_id`. → Hỏi Dev: landing thực tế của KH (`mooriniwt`/bot メディトク) có đúng `google_sheet_id = NULL` không? Bổ sung TC cover **alternative root cause** (`google_sheet_id` đã có nhưng sheet bị xóa/mất quyền → icon vẫn ẩn). Xem TC-NEW-04.
- `[MAJOR] [AP-6]` GAP-4: Mục 3 dev-impact ("Đã check và sửa các function...") **trống** — Dev chưa list caller. → Yêu cầu Dev list caller của `createSheetForLanding()` / điểm gọi job; có thể có nơi khác cũng tạo landing thiếu `google_sheet_id` (root cause gốc lúc TẠO landing chưa được fix, chỉ fix triệu chứng ở job daily).
- `[MAJOR]` GAP-5: Mục 4.2 dev khai **"Không có data update"** nhưng cách fix CREATE sheet + UPDATE `landing.google_sheet_id` + INSERT data. → Yêu cầu Dev sửa 4.2 cho đúng (đây là D-impact thực). Bổ sung boundary/negative cho data: insert **không trùng** khi job chạy lại (idempotency — TC011 chạm nhẹ nhưng cần TC riêng), data rỗng vs đã có.
- `[MAJOR]` Input chưa verify: `01-bug-task.md` auto-filled `2026-06-13 by /new-task` nhưng checkbox "Tester verify auto-fill chính xác" **chưa tick** → tester phải đọc lại Redmine #37396 (description + journal) và tick trước khi review có giá trị.
- `[MAJOR]` Input chưa verify: `03-dev-impact.md` auto-filled `2026-06-13 by /new-task` nhưng checkbox "Tester verify auto-fill chính xác" **chưa tick** → F/D/T có thể chưa đủ; tester verify + tick trước khi giao TC.

### 4.3 Minor (có thể fix sau)

- `[MINOR]` Toàn bộ 18 TC để trống cột **Type** và **Priority** (do convert từ Sheet phân cấp) → member fill Positive/Negative/Boundary/Regression + High/Medium/Low để dễ cân đối tỷ lệ.
- `[MINOR]` TC014 ("Check account staff") title chung — đổi thành "Account staff có quyền: liên kết gg sheet + job sync data landing hoạt động như account chính" (map CL1).
- `[MINOR]` Một số Expected dùng "check màn list và màn detail" — nên ghi rõ màn (List QR / Detail QR action) để đo lường được.

### 4.4 Nit (gợi ý)

- `[NIT]` Tách TC011 thành 2: (a) re-link verify "data sync không bị trùng" (idempotency), (b) verify icon hiển thị — để mỗi TC atomic 1 mục đích.
- `[NIT]` Bổ sung 1 TC i18n nhẹ: filename sheet tạo ra có ký tự JP / đặc biệt (tên bot メディトク) → verify không lỗi (C.5 "ký tự đặc biệt").

---

## 5. TCs đề xuất bổ sung

> Member copy vào `04-tc-list.md` ở round tiếp theo. Map to Impact ghi rõ để Leader trace.

| TC ID gợi ý | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| TC-NEW-01 | Job tạo sheet khi bot đã **mất quyền** Google → báo lỗi, không crash | Bot đã liên kết Google Sheet rồi **revoke quyền** ở Google account; có ≥1 landing thiếu `google_sheet_id` | Chạy job daily (ở Dev) | Job KHÔNG crash; landing đó bỏ qua hoặc log lỗi; GUI hiển thị **alert cảnh báo mất liên kết** để user liên kết lại (C.5); `google_sheet_id` KHÔNG bị set bừa | High | Negative | F1, C.5 |
| TC-NEW-02 | Job gặp **Google API lỗi 5xx / timeout** khi tạo sheet → có retry | Bot liên kết hợp lệ; mock Google API trả lỗi 5xx/timeout lần đầu | Chạy job daily | Job **retry** theo cơ chế CLJ01; lần retry thành công thì tạo sheet + cập nhật `google_sheet_id`; không tạo sheet trùng | High | Negative | F1, F2, CLJ01 |
| TC-NEW-03 | Job tạo **nhiều sheet** 1 lần chạy không vượt **rate-limit** Google | Bot liên kết hợp lệ; ≥ nhiều (lý tưởng ≥ 50–100) landing cùng thiếu `google_sheet_id` | Chạy job daily (ở Dev) | Tất cả landing được tạo sheet + cập nhật `google_sheet_id`; KHÔNG bị Google rate-limit; nếu bị thì job retry phần còn lại (CLJ01) | High | Boundary | F2, CLJ01 |
| TC-NEW-04 | Alternative root cause: `google_sheet_id` ĐÃ có nhưng sheet Google **bị xóa thủ công** → icon Spreadsheet | Landing có `google_sheet_id` hợp lệ; vào Google xóa/đổi quyền sheet đó | Mở màn List QR + Detail QR code action; chạy job daily | Xác định behavior đúng: icon Spreadsheet hiển thị/ẩn theo spec; nếu sheet không còn → hiển thị cảnh báo, KHÔNG silent ẩn icon như bug KH | High | Negative | BUG (alt root cause) |
| TC-NEW-05 | Idempotency: job chạy **lần 2** không insert data trùng / không tạo sheet thứ 2 | Landing đã được job tạo sheet + có `google_sheet_id` ở lần chạy trước | Chạy lại job daily lần 2 | KHÔNG tạo sheet mới; `google_sheet_id` giữ nguyên; data trên sheet KHÔNG bị duplicate | High | Boundary | D-implicit (UPDATE/INSERT) |
| TC-NEW-06 | Filename sheet chứa **ký tự đặc biệt / JP** (tên bot メディトク) | Bot tên có ký tự JP/đặc biệt; landing thiếu `google_sheet_id` | Chạy job tạo sheet | Sheet tạo thành công, tên file không lỗi (C.5 ký tự đặc biệt) | Medium | Boundary | F1, C.5 |

---

## 6. Spec update needed (nếu có)

- [x] Không cần update spec (bug là lỗi data/job, không phải thay đổi business rule). 
- [ ] Cần update spec
- Note: cần Dev/PM làm rõ **spec hiển thị icon Spreadsheet** trong QR code action phụ thuộc điều kiện gì (chỉ `google_sheet_id != NULL`? hay còn check sheet còn tồn tại / còn quyền?) — phục vụ TC-NEW-04. Đây là **câu hỏi spec**, không phải spec update.

---

## 7. Checklist đã chạy

- [x] A. Coverage — A.1 BUG (RISK), A.2 Function (RISK thiếu negative), A.3 Data (RISK + 4.2 sai), A.4 Feature (OK), A.5 không orphan, **A.6 fix-shape → thiếu Google-API-failure**
- [x] B. Chất lượng từng TC — Expected nhiều TC chưa đo lường được rõ màn; Type/Priority trống
- [x] C. Chất lượng bộ TC — **thiếu hẳn Negative**, tỷ lệ lệch về Positive; chưa có boundary rate-limit
- [x] D. Spec alignment — không mâu thuẫn spec; cần làm rõ điều kiện hiển thị icon
- [x] E. Hành chính — file 04 chưa điền "Tester viết TCs" / ngày submit
- [x] F. Base checklist LME
  - [x] F.1 Web — CL1 (staff: TC014 ✅), CL16/CL17 (xóa file/action — không chạm), CL13 (friend access — không trực tiếp)
  - [x] F.2 Job — **CLJ01 Google sync retry/rate-limit: CHƯA cover** → MAJOR (TC-NEW-02/03)
  - [x] F.3 Tính năng chung — **C.5 Google sheet: thiếu "mất quyền → alert", "ký tự đặc biệt", "job retry"** → MAJOR. C.7 Plan limit / C.8 Sort: không chạm.

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | | |
| Tester | (đã đọc & hiểu feedback) | |
