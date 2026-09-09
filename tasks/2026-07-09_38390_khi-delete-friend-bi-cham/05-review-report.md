# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | `#38390 — Khi delete friend bị chậm` |
| Reviewer (Leader) | `<Leader verify>` |
| Tester được review | Ngô Thúy Ngần (assignee) / TC gốc: Kim Cúc |
| Ngày review | `2026-07-09` |
| Version TCs | fetch từ Sheet (tab Testcase, dòng 143-155) |
| Vòng review | Round 1 |

> **Spec reference**: dùng `templates/LME-SYSTEM-SPEC.md` tổng (FA-013 Friend List, FA-015 Friend Information) — không có `02-spec-reference.md` riêng cho task này.
> **Nguồn file 04**: fetch read-only từ Redmine Link TCs (TC do human viết, cấu trúc phân cấp/merge cell). Reviewer suy luận Type/mapping từ Title/Steps/Expected.

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — Có issue BLOCKER, cần fix và review lại

**Lý do ngắn gọn**: Bộ TC verify rất tốt phần **tính đúng đắn cascade delete** (đủ các bảng, re-friend, xóa 1 vs hàng loạt trên 3 màn web), NHƯNG **bỏ lọt chính bug**: không TC nào tái hiện điều kiện chậm (line user có **nhiều data** ở `url_shorten_detail`) + **đo thời gian hoàn tất** → không verify được fix performance. Ngoài ra **thiếu hoàn toàn nhánh APP** (`Api deleteFriend` / FA-015 — Direct impact F4) dù fix áp cả web + app.

---

## 2. Tóm tắt cho member

Bộ TC gốc cover phần **data-correctness cực kỹ**: 3 màn web (hidden/user-block/block), cả xóa 1 friend lẫn xóa hàng loạt, check đủ các bảng cascade (`url_shorten`, `url_shorten_detail`, `form_answer_result`, `b_event_detail`, `scenario_lineuser_history`) + verify re-friend không còn ghost data — đây là điểm mạnh 👍. Tuy nhiên bug này là **bug hiệu năng**: cần bổ sung TC tái hiện đúng điều kiện chậm (friend có **rất nhiều** url_shorten_detail, bot lớn ~16.000 url) và **đo thao tác xóa hoàn tất nhanh, không load mãi** — nếu không, toàn bộ TC hiện tại chạy pass mà bug vẫn có thể còn. Đồng thời fix chạm cả **APP** (`Api deleteFriend`) nhưng chưa có TC nào cho app — bắt buộc bổ sung (test đối chiếu Web↔App, TC-14).

---

## 3. Coverage Matrix

> Suy luận mapping từ Title/Màn/Steps/Expected. TC gốc kiểm tra **đúng data bị xóa** (correctness) — tốt cho regression, nhưng **không** kiểm tra **tốc độ** (chính là bug).

| Impact | Loại | Priority | TCs map (suy luận) | # TC | Status |
|---|---|---|---|---|---|
| **BUG — xóa friend chậm** (query `whereIn('url_id',[~16.000 id])`) | Fix (performance) | — | (không TC nào seed large-data + đo thời gian) | **0** | **GAP** |
| **F1** — `updateLineUser(deleteLineUser)` — web màn hidden | Function | Direct | TC001, TC002, TC003 | 3 | OK (chỉ correctness, thiếu perf) |
| **F2** — `deleteUserBlock` — web màn user-block | Function | Direct | TC004, TC005, TC006 | 3 | OK (chỉ correctness, thiếu perf) |
| **F3** — `deleteUserBlockAction` — web xóa **hàng loạt** (regression #38473) | Function | Direct | TC001/004/007 (mass) + TC007-009 | 3+ | **RISK** — không có TC explicit case #38473 (multi-friend, friend không đứng đầu bị sót link) |
| **F4** — `Api\FriendInformationController::deleteFriend` — **APP** | Function | Direct | TC010 "my page"? (ambiguous, không rõ APP) | **0** | **GAP** |
| **D1** — cascade: `url_shorten` / `url_shorten_detail` / `DetailUrlClick` / `form_answer(_result)` / `b_event_detail` / `scenario_lineuser_history` | Data | — | TC001-TC011 (check bảng sau xóa + re-friend) | nhiều | OK — thiếu cross-account WHERE (CL-Func-11) |
| **T1** — Friend List (FA-013) — web | Feature | Medium | TC001-TC010 | nhiều | OK (regression correctness) |
| **T2** — Friend Information (FA-015) — **APP** | Feature | Medium | — | **0** | **GAP** |

### ORPHAN TCs

| TC ID | Title | Lý do | Hành động đề xuất |
|---|---|---|---|
| TC011 | check detail friend tab scenario | KHÔNG orphan — cover thêm bảng `scenario_lineuser_history` (D1). Giữ. | Giữ, map D1 |
| TC010 | Xóa friend ở my page | Ambiguous — "my page" web hay app? Nếu web thì trùng T1; nếu app thì mới cover F4/T2 | Yêu cầu member ghi rõ màn/step (xem [MAJOR] TC010) |

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| Fix shape (đọc mục 2 dev-impact) | **Performance / optimize query** (thay `whereIn` mảng 16k id → subquery semi-join; `->get()` → `pluck('id')`). Kèm khía cạnh **soft-delete cascade** (`form_answer_result.deleted_at`). |
| Trigger space cần cover | Điều kiện chậm = **line user có RẤT NHIỀU data** (bot lớn ~16.000 url_shorten, friend nhiều bản ghi `url_shorten_detail`). Cả 4 điểm: 3 web + 1 APP. Cả xóa 1 vs xóa hàng loạt (nhiều friend). |
| Số trigger TCs hiện cover | **0/1** — không TC nào seed dataset lớn + đo thời gian hoàn tất. TC hiện tại chỉ verify **data đã xóa đúng** (correctness), không verify **tốc độ** (fix). |
| KH report dạng | **Symptom + Dev đã trace root cause cụ thể** ("chậm load mãi" = symptom; Dev xác định = query 16k id). Alternative plausible: mass-delete nhiều friend vẫn chậm do **gọi LINE API per-friend** (Dev đã BỎ timeout LINE — giữ call gốc) và do load form/event (`->get()`→pluck). |
| Alternative root causes cần verify | (1) Xóa **hàng loạt nhiều friend** vẫn nhanh (không chỉ 1 friend). (2) Sau khi bỏ timeout LINE — luồng gọi LINE khi mass-delete không gây treo. |
| Anti-patterns dính | **AP-2** (symptom, đã root-cause nên nhẹ); **AP-3** (regression thiên happy-path — nhưng có check re-friend nên nhẹ); **AP-4** (chỉ có commit hash `a9beeef869`, không có PR/diff browsable → không verify được subquery đúng phạm vi cũ). AP-1/AP-5/AP-6: **không dính**. |

> ⚠️ Fix shape = performance → theo bảng fix-shape: **TC phải test với dataset lớn (≥ điều kiện repro) + verify thời gian**. Hiện **0 TC** làm điều này → nâng lên **[BLOCKER]** vì đây chính là bug root cause (không phải chỉ MAJOR smoke).

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- **[BLOCKER] FIX-SHAPE / GAP-BUG**: Không TC nào tái hiện **điều kiện chậm** (line user có nhiều `url_shorten_detail`, bot lớn ~16.000 url) và **đo thao tác xóa hoàn tất** (không load mãi). Toàn bộ TC hiện tại verify correctness với data thường → chạy pass kể cả khi bug performance vẫn còn. → Thêm **TC-NEW-01** (seed large-data + đo thời gian, cả xóa 1 & xóa hàng loạt).
- **[BLOCKER] GAP-F4/T2 (APP)**: Fix áp cả `Api\FriendInformationController::deleteFriend` (FA-015, xóa bạn trên **APP** — Direct impact) nhưng **không TC nào** cover nhánh app. GAP cho Direct function = Blocker. Kèm vi phạm **checklist-lme TC-14** (sửa spec dùng chung Web↔App bắt buộc test đối chiếu song song). → Thêm **TC-NEW-02** (xóa bạn trên app + cascade + perf).

### 4.2 Major (nên fix)

- **[MAJOR] AUTO-FILL chưa verify (01)**: `01-bug-task.md` có `Auto-filled: 2026-07-09 by /new-task` nhưng checkbox "Tester verify auto-fill chính xác" **CHƯA tick**. Bug lại có description Redmine trống (repro lấy từ note QA) → càng cần tester đọc kỹ. Yêu cầu tester verify + tick trước khi review có giá trị.
- **[MAJOR] AUTO-FILL chưa verify (03)**: `03-dev-impact.md` `Auto-filled: 2026-07-09 by /new-task`, checkbox chưa tick → F/D/T có thể chưa đủ/sai mapping. Đặc biệt file 03 có 2 báo cáo AI (bản mới sửa regression #38473) — tester cần xác nhận lấy đúng bản. Yêu cầu tick trước khi giao TC.
- **[MAJOR] SYMPTOM/REGRESSION #38473 — GAP-F3**: Fix khôi phục `whereIn` ở `deleteUserBlockAction` để dọn link các friend **không đứng đầu** khi chặn-xóa hàng loạt. TC007 (mass block-delete) chỉ check chung "data đã xóa" — chưa có TC **explicit**: xóa hàng loạt ≥3 friend, trong đó friend **không đứng đầu** có data `url_shorten_detail`, verify **TẤT CẢ** friend đều được dọn link (không sót). → **TC-NEW-03**.
- **[MAJOR] TC010 ambiguous**: "Xóa friend ở my page" không có màn/step rõ — không suy luận được là **web My page** (trùng T1) hay **app** (cover F4). Yêu cầu member ghi rõ URL/màn + steps. Nếu là web → vẫn còn GAP app (xem BLOCKER GAP-F4).

### 4.3 Minor (có thể fix sau)

- **[MINOR] CL-Func-11 (WHERE đúng account)**: Fix đổi cách query xóa → rủi ro xóa nhầm phạm vi. TC003/006/009 có check "chỉ xóa data của friend đã xóa" (tốt) nhưng chưa có case **2 bot / 2 account cùng data** → verify xóa friend bot A không đụng data bot B. → **TC-NEW-04**.
- **[MINOR] AP-4 — thiếu PR/diff**: Mục "Commit/PR" chỉ có commit hash `a9beeef869`, không có link PR/diff browsable → reviewer không verify được subquery có giữ **đúng phạm vi cũ** (Dev tự nhận `url_shorten.bot_id` không tin cậy nên lọc qua url_id-thuộc-bot). Yêu cầu Dev cung cấp link diff nếu cần verify sâu.
- **[MINOR] Format 04**: TC gốc thiếu cột **Type / Priority** (fetch từ sheet human khác cấu trúc). Khi member đưa vào review chuẩn nên bổ sung Type (Regression/Boundary) + Priority để Leader đánh giá tỷ lệ chiều.

### 4.4 Nit (gợi ý)

- **[NIT] TC-11 (load test)**: checklist-lme A.1+ TC-11 khuyến nghị chức năng cải thiện hiệu năng nên thêm quan điểm **load test / truy cập tập trung** (k6/Gatling) — optional, có thể để smoke đo thời gian là đủ cho round này.
- **[NIT]** TC gốc dùng merge-cell nên TC002/005/008 (check re-friend) và TC003/006/009 (xóa 1) hơi khó đọc rời — khi tách sang file review chuẩn nên đặt TC ID độc lập + precondition đầy đủ mỗi dòng.

---

## 5. TCs đề xuất bổ sung

> Member copy vào `04-tc-list.md` ở round tiếp theo.

| TC ID gợi ý | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| TC-NEW-01 | Xóa friend có **nhiều data** hoàn tất nhanh (verify fix performance) — web | Bot lớn (~16.000 `url_shorten`); 1 line user có **nhiều bản ghi** `url_shorten_detail` (vài nghìn) + có form_answer + b_event_detail; env Staging/Dev | 1. Vào `/basic/friendlist/hidden`<br>2. Chọn friend nhiều data → nhấn Xóa<br>3. Bấm giờ từ lúc click Xóa đến khi màn phản hồi<br>4. Lặp với **xóa hàng loạt** nhiều friend nhiều data | - Thao tác xóa hoàn tất trong thời gian hợp lý (không "load mãi"); so sánh trước/sau fix nếu có<br>- Không timeout/treo màn<br>- Data ở các bảng cascade đã xóa đúng | High | Boundary (perf) | **BUG**, F1, F3, D1 |
| TC-NEW-02 | Xóa bạn trên **APP** (`Api deleteFriend`, FA-015) — cascade + tốc độ | Tài khoản app admin; line user có nhiều data (như TC-NEW-01) | 1. Mở app mobile → màn xóa bạn (my page / friend)<br>2. Thực hiện xóa bạn<br>3. Đo thời gian + check DB các bảng cascade | - Xóa hoàn tất nhanh, không treo<br>- Cascade data xóa đúng như web<br>- **Đối chiếu song song Web↔App** cùng kịch bản (TC-14) khớp nhau | High | Regression + Boundary | **F4**, **T2**, BUG |
| TC-NEW-03 | Chặn-xóa **hàng loạt** dọn link đủ mọi friend (regression #38473) | Màn block; ≥3 friend, trong đó friend **không đứng đầu** danh sách có data `url_shorten` + `url_shorten_detail` + `DetailUrlClick` | 1. Vào `/basic/friendlist/block`<br>2. Chọn all (≥3 friend) → xóa hàng loạt<br>3. Check DB link của **từng** friend (đặc biệt friend không đứng đầu) | - `url_shorten` / `url_shorten_detail` / `DetailUrlClick` của **TẤT CẢ** friend đã xóa được dọn sạch — không friend nào bị **sót link** | High | Regression | **F3**, D1 |
| TC-NEW-04 | Xóa friend không đụng data account/bot khác (WHERE đúng — CL-Func-11) | 2 bot (A, B), mỗi bot có friend với data trùng dạng ở `url_shorten`/`url_shorten_detail` | 1. Xóa friend ở bot A<br>2. Check DB data friend tương ứng ở bot B | - Chỉ data friend bot A bị xóa<br>- Data bot B **nguyên vẹn** | Medium | Negative | D1, F1-F4 |
| TC-NEW-05 | Mass-delete nhiều friend không treo do LINE API (đã bỏ timeout) | Nhiều friend; theo dõi luồng gọi LINE | 1. Xóa hàng loạt nhiều friend<br>2. Quan sát thời gian + log gọi LINE (unfollow set is_blocked) | - Không treo do chờ LINE; thao tác hoàn tất; không mất data<br>- (checklist-lme TC-10/TC-12 hệ bất thường) | Medium | Boundary | BUG, T1 |

---

## 6. Spec update needed

- [x] Không cần update spec — fix là tối ưu query, **không đổi behavior** xóa (tập bản ghi bị xóa giữ nguyên). Không mâu thuẫn FA-013/FA-015.

---

## 7. Checklist đã chạy

- [x] A. Coverage — GAP ở BUG(perf), F4, T2; RISK ở F3
- [x] B. Chất lượng từng TC — TC010 ambiguous; thiếu Type/Priority
- [x] C. Chất lượng bộ TC — mạnh về correctness, thiếu chiều performance + cross-platform
- [x] D. Spec alignment — không mâu thuẫn (không có 02, dùng SPEC tổng)
- [x] E. Hành chính — auto-fill 01/03 chưa tick verify (MAJOR)
- [x] F. Base checklist LME
  - [x] F.1 web: CL-Func-10 (update/delete impact) ✓ cover tốt; CL-Func-11 (WHERE account) — thiếu cross-account (MINOR); TC-11 load test (NIT)
  - [x] F.2 job: không chạm Google sync / callback → N/A (Dev xác nhận job linect không dính)
  - [x] F.3 chung: **TC-14 Web↔App** — vi phạm (thiếu app, BLOCKER); C.3 Friend info xóa — cover web tốt

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | `<verify>` | |
| Tester | (đã đọc & hiểu feedback) | |
