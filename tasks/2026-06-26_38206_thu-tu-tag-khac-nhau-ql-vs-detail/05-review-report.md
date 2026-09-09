# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | `#38206 — [QL Tag] Thứ tự tag khác nhau giữa Quản lý tag (タグ管理) và màn sửa tag ở trang chi tiết friend (友だち詳細ページ)` |
| Reviewer (Leader) | `<Leader verify>` |
| Tester được review | `<member điền>` |
| Ngày review | `2026-06-27` |
| Version TCs | `v1` |
| Vòng review | `Round 1` |

> **Spec reference**: dùng `templates/LME-SYSTEM-SPEC.md` tổng — không có `02-spec-reference.md` riêng cho task này.

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — Có issue BLOCKER + nhiều MAJOR, cần fix và review lại

**Lý do ngắn gọn**: Modal **filter** (1 trong 2 bề mặt bug được báo) chỉ verify "filter chạy được" chứ KHÔNG verify **thứ tự** — gap trực tiếp trên bug. Kèm theo: dev-impact (03) thiếu F4/T4 richmenu (lệch với TCs thực tế), mục 3 trống, 01+03 chưa được tester verify auto-fill, và thứ tự tag ở các nơi hiển thị dùng chung `fetchCurrentTags()` (chat 1:1, My page, modal multi action) chưa được cover.

---

## 2. Tóm tắt cho member

Bộ TCs có **độ phủ thao tác rất tốt** trên trục dọc (sort → sort tiếp → xóa → thêm → tạo, cả folder ít/nhiều record cho cả tag, QR, richmenu) — bám sát CL-Func-4 (thao tác liên tục) và CL-Func-10 (update/delete impact). Điểm cần fix: (1) modal **filter** phải có Expected verify **đúng thứ tự** (hiện chỉ ghi "hiển thị đúng kết quả filter"), vì thứ tự trong modal filter chính là bug được báo; (2) cần verify thứ tự tag ở các nơi khác dùng chung `fetchCurrentTags()` (chat 1:1 right bar, My page tab タグ, modal multi action — C.4 Tag); (3) phối hợp Dev để vá dev-impact (thêm F4/T4 richmenu, điền mục 3 caller) và tick verify auto-fill trên file 01/03.

---

## 3. Coverage Matrix

| Impact | Loại | Priority | TCs map (suy luận) | # TC | Status |
|---|---|---|---|---|---|
| **BUG** — sort `id`→`position`, thứ tự tag detail friend khớp QL tag | Fix | — | 756 (reproduce), 757 | 2 | **RISK** — edit modal OK; **filter modal order chưa verify** |
| **F1** — `fetchCurrentTags()` (tag-mixin.js, my_page) | Function | Direct | 757–770 | 14 | **RISK** — chỉ verify trong detail friend; các nơi khác dùng chung function (chat 1:1, My page, multi action) chưa cover |
| **F2** — `ajaxTagEditModal()` (FriendlistController) | Function | Direct | 757–770 | 14 | **OK** edit modal / **RISK** filter modal (expected yếu — 769) |
| **F3** — `getFoldersByBot()` (LandingRepository) → QR | Function | Indirect | 771–783 | 13 | **RISK** — primary 771 "Not test"; 783 filter expected yếu |
| **F4** *(thiếu trong 03)* — `getRichmenuFilterFolders()` (FriendDetailRepository) → richmenu | Function | `<Dev confirm>` | 784–796 | 13 | **RISK** — scope chưa confirm; 784/790 "Not test" |
| **D** — (Dev ghi "Không có" — chỉ đổi logic sort khi đọc) | Data | — | — | — | **N/A** |
| **T1** — modal edit tag (detail friend) | Feature | High | 757–768, 770 | 13 | **OK** |
| **T2** — filter tag (detail friend) | Feature | Med | 769 | 1 | **RISK** — expected không verify thứ tự |
| **T3** — filter qr (detail friend) | Feature | Med | 771–783 | 13 | **RISK** — 783 expected không verify thứ tự |
| **T4** *(thiếu trong 03)* — filter richmenu (detail friend) | Feature | `<Dev confirm>` | 784–796 | 13 | **RISK** — 796 expected không verify thứ tự |

### ORPHAN TCs (có điều kiện)

| TC ID | Title | Lý do orphan | Hành động đề xuất |
|---|---|---|---|
| 784–796 | Nhóm richmenu | richmenu **không có trong dev-impact 03** (F1–F3 chỉ là tag+qr). Nếu Dev confirm fix **không** chạm richmenu → đây là case thừa. | **Confirm với Dev trước**: nếu richmenu in scope → bổ sung F4/T4 vào 03 (TCs hợp lệ). Nếu out scope → remove/đánh dấu regression-only. KHÔNG tự quyết. |

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| Fix shape (mục 2 dev-impact) | **Display-logic consistency fix** — đổi sort key (`id` → `position`) cho các list hiển thị trong trang detail friend. Không phải generic-catch / validation / race / migration / soft-delete. |
| Trigger space cần cover | **Tất cả list trong detail friend dùng pattern "sort by id"** + tất cả nơi hiển thị thứ tự tag dùng chung `fetchCurrentTags()`. Đã cover: tag (edit modal), qr landing, richmenu. **Chưa xác định đủ**: filter modal order (cả 3 entity), tag order ở chat 1:1 right bar / My page tab タグ / modal multi action (C.4). |
| Số trigger TCs hiện cover | edit modal: 3/3 entity (tag/qr/richmenu) ✓ — filter modal **order**: 0/3 (expected chỉ check "filter chạy") — nơi hiển thị tag khác: 0/3 |
| KH report dạng | **Symptom-only** — "並び順が違う / thứ tự khác nhau", không nêu màn nào lệch, không root cause. |
| Alternative root causes cần verify | "Thứ tự khác" có ≥2 cơ chế: (a) **sai sort key** (id vs position — Dev fix); (b) **sai sort direction** (ASC vs DESC — embedded note nhắc richmenu "sort ASC ngược list DESC"). → Expected "giống màn quản lý" bắt được cả hai **nếu** TC có assert thứ tự cụ thể (đó là lý do filter modal order là gap). |
| Anti-patterns dính | **AP-2** (symptom-only KH report), **AP-6** (mục 3 dev-impact trống). AP-1/AP-3/AP-4/AP-5 không dính rõ. |

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- `[BLOCKER] FIX-SHAPE — GAP-1` (TC 769 / 783 / 796): Modal **filter** là 1 trong **2 bề mặt bug** được báo ("modal edit tag **và** modal filter đang không hiển thị đúng thứ tự" — ghi chú Leader trong 01, row 756). Nhưng Expected của 769/783/796 chỉ ghi *"Hiển thị đúng kết quả filter ra"* → **không verify thứ tự**. Bug có thể vẫn lọt ở modal filter. — **Fix**: sửa Expected của 769 (tag) / 783 (qr) / 796 (richmenu) thành *"Thứ tự tag/QR/richmenu hiển thị trong modal filter **giống màn quản lý**; không hiển thị item đã xóa"*. Thêm precondition "folder đã sort thứ tự X ở màn quản lý".

### 4.2 Major (nên fix)

- `[MAJOR] AUTO-FILL` (file 01): `01-bug-task.md` auto-filled `2026-06-26 by /new-task` nhưng checkbox **"Tester verify auto-fill chính xác" CHƯA tick**, và Steps/Expected/Actual đang **để trống**. — Yêu cầu tester đọc lại Redmine #38206 (description + 2 attachment screenshot + journal), điền Steps/Expected/Actual và tick checkbox trước khi review có giá trị.
- `[MAJOR] AUTO-FILL` (file 03): `03-dev-impact.md` auto-filled nhưng checkbox verify **CHƯA tick**. F/D/T có thể chưa đủ (xem 2 issue dưới). — Yêu cầu tester verify với Dev rồi tick.
- `[MAJOR] AP-6 — Mục 3 dev-impact trống`: Mục 3 "Đã check các function caller" không liệt kê. Bug là pattern **"detail friend sort theo id"** → pattern này có thể tồn tại ở **list khác** trong trang detail friend mà Dev chưa fix/chưa liệt kê. — Yêu cầu Dev enumerate **đầy đủ** mọi list/modal trong 友だち詳細ページ có sort, xác nhận chỉ tag/qr/richmenu bị ảnh hưởng (hay còn friend info, template,...).
- `[MAJOR] SCOPE DISCREPANCY (richmenu)`: 03 mục 4.1 chỉ có F1–F3 (tag+qr) nhưng TCs 784–796 cover **richmenu**, và embedded assessment (Sheet row 755) nhắc **F4 `getRichmenuFilterFolders()`** + filter richmenu sort ASC ngược list DESC. — Confirm với Dev: nếu richmenu in scope → **bổ sung F4 + T4** vào 03/4.1/4.3; nếu không → 784–796 là ORPHAN (xem §3).
- `[MAJOR] GAP-2 — C.4 Tag (nơi hiển thị dùng chung)`: F1 `fetchCurrentTags()` nằm trong `my_page` mixin → khả năng cao **dùng chung** cho nhiều nơi hiển thị tag. Checklist C.4 liệt kê tag hiển thị ở: chat 1:1 right bar, My page tab タグ, modal **multi action**, CSV export, cross analysis... TCs chỉ verify thứ tự trong detail friend (edit/filter modal). — Yêu cầu thêm TC verify **thứ tự tag** ở **chat 1:1 right bar**, **My page tab タグ**, **modal multi action** có khớp màn QL tag sau fix không (regression của fetchCurrentTags).
- `[MAJOR] EXECUTION — TC primary "Not test"`: 771 (QR — primary order-check folder ít QR), 784 (richmenu — primary order-check), 790 (richmenu — folder nhiều) đang status **"Not test"**. Đây là các TC **xác nhận thứ tự cốt lõi** của QR/richmenu. — Phải execute trước khi approve; nếu richmenu out scope thì bỏ.

### 4.3 Minor (có thể fix sau)

- `[MINOR] TC 757–768 mơ hồ "check detail friend tag"`: Không nói rõ kiểm tra ở **edit modal** hay **filter modal** (hay cả hai). Vì filter modal là bề mặt bug → nên tách/ghi rõ surface trong Steps. (Liên quan BLOCKER GAP-1.)
- `[MINOR] CL-Func-2 (reload)`: Sau sort chưa có bước **reload** màn detail friend để verify thứ tự vẫn đúng. Thêm 1 bước reload vào TC primary (757/771/784).
- `[MINOR] Expected nhiều dòng trống (merged)`: 758–768, 772–782, 785–795 để Expected trống kế thừa dòng cha — chấp nhận theo format Sheet, nhưng khi tách filter-order TC nên ghi Expected tường minh.

### 4.4 Nit (gợi ý)

- `[NIT] CL-Func-1 (staff account)`: Cân nhắc 1 TC verify thứ tự tag hiển thị đúng với **account staff** (được phân quyền) ở detail friend.
- `[NIT] CL-Func-11 (multi-account)`: Tag/QR/richmenu sort là per-bot; 1 smoke TC tạo 2 bot có cùng tên tag để xác nhận thứ tự không lẫn account.

---

## 5. TCs đề xuất bổ sung

> Member copy vào `04-tc-list.md` (hoặc đẩy `/sync-review-tc`) ở round tiếp theo.

| TC ID gợi ý | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| TC-NEW-01 | Verify thứ tự **tag trong modal FILTER** ở detail friend khớp màn QL tag | Folder có ≥3 tag, đã sort thứ tự X ở màn Quản lý tag (タグ管理) | 1. Vào trang chi tiết friend → mở **modal filter** tag<br>2. Đối chiếu thứ tự tag với màn QL tag | Thứ tự tag trong modal filter **giống hệt** màn QL tag; tag đã xóa không hiển thị | High | Positive/Regression | BUG, F2, T2 |
| TC-NEW-02 | Verify thứ tự **QR/landing & richmenu trong modal FILTER** ở detail friend khớp màn list | Folder có ≥3 QR và ≥3 richmenu, đã sort thứ tự ở màn QR / richmenu | 1. Vào detail friend → mở modal filter QR, rồi modal filter richmenu<br>2. Đối chiếu thứ tự với màn list tương ứng | Thứ tự QR / richmenu trong modal filter giống màn list; item đã xóa không hiển thị | High | Positive/Regression | F3, F4(?), T3, T4(?) |
| TC-NEW-03 | Regression: thứ tự **tag ở chat 1:1 Right bar** sau fix khớp màn QL tag | Friend có gắn ≥3 tag; tag đã sort thứ tự X ở QL tag | 1. Mở chat 1:1 của friend → xem tag ở Right bar<br>2. Đối chiếu thứ tự với QL tag | Thứ tự tag ở Right bar khớp QL tag (verify `fetchCurrentTags` dùng chung không bị lệch) | Medium | Regression | F1, C.4 |
| TC-NEW-04 | Regression: thứ tự **tag ở My page tab タグ** và **modal multi action** khớp màn QL tag | Friend có ≥3 tag đã sort | 1. My page → tab タグ → xem thứ tự<br>2. Mở modal **multi action** (gắn/gỡ tag) → xem thứ tự danh sách tag | Thứ tự tag ở cả 2 nơi khớp màn QL tag | Medium | Regression | F1, C.4 |
| TC-NEW-05 | Verify thứ tự tag/QR/richmenu **giữ nguyên sau reload** detail friend | Đã sort + đang ở detail friend đúng thứ tự | 1. Sort ở màn quản lý<br>2. Vào detail friend, mở modal → reload (F5) màn | Sau reload thứ tự vẫn khớp màn quản lý (CL-Func-2) | Medium | Regression | BUG, T1 |

> **Lưu ý**: TC-NEW-02 và phạm vi richmenu (F4/T4) **phụ thuộc Dev confirm** richmenu có in scope không (xem §4.2 SCOPE DISCREPANCY). Nếu out scope → bỏ phần richmenu khỏi TC-NEW-02.

---

## 6. Spec update needed (nếu có)

- [x] Không cần update spec (fix là sửa logic sort cho khớp hành vi sẵn có của màn list — không đổi business rule).
- [ ] Cần update spec

---

## 7. Checklist đã chạy

- [x] A. Coverage — A.1 BUG (RISK filter), A.2 Function (RISK F1 lan toả), A.4 Feature (RISK filter), A.5 orphan (richmenu conditional), A.6 fix-shape ✓
- [x] B. Chất lượng từng TC — B.1 rõ ràng (filter expected yếu), B.2 atomic OK
- [x] C. Chất lượng bộ TC — phủ thao tác tốt; thiếu staff/multi-account (NIT)
- [x] D. Spec alignment — không mâu thuẫn
- [x] E. Hành chính — Tester/Version chưa điền (member fill)
- [x] F. Base checklist LME
  - [x] F.1 Checklist web — CL-Func-4 (thao tác liên tục) ✓ cover; CL-Func-10 (update/delete impact) ✓; CL-Func-2 (reload) thiếu (MINOR); CL-Func-1 (staff) thiếu (NIT); CL-Func-11 (multi-account) thiếu (NIT)
  - [x] F.2 Checklist job — N/A (fix chỉ logic đọc/sort, không chạm job)
  - [x] F.3 Các tính năng chung — **C.4 Tag**: GAP nơi hiển thị dùng chung (chat 1:1, My page, multi action) → MAJOR GAP-2; **C.8 Sort**: cover (tag/qr/richmenu)

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | | |
| Tester | (đã đọc & hiểu feedback) | |
