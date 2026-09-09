# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | `#38226 — [Detail friend][Tag] Hiển thị sẵn các tag đang được gắn (folder xổ sẵn từ đầu)` |
| Reviewer (Leader) | `<Leader điền>` |
| Tester được review | `Hạnh Nguyễn` (TC nguồn từ sheet "Improve 2026.05") |
| Ngày review | `2026-06-29` |
| Version TCs | `v1` |
| Vòng review | `Round 1` |

> **Spec reference**: dùng `templates/LME-SYSTEM-SPEC.md` tổng — không có `02-spec-reference.md` riêng cho task này.
> **Nguồn TC**: file 04 fetch từ Google Sheet human "Improve 2026.05" rows 830–847 (18 TC, đã đánh dấu Status `OK`). Đây là TC do người viết, review để bổ sung chiều coverage.

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — Có issue MAJOR, cần fix và review lại

**Lý do ngắn gọn**: Bộ TC bám bug tốt và có chiều sâu khá (add/gỡ/khôi phục/change tag, reload, empty state, staff). Tuy nhiên **2 file input (01, 03) auto-fill từ Redmine chưa được tester verify**, **mục 1 (nguyên nhân) + mục 3 (caller) của dev-impact để trống**, và **thiếu 2 boundary quan trọng** (nhiều folder/tag, phân biệt loại folder). Fix lại các điểm này rồi review vòng 2 — effort thấp.

---

## 2. Tóm tắt cho member

Bộ TC viết khá đầy đủ: không chỉ verify happy-path "folder xổ sẵn" mà còn cover được tái-render sau add/gỡ/khôi phục/đổi-folder tag (cả web + app), reload, trạng thái rỗng và account staff — đây là điểm tốt. Cần bổ sung: (1) tester **tick checkbox verify** ở 01 + 03 và xin Dev điền **mục 1 (nguyên nhân) + mục 3 (caller)** để review có cơ sở chốt expected; (2) thêm **boundary nhiều folder/nhiều tag** và **phân biệt folder default vs folder admin tạo** — đây là nơi logic "tự xổ folder có tag" dễ sai nhất.

---

## 3. Coverage Matrix

| Impact | Loại | Priority | TCs map (suy luận) | # TC | Status |
|---|---|---|---|---|---|
| BUG — folder chứa tag được gắn xổ sẵn ngay từ đầu | Fix | — | TC001, TC013 | 2 | OK |
| F1 — JS render danh sách folder/tag tại tab Tag (detail friend) | Function | Direct | TC001–TC016 | 16 | OK |
| D1 — (không có data — Dev xác nhận không chạm Backend) | Data | — | N/A | — | N/A |
| T1 — Detail friend tab Tag (現在ついているタグ): hiển thị folder/tag đang gắn | Feature | Medium | TC001–TC016 | 16 | **RISK** — đủ positive + empty(TC015/016) + reload(TC014), **thiếu boundary nhiều folder/tag + loại folder** |
| T2 — Add/gỡ tag (web/app/chat 1:1/multi action) | Feature | Medium | TC001–TC005, TC009–TC012, TC017 | 10 | OK |

### ORPHAN TCs

| TC ID | Title | Lý do orphan | Hành động đề xuất |
|---|---|---|---|
| — | — | Không có TC lạc chủ đề. TC017 (regression add/gỡ), TC018 (acc staff) đều thuộc scope T2 + checklist LME (CL-Func-1). | Giữ nguyên |

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| Fix shape (đọc mục 2 dev-impact) | **Khác — UI default-state / render change** (frontend JS: mặc định **xổ sẵn** folder đang chứa tag được gắn). Không phải generic-catch / validation / race-condition / migration. |
| Trigger space cần cover | Trạng thái render folder: (a) folder **có** tag được gắn → xổ; (b) folder **không** tag → không hiển thị; (c) **nhiều** folder có tag; (d) **loại folder** (chưa phân loại / 2 default / admin tạo); (e) re-render sau add / gỡ / khôi phục / change-folder tag; (f) reload; (g) user tự đóng folder rồi reload; (h) empty (friend chưa có tag). |
| Số trigger TCs hiện cover | ~6/8 — cover (a),(b),(e),(f),(g),(h). **Thiếu (c) nhiều folder/tag** và **(d) loại folder**. |
| KH report dạng | **Có root cause cụ thể** (SpecImprove — expected behavior rõ ràng: folder có tag xổ sẵn). Không phải symptom-only → **không** dính AP-2. |
| Alternative root causes cần verify | N/A (ticket cải tiến UX, không phải bug ẩn root cause). |
| Anti-patterns dính | **AP-6** (mục 3 dev-impact trống). AP-1/AP-2/AP-4 không áp dụng (không phải generic error-fix). AP-3 nhẹ: T1 thiếu edge-state boundary. |

> T1 trigger space cover < tổng (thiếu nhiều-folder + loại-folder) → flag [MAJOR] FIX-SHAPE ở §4.2.

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- Không có. BUG root cause + F1 Direct + T1/T2 đều có TC verify; không GAP coverage cho direct/high-risk impact.

### 4.2 Major (nên fix)

- **[MAJOR] INPUT chưa verify (file 01)**: `01-bug-task.md` auto-filled `2026-06-29 by /new-task` nhưng checkbox **"Tester verify auto-fill chính xác" CHƯA tick** — tester cần đọc lại Redmine #38226 (description + journal Tái hiện) và tick trước khi review có giá trị chốt.
- **[MAJOR] INPUT chưa verify (file 03)**: `03-dev-impact.md` auto-filled nhưng checkbox verify **chưa tick** — F/D/T trong 4.1/4.2/4.3 do `/new-task` suy ra từ note ngắn của Dev ("UI màn /basic/friendlist/my_page tab tag, Ko ảnh hưởng Backend"), có thể chưa đủ. Tester verify + tick.
- **[MAJOR] AP-6 — mục 3 (caller đã check) trống**: Dev không list nơi nào dùng chung function/component render danh sách folder/tag. Cần xác nhận **không có màn khác** (vd modal multi action, modal filter, chat 1:1 right bar) dùng lại đúng component "folder dropdown tag" này — nếu có, fix JS có thể vô tình đổi hành vi ở đó. Yêu cầu Dev xác nhận.
- **[MAJOR] Mục 1 (nguyên nhân) trống**: Không có root cause → không chốt được **điều kiện chính xác để 1 folder được tự xổ** (chỉ folder có ≥1 tag *đang gắn cho friend này*? hay mọi folder có tag bất kỳ?). Expected của TC hiện chỉ ghi "xổ sẵn" chung chung. Xin Dev điền nguyên nhân để chốt expected.
- **[MAJOR] FIX-SHAPE / Boundary nhiều folder + nhiều tag (T1, CL-Func-12 max)**: Chưa có TC cho friend có **nhiều folder chứa tag** (vd >10 folder, mỗi folder nhiều tag) → verify tất cả xổ sẵn đúng, không vỡ layout, scroll bình thường, không lệch caret. Đây là nơi logic auto-expand dễ sai/chậm nhất. → thêm TC-NEW-01.
- **[MAJOR] Phân biệt loại folder (C.3/C.4 — 3 loại folder)**: Chưa phân biệt **folder chưa phân loại / 2 folder default / folder admin tạo**. Logic tự xổ có thể khác nhau theo loại folder. → thêm TC-NEW-02.

### 4.3 Minor (có thể fix sau)

- **[MINOR] CL-Func-3 (chuyển tab setting)**: Chưa có TC switch từ tab タグ sang tab khác (基本情報 / アクション履歴) rồi quay lại → verify trạng thái xổ folder giữ đúng, không bị reset/đổi. → TC-NEW-03.
- **[MINOR] CL-NonF-1 (Compatibility)**: Fix là render JS frontend → nên ghi rõ test **Win + Mac (Chrome + Safari)** cho web và **Android + iOS** cho app. TC005/011/012 có chạm app/mobile nhưng chưa khai báo ma trận thiết bị. → TC-NEW-04.
- **[MINOR] Cột Type/Priority trống toàn bộ**: Nguồn sheet không có → member bổ sung phân loại (Positive/Boundary/Regression) + Priority để Leader đánh giá tỷ lệ chiều test (C §review-checklist).
- **[MINOR] Expected forward-fill mơ hồ**: TC002–TC005, TC008 ghi expected "(như TC001)" do gộp cell merge từ sheet → member viết expected tường minh cho từng TC (đo lường được), tránh 2 người chạy hiểu khác nhau (B.1).

### 4.4 Nit (gợi ý)

- **[NIT] Sai số row trong Redmine**: Redmine ghi `Row: 808 ~ 827` nhưng range đó là TC **richmenu sort**; file 04 đã tự sửa dùng đúng rows 830–847. Confirm lại với người tạo ticket để lần sau không nhầm.
- **[NIT] TC016 empty-state**: Bổ sung verify **đúng chuỗi** `タグが設定されていません。` ở cả web + app (không chỉ "hiển thị trống").
- **[NIT] Atomic TC013**: TC013 verify đồng thời "F1+F2 xổ sẵn" + "F3 không hiện" + "đủ 3 dòng tag" — có thể tách case F3-không-hiện ra TC riêng cho dễ trace.

---

## 5. TCs đề xuất bổ sung

> Member copy vào `04-tc-list.md` ở round tiếp theo.

| TC ID gợi ý | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| TC-NEW-01 | Boundary — friend có nhiều folder/nhiều tag đều xổ sẵn | Friend được gắn tag ở **≥10 folder**, mỗi folder ≥5 tag | 1. Mở detail friend → tab タグ (現在ついているタグ)<br>2. Quan sát toàn bộ danh sách ngay khi load<br>3. Scroll hết danh sách | Tất cả folder có tag đều **xổ sẵn** hiển thị đủ tag; không vỡ layout, caret đúng trạng thái mở, scroll mượt, không thiếu/ trùng folder | High | Boundary | T1, F1 |
| TC-NEW-02 | Phân biệt loại folder khi auto-expand | Friend có tag ở **folder chưa phân loại** + **folder default** + **folder admin tạo** | 1. Mở detail friend → tab タグ<br>2. Quan sát trạng thái xổ của từng loại folder | Cả 3 loại folder **nếu có tag được gắn** đều xổ sẵn như nhau; loại folder không có tag không hiển thị | High | Positive | T1, F1 |
| TC-NEW-03 | Giữ trạng thái xổ khi chuyển tab rồi quay lại | Friend có ≥2 folder chứa tag | 1. Vào tab タグ (folder xổ sẵn)<br>2. Chuyển sang tab 基本情報 / アクション履歴<br>3. Quay lại tab タグ | Folder có tag vẫn hiển thị xổ sẵn đúng, không reset sai trạng thái, không lỗi render | Medium | Regression | T1 (CL-Func-3) |
| TC-NEW-04 | Compatibility hiển thị tab Tag đa nền tảng | Tài khoản test trên Win Chrome, Mac Safari, Android app, iOS app | 1. Mở detail friend → tab タグ trên từng nền tảng<br>2. So sánh trạng thái xổ folder + hiển thị tag | Hành vi xổ sẵn folder có tag **đồng nhất** trên Win/Mac (web) và Android/iOS (app), không lệch layout | Medium | Compatibility | T1 (CL-NonF-1) |

---

## 6. Spec update needed

- [x] Không cần update spec — đây là ticket **SpecImprove** (cải tiến hành vi hiển thị), expected behavior đã rõ trong Redmine; không mâu thuẫn LME-SYSTEM-SPEC tổng. Khi fix merge, nên cập nhật spec feature Detail friend / tab Tag để ghi nhận "folder chứa tag đang gắn mặc định xổ sẵn".

---

## 7. Checklist đã chạy

- [x] A. Coverage — A.1 BUG ✓ / A.2 F1 ✓ / A.3 D1 N/A / A.4 T1 RISK(boundary) T2 ✓ / A.5 không orphan / A.6 fix-shape (§3.5)
- [x] B. Chất lượng từng TC — B.1 expected vài TC mơ hồ (MINOR) / B.2 TC013 hơi gộp (NIT) / B.3 OK / B.4 OK
- [x] C. Chất lượng bộ TC tổng thể — thiếu khai báo Type/Priority (MINOR); chưa có ma trận thiết bị (MINOR)
- [x] D. Spec alignment — không mâu thuẫn (dùng LME-SYSTEM-SPEC tổng)
- [x] E. Hành chính — nguồn sheet read-only; thiếu version/tester ký ở file 04 (member điền sau)
- [x] F. Base checklist LME
  - [x] F.1 Checklist web — **CL-Func-1** (staff: TC018 ✓), **CL-Func-2** (reload: TC014 ✓), **CL-Func-3** (chuyển tab: ✗ → MINOR/TC-NEW-03), **CL-Func-12** (max: ✗ → MAJOR/TC-NEW-01), **CL-NonF-1** (Win/Mac+Android/iOS: ✗ → MINOR/TC-NEW-04)
  - [x] F.2 Checklist job — N/A (fix thuần frontend, không chạm job)
  - [x] F.3 Các tính năng chung — **C.4 Tag** là feature chính: hiển thị/update tag tại detail friend (My page tab タグ), chat 1:1 right bar, multi action, app — đã cover phần lớn; **C.3 3 loại folder** chưa cover (MAJOR/TC-NEW-02). Các nơi hiển thị tag KHÁC (QL tag list, CSV export, cross analysis, modal filter) **không** đòi TC vì fix chỉ chạm JS render của tab Tag detail friend (xem AP-5 / root-cause-layer-focus).

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | | |
| Tester | (đã đọc & hiểu feedback) | |
