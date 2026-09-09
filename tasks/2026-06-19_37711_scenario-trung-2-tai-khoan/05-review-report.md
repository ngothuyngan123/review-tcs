# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | #37711 — [T11271][Scenario] Cùng 1 khách hiển thị 2 tài khoản trùng, scenario chạy song song |
| Reviewer (Leader) | `<Leader verify>` |
| Tester được review | `<member điền — file 04 chưa ghi tên>` |
| Ngày review | 2026-06-22 |
| Version TCs | v1 (42 TC human + 11 TC delta) |
| Vòng review | Round 1 |

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — Có issue BLOCKER/MAJOR, cần fix và review lại

**Lý do ngắn gọn**: Bộ TC phủ happy-path rất tốt (42 TC human cover mọi entry-point + 11 delta bù race/dedup/edge). NHƯNG còn **1 BLOCKER scope**: chưa chốt branch fix nào được merge (job-side `HandlePostbackTask` vs web-side `QRCodeController::checkFriend`) — quyết định trực tiếp TC-D01 (BUG reproduce) có verify đúng đường gây bug của KH hay không. Cộng thêm vài MAJOR về thiếu chiều concurrent cho F4/F5 và cách ép race.

---

## 2. Tóm tắt cho member

Bộ TC rất chắc ở phần phủ rộng — 42 TC human đã cover đủ mọi entry-point tạo bạn (QR/form/booking/item) và 11 TC delta bù đúng các lỗ hổng quan trọng (ép race, dedup giữ-min-id, không xóa nhầm user khác, edge block/đã-xóa). Điểm cần fix trước khi chạy test: **(1)** chốt với Dev branch nào thực sự merge — vì 2 bản fix nằm ở 2 layer khác nhau, nếu chọn nhầm thì TC-D01 test sai chỗ; **(2)** bổ sung biến thể concurrent cho luồng "bạn cũ nhắn tin lại" (F4) và "group friend" (F5) vì đó cũng là điểm insert mà fix chạm; **(3)** thêm cách ép/giả lập race để tránh false-pass "không reproduce = pass".

---

## 3. Coverage Matrix

| Impact | Loại | Priority | TCs map (suy luận) | # TC | Status |
|---|---|---|---|---|---|
| BUG (race web⨯job → 2 line_user) | Fix | — | TC-D01, TC-H12, TC-H42 | 3 | **RISK** (xem BLOCKER-1: reproduce phụ thuộc branch) |
| F1 — `checkDuplicateLineUserAfterInsert` (mới) | Function | Direct | TC-D01, D02, D03, D04 | 4 | OK |
| F2 — `findFirstByLineIdOrderByIdAsc` (mới) | Function | Direct | TC-D02 (giữ bản id nhỏ nhất) | 1 | OK |
| F3 — `doHandleFollowEvent` | Function | Direct | TC-H01, H07, H12, D01, D08 | 5 | OK |
| F4 — `checkAddOldFriend` | Function | Direct | TC-H02 | 1 | **RISK** (chỉ positive, thiếu concurrent/negative) |
| F5 — `checkAddGroupFriend` | Function | Direct | TC-H03, H08 | 2 | **RISK** (chỉ positive, thiếu concurrent) |
| F6 — `checkAddGroup` (member add) | Function | Direct | TC-D07 | 1 | OK |
| D1 — `line_user` (DELETE bản trùng, giữ min-id) | Data | — | TC-D01, D02, D03, D04 + mọi H-create | 8+ | OK |
| D2 — Elasticsearch (KHÔNG sync bản trùng) | Data | — | (ngầm qua GUI list) | 0 explicit | **RISK** (không có TC search/ES riêng) |
| D3 — schema/migration | Data | — | N/A (không đổi schema) | — | N/A |
| T1 — Follow/kết bạn | Feature | High | TC-H01, H07, H12, D01, D08, D09 | 6 | OK |
| T2 — `checkAddOldFriend` (bạn cũ nhắn tin lại) | Feature | Medium | TC-H02 | 1 | **RISK** (1 happy-path, không edge) |
| T3 — Group / member | Feature | Medium | TC-H03, H08, D07 | 3 | OK |
| T4 — Scenario (ステップ配信) không chạy song song | Feature | High | TC-H04–06, H09–11, H19–21, H24–26, H29–31, H34–36, H39–41, D10, D11 | 20+ | OK |

### ORPHAN TCs

| TC ID | Title | Lý do orphan | Hành động đề xuất |
|---|---|---|---|
| — | — | Không phát hiện TC lạc chủ đề | Mọi TC đều map về BUG / F* / D* / T* hoặc CL checklist LME |

> Ghi chú AP-5 (over-coverage): các TC test scenario nhiều step (H05/H06...) test đúng symptom (gửi trùng) — KHÔNG over-test layer scenario engine (engine không bị chạm code), nên giữ là regression hợp lệ, không phải orphan.

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| Fix shape (mục 2 dev-impact) | **Race-condition** (dedup sau insert: check line_id, giữ bản id nhỏ nhất, xóa bản vừa tạo) |
| Trigger space cần cover | Đồng thời tạo line_user cùng line_id tại các điểm insert: **web checkFriend ⨯ job follow**, **double-click/mở link liên tiếp**, **2 user khác line_id đồng thời** (no-cross-collision), **các insert point khác**: follow / checkAddOldFriend / checkAddGroupFriend / checkAddGroup |
| Số trigger TCs hiện cover | web⨯job: ✅ D01 · double-click: ✅ D03 · 2-user cross: ✅ D04 · group member: ✅ D07 · **old-friend⨯follow: ❌** · **group-friend⨯callback: ❌** (chỉ có happy-path H02/H03) |
| KH report dạng | **Symptom-only** ("hiển thị 2 tài khoản trùng", không error code) + **Steps reproduce TRỐNG** (bug không tái hiện được trong Redmine) |
| Alternative root causes cần verify | (a) race web⨯job ✅ cover · (b) race **job⨯job** (2 follow callback / LINE gửi webhook follow trùng) ❌ chưa có TC · (c) race tại checkAddOldFriend/checkAddGroup ❌ · (d) bản trùng CŨ tồn tại trước fix (ngoài scope fix — cần DBA) |
| Anti-patterns dính | **AP-2** (symptom-only KH report) · **AP-4** (thiếu PR/diff link — chỉ có commit hash, không verify được fix đặt đủ điểm insert) |

> ⚠️ Fix race-condition shape — câu hỏi adversarial bắt buộc ("có test đồng thời ≥2 request? multi-tab/device?") → **CÓ** (D01/D03/D04). Vì vậy KHÔNG phải BLOCKER concurrency. Nhưng race chỉ cover 1/4 điểm insert (web⨯job); còn 2 điểm insert (old-friend, group) chỉ có happy-path → **MAJOR**, không phải đủ chiều.

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- **[BLOCKER] FIX-SHAPE / SCOPE — Chưa chốt branch merge (job-side vs web-side)**: `03-dev-impact.md` ghi nhận **2 bản fix khác layer**: (a) Kim Cúc — job-side `HandlePostbackTask` (dedup tại doHandleFollowEvent / checkAddOldFriend / checkAddGroupFriend / checkAddGroup), branch `m_202606_duplicate_line_user_37711`; (b) AI auto-fix — web-side `QRCodeController::checkFriend` + `FormAnswerController`, branch `ai_fixbug_37711`. **Bản job-side KHÔNG liệt kê điểm insert phía web `checkFriend`** — mà theo chính phân tích root cause, web checkFriend là 1 trong 2 luồng tạo bản trùng. Nếu chỉ merge bản job-side, đường web vẫn có thể thắng race và bản trùng-web không được dedup → **TC-D01 (đúng flow KH: mở form ⨯ follow) sẽ FAIL hoặc cho kết quả không xác định**. — **Đề xuất**: Leader confirm với Dev branch merge thực tế + xác nhận điểm insert web checkFriend có được guard không. Chốt xong mới chạy test, nếu không TC-D01 không có giá trị verify.

### 4.2 Major (nên fix)

- **[MAJOR] FIX-SHAPE: thiếu concurrent test cho F4 (`checkAddOldFriend`) và F5 (`checkAddGroupFriend`)** — đây là 2 điểm insert mà fix chạm code (mục 4.1), nhưng TC chỉ có happy-path (H02, H03/H08), không có biến thể đua như D01. Race tại "bạn cũ nhắn tin lại đúng lúc follow callback" hoặc "thêm member group đúng lúc member gửi tin" hoàn toàn có thể tạo trùng. — **Đề xuất**: thêm TC-NEW-01, TC-NEW-02 (xem §5).
- **[MAJOR] SYMPTOM-ONLY / AP-2: alternative root cause chưa cover hết** — KH chỉ báo triệu chứng "2 tài khoản trùng" + Steps reproduce TRỐNG. TC cover web⨯job nhưng chưa cover **race job⨯job** (LINE gửi follow webhook trùng / 2 callback chồng nhau) — đường này không cần web vẫn tạo trùng. — **Đề xuất**: hỏi Dev có chặn trùng khi 2 follow callback cùng line_id không; thêm TC-NEW-03.
- **[MAJOR] D2 (Elasticsearch) không có TC verify riêng** — fix ghi rõ "bản trùng KHÔNG sync lên Elasticsearch". Hiện chỉ verify gián tiếp qua "GUI hiển thị 1 line_user". Search friend theo tên (ES-backed) có thể là nơi lộ bản trùng nếu sync sai. — **Đề xuất**: thêm TC search friend theo tên → đúng 1 kết quả (TC-NEW-04).
- **[MAJOR] AP-4: thiếu PR/diff link** — `03-dev-impact.md` mục "Commit / Pull Request" chỉ có commit hash `2f32444...`, không có URL PR/diff xem được. Không thể verify fix thực sự đặt guard ở **đủ** các điểm insert (đặc biệt điểm web). — **Đề xuất**: yêu cầu Dev cấp link diff để confirm fix shape thực tế.

### 4.3 Minor (có thể fix sau)

- **[MINOR] TC-H13**: human để **trống Expected result** (row 92 gốc "Step sau friend thỏa mãn"). — Member bổ sung expected (đối chiếu TC-D10: mỗi step gửi 1 lần, không 2 luồng song song).
- **[MINOR] Regression data cũ (CL-NonF-6)**: chưa có TC riêng verify **line_user đã tồn tại TRƯỚC fix** vẫn hoạt động bình thường sau khi deploy code mới (add lại / nhắn tin lại dùng đúng bản cũ). H02 chạm một phần. — Thêm 1 regression case.
- **[MINOR] Format sync lệch cột**: phần A (TC human) là bản chuyển-thể 10 cột; tab Sheet gốc 7 cột merged-cell. Khi `/sync-tc` chỉ push phần B (delta) và cần căn cột thủ công — đã note trong file 04, nhắc lại để tránh push đè row 80–121.
- **[MINOR] File 04 chưa điền tên Tester / ngày submit** (mục "Thông tin") — placeholder `<member điền>`.

### 4.4 Nit (gợi ý)

- **[NIT]** Dữ liệu trùng **CŨ** (đã tồn tại trước fix) nằm ngoài scope fix (cần DBA dọn — `needDataRecovery`). TC không verify được phần này — đề nghị tách ticket riêng cho DBA + 1 TC xác nhận sau khi DBA gộp thì scenario không còn chạy 2 luồng.
- **[NIT]** Fix tự nhận "không có unique index ở DB → guard mức ứng dụng, không tuyệt đối 100%". Cân nhắc đề xuất Dev thêm unique index (long-term) — ngoài scope round này.
- **[NIT]** CL-Func-13: có thể tách rõ case mở link **in-app LINE** vs **trình duyệt ngoài/PC** cho từng loại link (form/booking/item) thay vì gộp — hiện D08 đại diện chung.

---

## 5. TCs đề xuất bổ sung

| TC ID gợi ý | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| TC-NEW-01 | Race `checkAddOldFriend` ⨯ follow callback — bạn cũ nhắn tin lại đúng lúc re-follow → 1 line_user | User là bạn cũ đã có line_user nhưng chưa có bot_line_user (hoặc đã xóa bạn) | 1. User nhắn tin lại cho bot (kích checkAddOldFriend).<br>2. Gần như đồng thời bấm re-follow (follow callback).<br>3. Lặp 5–10 lần.<br>4. Vào friend list. | Chỉ 1 line_user cho user; dùng đúng bản gốc; không tạo bản trùng; scenario không chạy 2 luồng | High | Boundary | F4, T2, D1 |
| TC-NEW-02 | Race `checkAddGroupFriend` — thêm member ⨯ member gửi tin đồng thời → group_line_user không trùng | Bot trong group; member mới chưa tương tác | 1. Thêm member vào group đồng thời member gửi tin ngay.<br>2. Lặp vài lần.<br>3. Kiểm tra member trong group. | Member chỉ 1 line_user / 1 line_user_group; không nhân đôi | Medium | Boundary | F5, T3, D1 |
| TC-NEW-03 | Race job⨯job — 2 follow callback cùng line_id (LINE gửi webhook follow trùng) → 1 line_user | Tài khoản LINE chưa là bạn; mô phỏng/nhờ Dev bắn 2 follow callback cùng line_id sát nhau | 1. Trigger 2 follow event cùng line_id trong cửa sổ < 500ms.<br>2. Vào friend list. | Chỉ 1 line_user; không phụ thuộc có web hay không; scenario chạy 1 luồng | High | Boundary | BUG, F3, F1 |
| TC-NEW-04 | Search friend theo tên (Elasticsearch) → bản trùng không lộ ra (D2) | User đã được dedup về 1 line_user | 1. Vào Quản lý bạn bè, search theo tên LINE của user.<br>2. Đối chiếu kết quả. | Search trả về đúng 1 kết quả; không có bản trùng "mồ côi" trong index | Medium | Regression | D2 |
| TC-NEW-05 | Regression data cũ — line_user tồn tại TRƯỚC deploy vẫn hoạt động sau fix | line_user cũ (tạo trước khi merge fix) | 1. Sau deploy, user cũ nhắn tin / add lại / nhận scenario.<br>2. Kiểm tra. | Dùng đúng line_user cũ; không tạo mới; không trùng; scenario tiếp đúng tiến trình | Medium | Regression | CL-NonF-6, F4 |

---

## 6. Spec update needed

- [x] Không cần update spec (bug fix nội bộ, không đổi business rule end-user)
- [ ] Cần update spec
- Ghi chú: không có file `02-spec-reference.md` — **Spec reference: dùng `templates/LME-SYSTEM-SPEC.md` tổng (mục Scenario/ステップ配信), không có spec riêng cho task này.**

---

## 7. Checklist đã chạy

- [x] A. Coverage — A.1 BUG có TC reproduce (D01) ✓ nhưng phụ thuộc branch (BLOCKER-1); A.2 F4/F5 thiếu chiều (MAJOR); A.3 D2 RISK; A.4 T-features OK; A.5 không orphan
- [x] B. Chất lượng từng TC — Title rõ, có keyword function/data; B.4 realistic OK; lưu ý H13 thiếu expected
- [x] C. Chất lượng bộ TC — tỷ lệ thiên Positive (do 42 human happy-path) + delta bù Negative/Boundary; không trùng lặp (delta đã tránh reuse); priority phân bổ hợp lý
- [x] D. Spec alignment — không mâu thuẫn (không có file 02)
- [x] E. Hành chính — ⚠️ thiếu tên Tester / ngày (MINOR)
- [x] F. Base checklist LME:
  - [x] **F.1 Web** — CL-Func-25 (race) ✓D01/D03/D04 · CL-Func-13 (access link) ✓D08/D09+H-web · CL-Func-11 (không xóa nhầm account) ✓H16/D04 · CL-Func-5 (double-click) ✓D03 · CL-Func-10 (cascade) ✓D02. A.2 Security N/A (không URL mới); Compatibility chạm nhẹ CL-Func-13 ✓D08
  - [x] **F.2 Job** — B.1 Job callback **áp dụng** (fix ở callback follow) ✓D01/D10; B.2 CLJ01 N/A
  - [x] **F.3 Tính năng chung** — C.2 Send message (scenario duplicate ✓D10 · friend block ✓D05/D11); C.3 Friend info chạm gián tiếp (gộp về 1 account) — member verify thủ công; C.1/C.4/C.5/C.6/C.7/C.8 N/A

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | `<verify report này, đặc biệt BLOCKER-1 branch + 5 TC đề xuất>` | |
| Tester | (đã đọc & hiểu feedback) | |
