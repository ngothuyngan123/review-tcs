# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | `#38003 — Sửa màn hình lịch sử access bot theo sort theo time_access` |
| Reviewer (Leader) | `<Leader verify>` (draft sinh bởi `/review-tc`) |
| Tester được review | `<chưa điền — file 04 chưa có tên tester>` |
| Ngày review | `2026-06-22` |
| Version TCs | `<file 04 chưa điền version>` |
| Vòng review | `Round 1` |

> **Note spec reference**: Không có `02-spec-reference.md` riêng → dùng `templates/LME-SYSTEM-SPEC.md` tổng + `framework/checklist-lme.md`. Không có spec riêng cho màn "lịch sử access bot" trong task này.

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — Có issue BLOCKER, cần fix và review lại

**Lý do ngắn gọn**: Bộ TC fetch (TC-AH-019→029) test **hành vi GHI lịch sử access** (whether record được log — concern của task #37743), **KHÔNG có TC nào verify 2 fix thực của #38003**: (1) sort danh sách theo `time_access` thay vì `id`; (2) dropdown chọn bot trên màn hoạt động. Toàn bộ root cause + F2/F3/F4 + T2 ở trạng thái **GAP**.

---

## 2. Tóm tắt cho member

Bộ TC hiện tại là TC regression của **việc ghi lịch sử access** (lấy từ tab `[AI] TCs_37743`, row 23-32) — chất lượng từng TC tốt, rõ steps/expected. **Nhưng nhầu hết lạc chủ đề với fix #38003**: fix này chỉ chạm **tầng hiển thị** (sort theo `time_access` + sửa dropdown chọn bot + export CSV + detail bot Supper Admin), trong khi các TC lại test **tầng ghi record** (middleware/setBotInvite) — Dev đã confirm "data impact = không có", nghĩa là logic ghi không bị đụng. Cần **bổ sung TC trực tiếp cho fix**: assert thứ tự dòng theo `time_access` (gồm tie-break + biên ngày 23:59→00:01), dropdown chọn bot reload đúng history, export CSV đúng thứ tự + format giờ, và regression detail bot. Xem §5.

---

## 3. Coverage Matrix

> Map suy luận từ Title / Precondition / Steps / Expected. File 04 không có cột "Map to Impact".
> Lưu ý: các TC "Vào màn アクセス履歴 → có 1 dòng record" chỉ **verify record xuất hiện**, KHÔNG assert **thứ tự sort** hay **dropdown** → không tính là cover fix.

| Impact | Loại | Priority (suy luận) | TCs cover (suy luận) | # TC hiệu lực | Status |
|---|---|---|---|---|---|
| **BUG** — sort theo `time_access` + dropdown chọn bot | Fix | — | *(không TC nào assert thứ tự sort / dropdown)* | **0** | **GAP** |
| **F2** — `getAccessHistories` (order list) | Function | Direct (suy luận) | TC-AH-021 chỉ render màn, không assert order | **0** | **GAP** |
| **F4** — dropdown bot `access_histories.js` | Function | Direct (suy luận) | *(TC-AH-027/029 test ghi record khi đổi bot ở header/home, KHÔNG phải dropdown filter trên màn history)* | **0** | **GAP** |
| **F3** — `exportCsvAccessHistory` | Function | — | — | **0** | **GAP** |
| **F1** — `detailBot` (Supper Admin) | Function | — | — | **0** | **GAP** |
| **F5** — view `access_histories.blade.php` | Function | — | TC-AH-021 (render data cũ) | 1 | **RISK** (render OK, không assert order/dropdown) |
| **T1** — Màn lịch sử access bot | Feature | — | TC-AH-019, 019b, 020, 021, 024-029 (regression *ghi* record) | nhiều nhưng off-fix | **RISK** |
| **T2** — Export CSV lịch sử access | Feature | — | — | **0** | **GAP** |
| **T3** — Detail bot Supper Admin | Feature | — | — | **0** | **GAP** |

### ORPHAN TCs

> AP-5 (layer-downstream over-coverage): fix #38003 chạm **tầng hiển thị** (order + dropdown + export + detail). Các TC dưới test **tầng ghi record** — Dev confirm data/logic ghi KHÔNG bị đụng (4.2 = không có) → không cover fix.

| TC ID | Title | Lý do orphan | Hành động đề xuất |
|---|---|---|---|
| TC-AH-019 / 019b | setBotInvite vẫn ghi history như cũ | Test path GHI record (write), fix không chạm | Giữ làm regression nhẹ T1 HOẶC remove (đã có ở task 37743) |
| TC-AH-020 | setBotInvite + access cùng ngày không trùng | Test dedup ghi, fix không chạm | Remove / để 37743 |
| TC-AH-024 / 025 / 026 | Login → chọn bot → ghi history | Test write path, fix không chạm | Remove / để 37743 |
| TC-AH-027 / 028 / 029 | Đổi bot ở header/home → ghi history bot đích | Test write path khi đổi bot — **KHÔNG** phải dropdown filter trên màn history (F4) | Remove / để 37743; KHÔNG nhầm là cover F4 |
| TC-AH-021 | Dữ liệu lịch sử cũ vẫn hiển thị bình thường | TC **duy nhất** liên quan T1/F5 (render sau deploy) | **Giữ** — re-label rõ là regression hiển thị màn history |

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| Fix shape (mục 2 dev-impact) | **Khác** — (a) Sort/ordering fix (`order by id` → `order by time_access`); (b) UI component fix (dropdown chọn bot). KHÔNG phải generic catch / validation / race / migration. |
| Trigger space cần cover | **Sort**: thứ tự desc/asc đúng, tie-break khi `time_access` bằng nhau, `time_access` null/empty, biên ngày 23:59→00:01, nhiều ngày, dataset lớn (≥1000), sort stability sau add/edit. **Dropdown**: chọn bot → reload đúng history bot đó, default value, tap/hover behavior (CL-Func-24/TC-24), bot không quyền không hiện. **Export CSV**: thứ tự dòng khớp màn + format datetime (TC-05/TC-23). |
| Số trigger TCs hiện cover | **0 / ~12** (không TC nào assert ordering, dropdown filter, hay export) |
| KH report dạng | **Symptom-only / rỗng** — Redmine description trống hoàn toàn, không có Steps/Expected/Actual của KH. Root cause chỉ do Dev cung cấp (2 nguyên nhân cụ thể). Rủi ro alternative-root-cause **thấp** vì Dev nêu rõ code-level cause, nhưng TC vẫn phải bám đúng 2 cause này (hiện chưa bám cause nào). |
| Alternative root causes cần verify | N/A (root cause concrete) — nhưng cần xác nhận với Dev: ngoài `time_access`, có cần tie-break phụ (vd `id`) khi 2 record cùng giây không? Dropdown sửa ở JS hay cả server-side filter? |
| Anti-patterns dính | **AP-5** (orphan logging TCs), **AP-6** (mục 3 dev-impact trống), **AP-2** (KH report rỗng — bám 1 nguồn root cause Dev) |

> Trigger space cover **0/~12** → flag **[BLOCKER] FIX-SHAPE** trong §4.1.

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- **[BLOCKER] FIX-SHAPE / GAP-BUG**: Không có TC nào assert **thứ tự sort theo `time_access`** — đây là fix #1 của ticket. Bộ TC chỉ verify "record xuất hiện trên màn", không kiểm tra thứ tự. → Thêm TC-NEW-01/02/03 (§5): sort desc đúng, tie-break, biên ngày.
- **[BLOCKER] FIX-SHAPE / GAP-F4**: Không có TC nào verify **dropdown chọn bot trên màn lịch sử access** hoạt động (fix #2). TC-AH-027/029 test ghi record khi đổi bot ở *header/home* — **khác** với dropdown filter trên màn history. → Thêm TC-NEW-04/05 (§5).
- **[BLOCKER] GAP-F3 / T2**: Không có TC nào cho `exportCsvAccessHistory` (export CSV) — Dev list là impacted. Sau fix order, thứ tự dòng trong CSV và format giờ phải được verify (CL-Func-23/TC-05). → Thêm TC-NEW-06.
- **[BLOCKER] GAP-F1 / T3**: Không có TC nào cho `detailBot` trong Supper Admin — Dev list là impacted (F1). → Thêm TC-NEW-07 (regression detail bot hiển thị đúng sau fix).

> Ghi chú severity: Dev **không** ghi cột Direct/Indirect ở 4.1 nên không thể auto-phân BLOCKER theo "Direct impact". 2 fix chính (sort, dropdown) chắc chắn Direct → BLOCKER. F1/F3 Leader confirm mức Direct/Indirect với Dev; tạm để BLOCKER vì 0 coverage trên function được list.

### 4.2 Major (nên fix)

- **[MAJOR] AUTO-FILL chưa verify (file 01)**: `01-bug-task.md` có `Auto-filled: 2026-06-22 by /new-task` nhưng checkbox "Tester verify auto-fill chính xác" **chưa tick**. Yêu cầu tester đọc lại Redmine #38003 và tick trước khi review có giá trị.
- **[MAJOR] AUTO-FILL chưa verify (file 03)**: `03-dev-impact.md` tương tự — checkbox chưa tick. F/D/T có thể chưa đầy đủ/mapping sai (đặc biệt Dev không phân Direct/Indirect, không ghi risk level).
- **[MAJOR] AP-6 — mục 3 dev-impact trống**: "Đã check và sửa các function caller" chỉ có heading, không list. → Hỏi Dev: ngoài màn access history, còn màn nào khác cũng `order by id` cùng pattern bug, hoặc dropdown bot dùng chung component không?
- **[MAJOR] SYMPTOM-ONLY (file 01)**: Redmine description **rỗng**, không có steps/expected/actual của KH. TC bám hoàn toàn vào root cause Dev tự nêu. → Xác nhận với Dev/PM behavior mong đợi chính xác của sort (desc hay asc? tie-break field?).
- **[MAJOR] §C.8 Sort (checklist LME) chưa cover**: Task chính là **sort** — phải base §C.8. Thiếu: sort stability, sort sau thao tác liên tục (CL-Func-4: "Add mới→Sort", "Edit→Sort"), reload sau sort không lỗi (CL-Func-2), phân trang scroll-to-top (CL-Func-15).
- **[MAJOR] TC-24 / CL-Func-24 (dropdown UI) chưa cover**: dropdown là UI component → test hành vi tap/hover/default value, paste không áp dụng nhưng tap-behavior bắt buộc.

### 4.3 Minor (có thể fix sau)

- **[MINOR] File 04 thiếu metadata**: "Tester viết TCs", "Ngày submit", "Version TCs" để placeholder `<member điền>`. Cần điền trước khi chốt.
- **[MINOR] Title TC-AH-027/029 dễ gây nhầm**: "Đổi bot... select bot ở header/admin home" dễ bị hiểu nhầm là cover dropdown fix (F4). Nếu giữ làm regression, nên nói rõ "ghi history" để tách khỏi dropdown filter màn history.
- **[MINOR] gid → tab map bằng suy luận**: MCP google-sheets không expose `sheetId`; tab `[AI] TCs_37743` được suy luận từ "Line 23~32". Tab này mang tên task **37743** (khác ticket) → củng cố nghi vấn các TC vốn không thuộc #38003. Tester verify lại đúng tab/row trong Redmine.

### 4.4 Nit (gợi ý)

- **[NIT]** Cân nhắc tách bộ TC #38003 sang tab riêng (vd `[AI] TCs_38003`) thay vì append vào tab 37743, để coverage rõ ràng theo ticket.
- **[NIT]** TC-AH-020/026... có `⏳ Pending QA` — nếu giữ trong scope #38003 thì resolve hoặc chuyển về task 37743.

---

## 5. TCs đề xuất bổ sung

> Member copy vào `04-tc-list.md` round tiếp theo. Đây là TC **trực tiếp cho fix #38003** (góc nhìn manual tester — quan sát UI, không dẫn bằng query DB).

| TC ID gợi ý | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| TC-NEW-01 | Lịch sử access sort theo `time_access` (mới nhất trên cùng), KHÔNG theo id | Bot X có ≥3 record access mà **thứ tự `time_access` ngược với thứ tự id** (vd record id nhỏ nhưng time_access mới hơn) | 1. Admin mở màn アクセス履歴 bot X | Các dòng hiển thị **giảm dần theo アクセス日時 (time_access)** — dòng có time_access mới nhất ở trên cùng; KHÔNG còn sắp theo id | High | Positive | BUG, F2, T1 |
| TC-NEW-02 | Tie-break khi 2 record cùng `time_access` | Bot X có 2 record access **cùng giây** time_access | 1. Mở màn アクセス履歴 bot X<br>2. Quan sát 2 dòng cùng giờ | 2 dòng hiển thị ổn định, không nhảy thứ tự khi reload (xác nhận tie-break field với Dev — vd id phụ) | Medium | Boundary | BUG, F2 |
| TC-NEW-03 | Sort đúng qua biên ngày 23:59 → 00:01 và nhiều ngày | Bot X có record lúc 23:59 ngày D và 00:01 ngày D+1 (+ vài ngày trước) | 1. Mở màn アクセス履歴 bot X | Thứ tự đúng theo mốc thời gian thực (00:01 D+1 đứng trên 23:59 D); không lẫn lộn do so sánh text/date (TC-04) | Medium | Boundary | BUG, F2, T1 |
| TC-NEW-04 | Dropdown chọn bot trên màn lịch sử access reload đúng history | User có quyền bot X và bot Y; mỗi bot có record khác nhau | 1. Mở màn アクセス履歴, dropdown đang ở bot X<br>2. Chọn bot Y trên **dropdown của màn** | Danh sách reload sang đúng access history của **bot Y** (không còn của bot X, không trộn lẫn) | High | Positive | BUG, F4, T1 |
| TC-NEW-05 | Dropdown bot — default value + hành vi tap (CL-Func-24/TC-24) | User có quyền ≥2 bot | 1. Mở màn, kiểm tra giá trị mặc định dropdown<br>2. Tap mở/đóng dropdown, di chuyển chọn | Default đúng bot context hiện tại; tap mở list đầy đủ bot có quyền; chọn xong list cập nhật; không lỗi JS/console | Medium | Boundary | F4, T1 |
| TC-NEW-06 | Export CSV lịch sử access — thứ tự dòng + format giờ khớp màn | Bot X có nhiều record nhiều ngày (đã sort theo time_access trên màn) | 1. Mở màn アクセス履歴 bot X<br>2. Bấm export CSV<br>3. Mở file CSV | Thứ tự dòng trong CSV **khớp thứ tự màn** (theo time_access); cột アクセス日時 đúng format datetime spec (TC-05/TC-23); không lệch giờ | High | Positive | F3, T2 |
| TC-NEW-07 | Regression: detail bot trong Supper Admin hiển thị đúng sau fix | Tài khoản Supper Admin; bot X tồn tại | 1. Vào Supper Admin → detail bot X | Màn detail bot load đúng, không lỗi sau khi sửa `detailBot`; thông tin bot hiển thị đầy đủ | Medium | Regression | F1, T3 |
| TC-NEW-08 | Sort dataset lớn + phân trang scroll-to-top | Bot X có ≥1000 record access | 1. Mở màn, cuộn/loadmore hoặc next page | Thứ tự time_access đúng xuyên suốt các trang; next page tự scroll lên đầu (CL-Func-15); không treo/lỗi performance | Low | Boundary | F2, T1 |
| TC-NEW-09 | Thao tác liên tục: reload sau khi sort/đổi bot không lỗi | Bot X có record | 1. Đổi bot qua dropdown<br>2. Reload màn (F5)<br>3. Đổi tiếp bot khác → reload | Sau reload màn giữ đúng dữ liệu/sort, không lỗi (CL-Func-2, CL-Func-4) | Low | Regression | F2, F4, T1 |
| TC-NEW-10 | Security: staff không quyền gõ trực tiếp URL access-histories?bot_id=X | Staff role ≠ admin, không quyền bot X | 1. Đăng nhập staff<br>2. Gõ URL /admin/access-histories?bot_id=X | Bị redirect / báo「この権限は許可されていません。」, không xem được history (CL-NonF-2) | Medium | Negative | F2, T1 |

---

## 6. Spec update needed

- [x] Không cần update spec
- [ ] Cần update spec

> Lưu ý: cần Dev/PM **làm rõ behavior sort** (desc/asc, tie-break field) vì Redmine description rỗng — không phải update spec mà là bổ sung định nghĩa expected để viết TC chính xác.

---

## 7. Checklist đã chạy

- [x] A. Coverage — **FAIL**: BUG/F1/F2/F3/F4/T2/T3 = GAP
- [x] B. Chất lượng từng TC — **PASS** (các TC fetch rõ ràng, atomic) nhưng off-scope
- [x] C. Chất lượng bộ TC tổng thể — **FAIL**: thiếu Negative/Boundary cho chính fix; 0 TC cho dimension sort & dropdown
- [x] D. Spec alignment — N/A (không spec riêng); cần clarify expected sort với Dev
- [x] E. Hành chính — **MINOR**: thiếu tên tester / version trong file 04
- [x] F. Base checklist LME
  - [x] F.1 Checklist web — **FAIL**: CL-Func-24 (dropdown), CL-Func-2/4/15 (sort+reload+phân trang), CL-NonF-2 (security URL) chưa cover
  - [ ] F.2 Checklist job — N/A (fix không chạm job)
  - [x] F.3 Các tính năng chung — **FAIL §C.8 Sort** (task là sort nhưng không base §C.8); C.1-C.7 N/A

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | `<Leader verify draft này>` | |
| Tester | (đã đọc & hiểu feedback) | |

<!-- Draft sinh bởi /review-tc lúc 2026-06-22. Dựa trên 4 file input trong folder; không fetch Redmine. Leader verify trước khi gửi member. -->
