# 05 — Review Report

> Draft cho Leader verify. Bug ID + ngày nằm ở tên folder; vòng review nằm ở tên file.

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | **(1) MCP LME TEST STUDIO — task `#198`** |
| Vì sao không dùng nguồn ưu tiên cao hơn | `N.A. — đã dùng nguồn 1` |
| Ticket · task_id · round · branch | `34051` · `#198` · round `1` · `ai_fixbug_33350` |
| Thời điểm fetch | `2026-09-05` (`task_list` → `testcase_list` → `task_get_context` → `task_get_report` → `review_list_comments`) |
| Tổng số TC review | **12** (`totalMatched = 12`, `nextCursor = null`) |
| Snapshot đã ghi | `04-tc-list.md` — **không refresh**: file đã mang header `<!-- source: MCP LME TEST STUDIO — task_id=198 ... -->` do `/new-task` sinh cùng session, cùng nguồn, cùng đúng 12 TC |
| Đối chiếu chéo nguồn | `KHÔNG — đã dừng ở nguồn 1` |
| Tester được review | `AI pipeline (Studio job 582)` — 9/12 TC · `haodtb` (qua MCP) — 3/12 TC |
| Vòng review | `Round 1` (Studio `reviewState = leader`, `reviewed = false`, `review_list_comments` = rỗng → **chưa có vòng review nào trước đó**) |
| **Nguồn spec đã dùng** | [`spec-features/admin/form-answer/feature-spec.md`](../../spec-features/admin/form-answer/feature-spec.md) — **FA-011「フォーム作成」**: `SCR-FA11-09` Trang kết quả trả lời (EP-14/EP-15/EP-42), `BR-09` Phiên bản UI `using_old_version`, `BR-06` Backup lock, ER `form_answer_result ||--o{ form_answer_item_remind`. Tra mã màn hình qua [`templates/LME-SYSTEM-SPEC.md`](../../templates/LME-SYSTEM-SPEC.md) dòng 687 (FA-011) + 695 (FA-022「リマインド配信」). |

> ⚠️ Studio gán `feature = "shop-card"` cho task #198, nhưng task thuộc **FA-011 / FA-022 (form-answer)** — xem `[MINOR] M-05`.

**Cảnh báo bắt buộc về chất lượng nguồn** — *Nguồn 1 (Studio)*:

| # | Chiều | Kết quả | Flag |
|---|---|---|---|
| 1 | Kết quả thực thi thật (`pass` mới là Đạt) | **11/12 pass (91.7%)** · 1 `skip` (TC-DEPLOYASSET001-01) · 0 fail · 0 error | `OK` về tỷ lệ — **nhưng 100% số pass đó chỉ ở env `local`** (xem #3) |
| 2 | TC `fail`/`error` + TC gắn ticket bug | **0 TC fail · 0 TC error · `bugs.total = 0`** — không TC nào gắn ticket. **NHƯNG ở tầng RUN**: run `#888` (env `staging`) = **`error`** (2026-09-05 02:07→02:18), run `#904` (env `staging`) đang **`running`** từ 2026-09-05 03:59 → **chưa từng có một run staging nào hoàn tất** | `[MAJOR] B-05` |
| 3 | Môi trường đã chạy — RULE-08 / ENV-003 | **PROD 0 · STAGING 0 run hoàn tất (1 error + 1 đang chạy) · LOCAL 3 run** (`#456`, `#488`, `#846`). Manual: 3 lần **skip** TC-DEPLOYASSET001-01 (2× local, 1× staging). Task chạm **asset JS** + **job nền gửi remind** | `[BLOCKER] B-02` |
| 4 | Ai chạy (`last_exec.source` / `by`) | **11/11 pass đều `source = "ai"`** → do **pipeline AI** chạy (`by` = `haodtb` / `quyend` chỉ là người bấm run). Người thật chỉ thao tác 3 lần và đều là **skip**. `submittedWithoutMcp = false` | `[MAJOR] M-01` |
| 5 | Tác giả TC (`provenance.source`) | **9/12 (75%) do AI sinh** (`actor=AI`, `created_job_id=582`) · 3/12 do người viết (`haodtb@mcp`: NEW-11/12/13). `reviewState = leader` — **chưa `done`** | `[MAJOR] M-02` |
| 6 | Mã quan điểm KHÔNG có trong `checklist-lme.md` | **2 mã / 2 lượt TC**: `TOOL-KNOW-002` (TC-TOOLKNOW002-01 — chính là TC tái hiện bug) · `TOOL-ERRHYG-001` (TC-TOOLERRHYG001-01) | `[MAJOR] M-03` |

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — Có issue BLOCKER, cần fix và review lại

**Lý do ngắn gọn**: 4 BLOCKER — (1) Dev **không cung cấp danh sách 8 caller** của hàm dùng chung `initData` nên REG-SHARED-001 không thể kết luận, và evidence 3 TC tự đếm ra 3 con số khác nhau; (2) TC cho **DEPLOY-ASSET-001 bị skip 3 lần, chưa từng chạy** trong khi Dev cố ý không bump version asset; (3) **GAP COMPAT-LEGACY-001** — form đời cũ (`using_old_version=1`) có item remind chưa được rà; (4) **GAP CONC-001** — chính bản fix tạo ra rủi ro mới (popup giữ mở → nút 配信停止 còn bấm được trong lúc reload).

---

## 2. Tóm tắt cho member

Bộ 12 TC bám rất sát root cause và **chất lượng evidence thuộc nhóm tốt nhất từng thấy**: `actual` của mỗi TC ghi giá trị đo được thật (đối chiếu `deleted_at` + `user_deleted` DB với 操作日時 trên UI, `current_page=2`, tên bản ghi `SF34051-RECORDB`), TC NEW-12/NEW-13 do người viết bổ sung đúng chỗ AI còn hở, và TC NEW-12 còn phát hiện được `changePaginate` là **dead code** — đó là phát hiện có giá trị hơn cả việc pass.

Ba việc phải xử lý trước khi approve: **(a)** bộ TC mới chỉ chứng minh được fix đúng **trên `local`** — mà bản chất bug này là một file JS được thay mà **không bump version asset**, nên TC quan trọng nhất (`TC-DEPLOYASSET001-01`) lại đúng là TC bị skip 3 lần; **(b)** con số caller của `initData` không khớp giữa Dev (8) và evidence TC (6 + 4) — cần Dev chốt danh sách chính thức thì REG-SHARED-001 mới có nghĩa; **(c)** 0/12 TC là `Boundary` và chưa có TC nào cho luồng **hủy hộp thoại xác nhận** hay **bấm 配信停止 hai lần**, trong khi fix đã làm popup ở lại màn hình — tức nút đó bây giờ vẫn nằm dưới tay người dùng trong lúc danh sách đang reload.

---

## 3. Coverage Matrix

| Impact | Loại | TC cover (suy luận) | # TC | Exec | Status |
|---|---|---|---|---|---|
| **BUG** (root cause — nhánh success của stop remind xóa `preview_item` + đóng popup) | Fix | TC-TOOLKNOW002-01, TC-DATAID001-01, TC-TOOLERRHYG001-01 | 3 | 3/3 | **OK** (chỉ `local`) |
| **F1** — `stopItemRemind` + `confirmStopItemRemind` (nhánh success) | Function | TC-TOOLKNOW002-01, TC-OUTTRUTH001-01, TC-TOOLERRHYG001-01, TC-DATA001-02 | 4 | 4/4 | **RISK** — thiếu: hủy hộp thoại xác nhận · double-click · branch guard "không tìm thấy bản ghi" |
| **F2** — `initData` (thêm optional callback) — **hàm dùng chung, 8 caller cũ** | Function | TC-REGSHARED001-01, TC-REGSHARED001-02, TC-DATA001-01 | 3 | 3/3 | **RISK** — không có danh sách caller chính thức; evidence đếm 6 / 4 / (Dev nói 8) |
| **F3** — `removeFormResult` (xóa câu trả lời) | Function | TC-REGSHARED001-03 | 1 | 1/1 | **RISK** — không verify **số người trả lời giảm** (kho `TC-FORM-351` có) |
| **F4** — `showModalInfo` / `hideModalInfo` | Function | TC-REGSHARED001-04 | 1 | 1/1 | **OK** |
| **F5** — `FormAnswerController::stopItemRemind` (không sửa) | Function | TC-TOOLERRHYG001-01 | 1 | 1/1 | **RISK** — chỉ chạy 1 trigger lỗi (5xx), bỏ nhánh backup guard `BR-06` |
| **F6** — `showFormResultV3` — `dataRemind` `withTrashed` (không sửa) | Function | TC-OUTTRUTH001-01, TC-DATA001-02 | 2 | 2/2 | **OK** |
| **F7** — `FormAnswerService::stopItemRemind` (không sửa) | Function | (gián tiếp qua F5) | 1 | 1/1 | **OK** — tầng service không bị chạm |
| **F8** — View `remind-box` + modal chi tiết (không sửa) | Function | TC-TOOLKNOW002-01, TC-OUTTRUTH001-01 | 2 | 2/2 | **OK** |
| **F9** — `stopRemind` màn chi tiết bạn bè `my_page.js` | Function | — | **0** | — | *Ngoài phạm vi* — Dev khai thiết kế khác, không đụng code (**AP-5**: không đề xuất TC) |
| **D1** — `FormAnswerItemRemind.deleted_at` + `user_deleted` (READ, `withTrashed`) | Data | TC-OUTTRUTH001-01, TC-DATA001-02 | 2 | 2/2 | **OK** — evidence có đối chiếu DB thật (`user_deleted=773`, `deleted_at=2026/09/04 12:25`) |
| **D2** — asset `public/js/form_answer/form_result_v3.js` (KHÔNG bump version) | Data | TC-DEPLOYASSET001-01 | 1 | **0/1** | **RISK → thực chất GAP** (skip 3 lần) |
| **T1** — Form Answer Result — Reminder Delete (FA-011 / FA-022) — **High** | Feature | TC-TOOLKNOW002-01, TC-OUTTRUTH001-01, TC-TOOLERRHYG001-01, TC-DATA001-02 | 4 | 4/4 | **RISK** — 0 Boundary; chưa rà nhánh form đời cũ |
| **T2** — Phân trang / số dòng / sort / lọc ngày / đổi tab (8 caller `initData`) — Medium–High | Feature | TC-REGSHARED001-01, TC-REGSHARED001-02, TC-DATA001-01 | 3 | 3/3 | **RISK** — chỉ test từng caller **riêng lẻ**, chưa test **chuỗi thao tác sau khi stop remind** (FUNC-SEQ-001) |
| **T3** — Xóa câu trả lời trong popup (phải vẫn đóng popup) — Medium | Feature | TC-REGSHARED001-03 | 1 | 1/1 | **RISK** — 1 TC, precondition data sạch (**AP-3**) |
| **T4** — Nút đóng popup + đổi tab danh sách — Medium | Feature | TC-REGSHARED001-04 | 1 | 1/1 | **OK** |
| **T5** — Deploy / cache asset JS — Medium | Feature | TC-DEPLOYASSET001-01 | 1 | **0/1** | **RISK → thực chất GAP** |
| **T6** — Màn chi tiết bạn bè (`my_page.js`) — Low | Feature | — | **0** | — | *Ngoài phạm vi* (**AP-5**) |

### ORPHAN TCs

| TC ID | Title | Lý do orphan | Hành động đề xuất |
|---|---|---|---|
| — | — | Không có TC lạc chủ đề — cả 12 TC đều trace được về code path Dev đã sửa hoặc về 3 luồng đóng popup hợp lệ | Giữ nguyên |

> Bộ TC này **không dính AP-5** (over-coverage tầng dưới): không TC nào đi test service/DB layer hay luồng gửi tin thực tế — đúng với việc fix chỉ chạm JS.

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| Fix shape (đọc mục 2 dev-impact) | **Kết hợp 2 shape**: ① **"sửa hàm dùng chung"** (`initData` + optional callback — `共通`/shared) → REG-SHARED-001 · ② **"JS / asset"** (sửa `form_result_v3.js`, **KHÔNG bump** `config/sns-line.php`) → DEPLOY-ASSET-001 |
| Trigger space cần cover | ① **8 caller cũ của `initData`** (Dev khai số lượng, **không khai tên**) · ② Browser còn cache bản JS trước fix, chỉ **F5 thường** |
| Số trigger TCs hiện cover | ① **6 caller** (TC-REGSHARED001-01: `changePage`, `changeLimit`, `sort`, `全期間 reset`, `changePanel` — evidence ghi "6 caller" nhưng chỉ liệt kê **5** thao tác) **+ 4 caller** (TC-REGSHARED001-02: `created()`, `daterangepicker`, `removeFormResult`, `changePaginate`) — trong đó `changePaginate` **KHÔNG có binding trong blade ⇒ dead code, không chạy được**. → tổng tên caller đếm được = **9–10**, Dev khai **8** → **không khớp, không thể kết luận đã phủ đủ** · ② **0/1** (TC tồn tại nhưng skip 3 lần) |
| KH report dạng | **Symptom-only** — description Redmine đúng **1 dòng** `Exp:`, không có Steps / Actual / môi trường / ảnh; Actual phải suy từ *subject* |
| Alternative root causes cần verify | (a) KH dùng **form đời cũ** (`using_old_version=1`, BR-09) — màn kết quả bản cũ không dùng `form_result_v3.js`, có thể là màn khác hẳn; (b) request `stop-item-remind` lỗi/timeout (session hết hạn, backup guard BR-06) khiến popup đóng vì nhánh khác; (c) browser giữ bản JS cũ sau một release trước đó |
| Anti-patterns dính | **AP-2** (symptom-only) · **AP-3** (happy-path-only regression ở T2/T3) · **AP-4** (không có PR link, chỉ có commit hash `6daa778302`) · **AP-6 biến thể** (mục 3 có list function nhưng **không list 8 caller** của `initData` — đúng chỗ cần nhất) |

**Câu hỏi adversarial còn treo — Dev phải trả lời trước vòng 2:**

1. **Liệt kê đích danh 8 caller** của `initData` trong `form_result_v3.js` (tên hàm + dòng). `changePaginate` là dead code thật hay còn binding ở nơi khác?
2. Nhánh `success` mới **có disable / ẩn nút 配信停止** trong lúc chờ reload không? Nếu không → bấm lần 2 sẽ gửi request `stop-item-remind` thứ hai.
3. Guard "kiểm tra tìm thấy mới gán" (Dev tự nêu ở TỰ REVIEW) hành xử ra sao khi **không tìm thấy** bản ghi sau reload — popup giữ dữ liệu cũ và **vẫn hiện trạng thái "đã dừng"** hay hiện dữ liệu cũ chưa dừng?
4. Cơ chế cache-busting asset của hệ thống là gì nếu **không** bump `sns-line.version` (hash tự sinh khi build? header cache-control?) — đây là điều kiện tiên quyết để đóng `REQ-008`.
5. Màn kết quả của **form đời cũ** có nút dừng remind không, và nếu có thì dùng file JS nào?

---

## 3.6 Bảng quan điểm đối chiếu

| Mã quan điểm | Ưu tiên | Trigger khớp task? | TC cover (suy luận) | Exec | Kết luận |
|---|---|---|---|---|---|
| `FUNC-001` | Cao | ◯ mọi chức năng | TC-TOOLKNOW002-01 *(mang mã Studio lạ)* | 1/1 | **GAP theo 0.6#6** — nội dung ĐÃ test, chỉ là mã quan điểm không map được → `[MAJOR] M-03` |
| `FUNC-SEQ-001` ★ | Trung bình (**BẮT BUỘC** — màn có ≥2 thao tác trên cùng danh sách + **Sort**) | ◯ | — | — | **GAP** → `[MAJOR] M-08` |
| `CONC-001` | **Cao** | ◯ nút thực thi hành động quan trọng (dừng gửi tin, soft-delete không hoàn tác) | — | — | **GAP** → `[BLOCKER] B-04` |
| `CONC-003` ★ | Trung bình → **Cao** (màn có phân trang + filter) | ◯ | TC-CONC003-01 | 1/1 | **RISK** — evidence ghi `openedB=false`: LoadingOverlay chặn đổi selection ⇒ **nhánh race chính không chạy được**, TC pass nhưng chưa chứng minh được điều nó định chứng minh |
| `DATA-001` | Cao | ◯ cập nhật dữ liệu được tham chiếu nơi khác | TC-DATA001-01, TC-DATA001-02 | 2/2 | **RISK** — thiếu Boundary (RULE-01) |
| `DATA-ID-001` | Trung bình → **Cao** (màn chọn đối tượng để thao tác) | ◯ | TC-DATAID001-01 | 1/1 | **RISK** — TC dùng 2 bản ghi **khác biệt rõ ràng** (`SF34051-RECORDB`), **không** test 2 bản ghi **trùng tên hiển thị** = đúng trigger của quan điểm → `[MAJOR] M-09` |
| `DATA-COUNT-001` | Cao | ◯ màn có số đếm (tổng bản ghi, 回答者数) | — | — | **GAP** → `[MAJOR] M-10` *(hạ từ BLOCKER — xem ghi chú ①)* |
| `DATA-DB-001` ★ | Cao | ◯ soft-delete (`deleted_at`) | TC-OUTTRUTH001-01, TC-DATA001-02 | 2/2 | **RISK** — có đối chiếu DB thật nhưng thiếu WHERE-scope 2 bot/2 tài khoản → `[MAJOR] M-11` *(hạ từ BLOCKER — xem ghi chú ②)* |
| `DATA-CACHE-001` | Trung bình → **Cao** (release đổi JS) | ◯ | TC-DEPLOYASSET001-01 (một phần) | **0/1** | **GAP** cho kịch bản (1) "tab mở sẵn **trước** deploy, không refresh, thao tác tiếp" → `[MAJOR] M-12` |
| `DATA-AUDIT-001` | Cao | ◯ hiển thị ai dừng + khi nào | TC-OUTTRUTH001-01, TC-DATA001-02 | 2/2 | **OK** — evidence khớp 3 tầng (DB `user_deleted` ↔ username UI ↔ 操作日時) |
| `OUT-TRUTH-001` | Cao | ◯ thao tác có thông báo kết quả | TC-OUTTRUTH001-01 | 1/1 | **RISK** — chỉ `Normal`, thiếu Abnormal + Boundary (RULE-01) |
| `UI-003` | Trung bình → **Cao** (rủi ro false success) | ◯ màn danh sách / xử lý bất đồng bộ | TC-TOOLERRHYG001-01 | 1/1 | **RISK** — có nhánh lỗi, thiếu trạng thái **rỗng** + **mạng chậm** ở tab リマインド → `[MAJOR] M-13` |
| `LIST-001` | Trung bình | ◯ màn danh sách có filter/pagination | TC-REGSHARED001-01, -02, TC-DATA001-01 | 3/3 | **OK** |
| `REG-SHARED-001` | **Cao** | ◯ sửa **hàm dùng chung** `initData` | TC-REGSHARED001-01 → -04 | 4/4 | **RISK → không kết luận được** — thiếu **danh sách nơi ảnh hưởng do Dev cung cấp** (điều kiện bắt buộc của quan điểm) → `[BLOCKER] B-01` |
| `REG-RUN-001` | Cao | ◯ release khi có dữ liệu/job đang chạy dở (remind đã lên lịch, admin đang mở màn) | TC-DEPLOYASSET001-01 (một phần) | **0/1** | **RISK** — gộp xử lý cùng `DATA-CACHE-001` / `M-12` |
| `DEPLOY-ASSET-001` ★ | **Cao** | ◯ release sửa file JS | TC-DEPLOYASSET001-01 | **0/1 (skip ×3)** | **GAP thực chất** → `[BLOCKER] B-02` |
| `ENV-003` ★ | **Cao** | ◯ chạm asset JS + job nền gửi remind | TC-DEPLOYASSET001-01 | **0/1** | **GAP thực chất** — 0 run production, 0 run staging hoàn tất → `[BLOCKER] B-02` (RULE-08) |
| `COMPAT-LEGACY-001` ★ | **Cao** | ◯ chạm **form** + **remind** — RULE-09 nêu đích danh cặp "remind cũ ⇄ remind mới (salon/lesson/**form**)"; `BR-09` xác nhận tồn tại `using_old_version=1`; kho `TC-FORM-176` xác nhận **form CŨ có item remind** | — | — | **GAP** → `[BLOCKER] B-03` |
| `PERM-002` | Cao | ◯ trên giấy (thao tác xóa/dừng gửi tin) | — | — | **Không đề xuất TC** — tầng phân quyền (`basic_access`) không bị chạm code (**AP-5**) → `[NIT] N-01` |
| `MSG-002` / `STATE-DEP-001` | Cao | ◯ trên giấy (remind = gửi tin theo lịch, chạy qua job nền) | — | — | **Không đề xuất TC** — fix là UI-only, tầng job/gửi tin không bị chạm (**AP-5** + nguyên tắc root-cause-layer). Ghi lại để Leader tự quyết nếu muốn phủ RULE-06 |

**Ghi chú hạ severity (nêu rõ để Leader override được):**

- **①  `DATA-COUNT-001`** — luật ở BƯỚC 3 là "quan điểm Cao + GAP → `[BLOCKER]`". Hạ xuống `[MAJOR]` vì con số đếm được render **bên trong chính `initData`** — đường đi đã được TC-REGSHARED001-01/-02 verify (`per=50`, `rows=50`, `11 dòng`, `10 dòng`). Rủi ro còn lại chỉ là số đếm bị reset/nháy **sau riêng luồng stop remind**, chưa ai kiểm.
- **②  `DATA-DB-001`** — luật là "UPDATE/DELETE mà không có TC kiểm WHERE scope trên 2 tài khoản → `[BLOCKER]`". Hạ xuống `[MAJOR]` vì câu `WHERE` nằm ở `FormAnswerService::stopItemRemind` — **không bị fix chạm** (fix chỉ đổi JS), và TC-OUTTRUTH001-01 / TC-DATA001-02 đã đối chiếu DB thật ở tầng bản ghi.

**Tổng kết**: 20 quan điểm ◯ · **4 GAP mức Cao** (`CONC-001`, `DEPLOY-ASSET-001`, `ENV-003`, `COMPAT-LEGACY-001`) → 4 BLOCKER · 8 RISK · 4 OK · 3 chủ động không đề xuất TC (AP-5).

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- **`[BLOCKER] B-01` FIX-SHAPE + [AP-6] — GAP-1 / REG-SHARED-001**: mục 2 dev-impact khai `initData` là hàm dùng chung có **"8 chỗ gọi cũ"** nhưng **không liệt kê tên caller nào**; quan điểm `REG-SHARED-001` yêu cầu **danh sách nơi ảnh hưởng do dev cung cấp** làm điều kiện tiên quyết. Ba nguồn đang mâu thuẫn: Dev nói **8**, evidence TC-REGSHARED001-01 nói **"6 caller"** nhưng chỉ liệt kê **5** thao tác, TC-REGSHARED001-02 liệt kê thêm **4** (một trong đó — `changePaginate` — là **dead code không có binding**). Không thể kết luận đã phủ hết. — **Fix**: yêu cầu Dev đưa danh sách 8 caller (tên hàm + dòng trong `form_result_v3.js`), rồi cập nhật `Điều kiện tiền đề` + `Dữ liệu nhập` của TC-REGSHARED001-02 bằng danh sách đó thay cho câu "các caller còn thiếu"; xác nhận riêng tình trạng `changePaginate`.
- **`[BLOCKER] B-02` — GAP-2 / DEPLOY-ASSET-001 + ENV-003 (RULE-08)**: `TC-DEPLOYASSET001-01` là TC **duy nhất** cover rủi ro lớn nhất của bản fix này (thay file JS mà **cố ý không bump** `config/sns-line.php`) nhưng đã bị **skip 3 lần**: `local` 2026-09-04 07:10 (lý do `"API"`), `local` 2026-09-04 07:17 (`"K test trên local"`), **`staging` 2026-09-05 02:08 (`"API"`)**. Toàn task: **0 run production, 0 run staging hoàn tất** (run `#888` = `error`, run `#904` đang chạy). Theo `ENV-003`/RULE-08, asset + job nền **không được kết luận từ local**. — **Fix**: chạy thật TC-DEPLOYASSET001-01 trên `staging` rồi `production` theo đúng 6 bước của `DEPLOY-ASSET-001` (mở màn bằng bản cũ để cache → deploy → **chỉ F5 thường** → DevTools Network: JS trả 200 kèm query version mới, không 404); đính screenshot Network + screenshot sau F5. Nếu vẫn không chạy được, phải có phiếu xác nhận + phương án giám sát (Evidence của ENV-003), **không đóng bằng `skip`**.
- **`[BLOCKER] B-03` — GAP-3 / COMPAT-LEGACY-001 (RULE-09)**: fix chỉ nằm trong `form_result_v3.js` — **nhánh V3**. Spec `BR-09` xác nhận tồn tại `using_old_version=1` (UI cũ), và kho TCs xác nhận **form đời cũ CÓ item remind** (`TC-FORM-176`: *"Item remind của form CŨ: hiển thị được data cũ, KHÔNG cho edit, chỉ cho xóa"*). RULE-09 + `COMPAT-LEGACY-001` nêu đích danh cặp **"remind cũ ⇄ remind mới (salon / lesson / form)"**. Không TC nào chạm nhánh cũ, và mục 2 dev-impact quét ngang cũng chỉ quét **trong cùng màn V3** + `my_page.js`. Đây cũng là **alternative root cause** của bug (KH có thể đang dùng form cũ). — **Fix**: thêm TC-COMPATLEGACY001-01/-02 ở §5; đồng thời hỏi Dev màn kết quả của form đời cũ dùng file JS nào và có nút dừng remind không.
- **`[BLOCKER] B-04` — GAP-4 / CONC-001**: **chính bản fix tạo ra rủi ro mới**. Trước fix, sau khi dừng remind popup **đóng ngay** → không còn nút để bấm. Sau fix, popup **ở lại** và danh sách reload bất đồng bộ → nút 「配信停止」 vẫn nằm dưới tay người dùng trong khoảng thời gian chờ. `CONC-001` (Cao) yêu cầu 4 kịch bản; hiện **0 TC**. TC-CONC003-01 chỉ chạm race tầng client và evidence cho thấy nhánh chính của nó (`openedB=false`) **không chạy được**. — **Fix**: thêm TC-CONC001-01/-02/-03 ở §5; hỏi Dev nhánh success mới có disable/ẩn nút trong lúc chờ reload không.

### 4.2 Major (nên fix)

- **`[MAJOR] M-01` (0.6 #4)** — 11/11 kết quả `pass` đều có `last_exec.source = "ai"`: do **pipeline AI tự chạy tự chấm**, không phải QA người verify. Người thật chỉ thao tác 3 lần, cả 3 đều là **skip**. Nhóm rủi ro cao nhất (`REG-SHARED-001`, `DEPLOY-ASSET-001`) rơi trọn vào diện này. — **Fix**: QA người chạy lại ít nhất TC-TOOLKNOW002-01, TC-REGSHARED001-01/-02 và TC-DEPLOYASSET001-01, đính evidence tay.
- **`[MAJOR] M-02` (0.6 #5)** — **9/12 (75%) TC do AI sinh** (`created_job_id=582`) trong khi `reviewState = leader`, `reviewed = false`, `review_list_comments` rỗng → chưa ai review nội dung TC. — **Fix**: report này chính là vòng review đó; sau khi xử lý BLOCKER, chuyển `reviewState` sang `done`.
- **`[MAJOR] M-03` (0.6 #6)** — 2 mã quan điểm **không tồn tại** trong `framework/checklist-lme.md`: `TOOL-KNOW-002` và `TOOL-ERRHYG-001` (nhóm `TOOL-*` là mã nội bộ Studio). Nghiêm trọng ở chỗ `TOOL-KNOW-002` được gán cho **TC tái hiện bug chính**. Theo BƯỚC 0.6#6 các mã này **không được tính là cover** → `FUNC-001` thành GAP trên giấy dù nội dung đã test. — **Fix**: `testcase_update` gán lại `viewpoint`: `TOOL-KNOW-002` → **`FUNC-001`**, `TOOL-ERRHYG-001` → **`UI-003`** (hoặc `OUT-TRUTH-001`).
- **`[MAJOR] M-04`** — `01-bug-task.md` và `03-dev-impact.md` đều mang `Auto-filled: 2026-09-04 by /new-task` nhưng checkbox **"Tester verify auto-fill chính xác" CHƯA tick** ở cả hai file. F/D/T có thể thiếu hoặc map sai → coverage matrix ở §3 chỉ đáng tin sau khi tester xác nhận. — **Fix**: tester đọc lại Redmine #34051 (description + journal AI Auto-fixbug) rồi tick 2 checkbox.
- **`[MAJOR] M-05` (0.6 #2)** — ở tầng RUN: run `#888` env `staging` kết thúc **`error`** sau 11 phút (không có `counts`), run `#904` env `staging` vẫn `running` từ 03:59. Nghĩa là **chưa từng có một run staging nào hoàn tất**, và lỗi run chưa được raise thành ticket hay ghi nhận ở đâu. — **Fix**: điều tra `stageError` của run #888, đợi/kiểm tra kết quả run #904 rồi bổ sung vào report vòng 2.
- **`[MAJOR] M-06` [AP-2] SYMPTOM-ONLY** — description Redmine đúng **1 dòng** `Exp:`, không có Steps / Actual / môi trường / ảnh; "Actual result" ở file 01 phải suy từ *subject*. Dev xác định root cause **chỉ bằng đọc mã** và tự ghi *"Không tái hiện trên dev qua giao diện"*, verify dừng ở mức **`lint`**. Một triệu chứng "popup bị đóng" có ≥ 3 root cause hợp lý (xem §3.5). — **Fix**: hỏi lại KH/PM môi trường + loại form (V3 hay đời cũ) + có tái hiện lại được sau khi deploy fix không.
- **`[MAJOR] M-07` [AP-4]** — mục "Commit / Pull Request" của `03-dev-impact.md` **không có link PR**, chỉ có commit hash `6daa778302`. Không đọc được diff thì không kiểm chứng được fix-shape thực tế (đặc biệt câu hỏi "có disable nút trong lúc reload không"). — **Fix**: Dev cung cấp link PR/diff.
- **`[MAJOR] M-08` — GAP-5 / FUNC-SEQ-001**: quan điểm này **BẮT BUỘC** với màn có ≥2 thao tác trên cùng danh sách và có **Sort**. Các TC hiện có chỉ chạy **từng caller riêng lẻ**; không TC nào chạy **chuỗi** `stop remind → sort → phân trang → F5`. Đây đúng là vùng luồng mới (`initData` + callback) đi qua. — **Fix**: TC-FUNCSEQ001-01 ở §5.
- **`[MAJOR] M-09` — TC-DATAID001-01 chưa cover đúng quan điểm của chính nó**: `DATA-ID-001` yêu cầu *"tạo 2 đối tượng **trùng tên hiển thị** → thao tác từng cái"*, nhưng TC dùng 2 bản ghi **cố ý khác biệt rõ ràng** (`SF34051-RECORDB` vs bản ghi khác) — chính là điều kiện dễ nhất, không phải điều kiện quan điểm nhắm tới. Fix trỏ lại bản ghi bằng `find` theo id, đúng kiểu bug dễ lộ khi 2 dòng trùng tên + trùng ngày. — **Fix**: TC-DATAID001-02 (Boundary) ở §5.
- **`[MAJOR] M-10` — GAP-6 / DATA-COUNT-001**: màn 回答一覧 có tổng số bản ghi + phân trang, màn list form có 回答者数. Không TC nào kiểm số đếm **sau luồng stop remind** (luồng reload mới). Kho đã có `TC-FORM-351` gắn count vào luồng xóa câu trả lời, nhưng TC-REGSHARED001-03 của Studio **bỏ mất phần count** đó. — **Fix**: TC-DATACOUNT001-01 ở §5; đồng thời bổ sung expected "số người trả lời giảm đúng 1" vào TC-REGSHARED001-03.
- **`[MAJOR] M-11` — DATA-DB-001 thiếu WHERE-scope**: có đối chiếu DB thật ở tầng bản ghi nhưng chưa có case *"2 bot / 2 tài khoản có bản ghi trùng tên → dừng remind ở A → query xác nhận B không đổi"*. Đã hạ từ BLOCKER (ghi chú ② ở §3.6). — **Fix**: Leader quyết — nếu muốn phủ, thêm 1 TC regression; nếu chấp nhận rủi ro vì tầng service không bị chạm thì ghi lý do vào `Ghi chú` TC-OUTTRUTH001-01 (RULE-03).
- **`[MAJOR] M-12` — GAP-7 / DATA-CACHE-001 + REG-RUN-001**: kịch bản (1) của `DATA-CACHE-001` — *"trước deploy mở sẵn 1 tab (không refresh) → sau deploy thao tác tiếp trên tab đó"* — chưa có TC. Khác với TC-DEPLOYASSET001-01 (mở lại màn sau deploy): đây là **tab đang mở xuyên qua deploy**, đúng tình huống admin thật đang làm việc. — **Fix**: TC-DATACACHE001-01 ở §5.
- **`[MAJOR] M-13` — GAP-8 / UI-003**: chỉ có nhánh lỗi 5xx; thiếu **trạng thái rỗng** và **mạng chậm** ở tab リマインド sau khi popup được giữ mở. `UI-003` cảnh báo đúng rủi ro **false success** — popup ở lại mà tab remind render sai/loading vô hạn thì user vẫn tưởng đã dừng. — **Fix**: TC-UI003-01 ở §5.
- **`[MAJOR] M-14` — TC-CONC003-01 pass nhưng không chứng minh được điều nó nhắm tới**: evidence ghi `openedB=false (LoadingOverlay chặn đổi selection khi reload chờ)` — tức **nhánh race chính không chạy được**, TC rơi về trạng thái mà `tech_note` đã dự phòng là **N/A**. Đánh `pass` cho một branch N/A làm quan điểm `CONC-003` (đã nâng Cao) **trông như đã phủ**. — **Fix**: đổi kết quả thành `N/A`/ghi rõ branch không chạy được ở `Ghi chú`, và tách 1 TC riêng verify chính LoadingOverlay khóa đúng.
- **`[MAJOR] M-15` — TC-TOOLERRHYG001-01 chỉ chạy 1 trigger lỗi**: `Điều kiện tiền đề` nêu **2** khả năng (backup guard `BackupHistory status 0/1` theo `BR-06`, hoặc 5xx) nhưng evidence chỉ ghi *"Lỗi 5xx"*. Nhánh backup guard là nhánh có thật trong nghiệp vụ (EP-55) và cho thông báo khác. *(Không nâng BLOCKER vì nhánh error **không bị fix chạm** — Dev khai rõ; nhưng vẫn phải test đủ 2 trigger đã tự khai trong precondition.)* — **Fix**: chạy thêm nhánh backup guard, hoặc tách thành TC riêng.
- **`[MAJOR] M-16` — RULE-01: Boundary = 0/12**: phân bố `Normal 9 · Abnormal 3 · **Boundary 0**`. Các quan điểm ưu tiên **Cao** (`DEPLOY-ASSET-001`, `REG-SHARED-001`, `DATA-001`, `OUT-TRUTH-001`, `CONC-003` đã nâng Cao) đều thiếu Boundary mà **không TC nào ghi lý do** ở `Ghi chú`. — **Fix**: bổ sung Boundary theo §5, hoặc ghi lý do miễn trừ (RULE-03).
- **`[MAJOR] M-17` — GAP-9: chưa có TC cho luồng HỦY hộp thoại xác nhận**. Kho có `TC-FORM-354` với bước *"Nhấn 閉じる hoặc X → kiểm tra remind"* và expected *"không xóa remind"*. Luồng này đi qua đúng `confirmStopItemRemind` — hàm **Dev đã sửa**. Toàn bộ 12 TC chỉ đi nhánh "xác nhận". — **Fix**: TC-FUNC001-01 ở §5.
- **`[MAJOR] M-18` — GAP-10: branch guard "không tìm thấy bản ghi sau reload" chưa test**. Dev **tự nêu** ở mục TỰ REVIEW: *"Nếu bản ghi đang xem rơi khỏi trang/khoảng lọc hiện tại sau khi nạp lại thì popup giữ dữ liệu cũ; ... đã guard bằng kiểm tra tìm thấy mới gán"* — rồi tự kết luận "không xảy ra". Nhưng TC-CONC003-01 ghi trong `note` rằng case này đã bị **chủ động loại bỏ** ("boundary giả tạo"). Thực tế nó xảy ra được: một admin khác **xóa câu trả lời đó** trong lúc mình đang mở popup. Khi ấy popup giữ dữ liệu cũ và có thể hiển thị trạng thái sai. — **Fix**: TC-CONC001-03 ở §5.
- **`[MAJOR] M-19` [AP-3] — happy-path-only regression**: `T2` (3 TC) và `T3` (1 TC) đều có precondition "data sạch, đủ dữ liệu để phân trang" — không TC nào chạy regression ở **edge state** (danh sách rỗng sau lọc, form không có item remind, câu trả lời không chọn option remind nào — trạng thái mà kho `TC-FORM-353` mô tả là "tab remind ĐỂ TRỐNG"). — **Fix**: gộp vào TC-UI003-01 (§5) + bổ sung precondition biến thể cho TC-REGSHARED001-03.
- **`[MAJOR] M-20` — 12/12 TC có `spec_status = null`** → cột `Trạng thái đánh giá spec` rỗng toàn bộ. Không phân biệt được expected nào dựa trên spec, expected nào do AI/người tự suy diễn. Với task này rủi ro thật: expected "popup giữ mở" **không có trong spec FA-011** — nó đến từ 1 dòng `Exp:` của KH. *(Đối chiếu ngược: kho `TC-FORM-354` đã ghi expected tương đương từ trước — xem §6.)* — **Fix**: điền `spec_status` cho 12 TC (`Spec ghi rõ` / `Spec không ghi (đã hỏi <ai>)`).

### 4.3 Minor (có thể fix sau)

- **`[MINOR] M-21`** — evidence TC-REGSHARED001-01 ghi *"6 caller initData chạy OK"* nhưng chỉ liệt kê **5** thao tác (`changePage`, `changeLimit`, `sort`, `全期間 reset`, `changePanel`). Con số và danh sách không khớp nhau.
- **`[MINOR] M-22`** — 3 lần skip TC-DEPLOYASSET001-01 ghi lý do `"API"` (2 lần) — không có nghĩa với người đọc report. Lý do skip phải nói rõ điều kiện thiếu.
- **`[MINOR] M-23`** — 3 TC (TC-CONC003-01, TC-REGSHARED001-02, TC-DATA001-02 — tức NEW-11/12/13) **không map `requirement_keys` nào**, dù nội dung rõ ràng thuộc REQ-005 / REQ-002 / REQ-003. Làm lệch bảng coverage của Studio.
- **`[MINOR] M-24`** — `temp_id` **NEW-3 khuyết** (Studio id `12508` không còn trong danh sách, dãy id 12506→12515 đứt đúng 1 chỗ). Không rõ TC đó bị xóa vì lý do gì và có mang coverage nào không → dùng `testcase_get_history` để truy vết.
- **`[MINOR] M-25`** — Studio gán `feature = "shop-card"` cho task #198, trong khi task thuộc **FA-011 / FA-022 (form-answer)**. `task_get_report` vì thế đối chiếu coverage với spec của `shop-card` và ra `0/7 covered`. Gán sai feature làm hỏng thống kê độ phủ.
- **`[MINOR] M-26`** — `TC No.` trong `04-tc-list.md` là do tool sinh lại theo quy ước repo; trên Studio các TC vẫn chỉ có `temp_id` (`NEW-n`). Hai hệ định danh song song dễ gây nhầm khi trao đổi — nên thống nhất bằng `client_ref` (hiện chỉ 3/12 TC có).

### 4.4 Nit (gợi ý)

- **`[NIT] N-01`** — `PERM-002` (Cao) có trigger khớp trên giấy (thao tác dừng gửi tin = nhạy cảm) nhưng **không đề xuất TC**: tầng phân quyền `basic_access` không bị fix chạm (AP-5). Ghi lại để Leader chủ động quyết, không để nó im lặng biến mất khỏi bảng quan điểm.
- **`[NIT] N-02`** — tương tự với `MSG-002` / `STATE-DEP-001` / RULE-06: chưa TC nào verify **tin nhắc lịch thật sự không còn được gửi ra LINE** sau khi dừng. Cố ý không đề xuất vì fix là UI-only và tầng job gửi tin không bị chạm — nhưng nếu Leader muốn một lần chốt hành vi end-to-end thì đây là chỗ duy nhất còn hở.
- **`[NIT] N-03`** — tên folder review ghi `2026-09-04` trong khi ngày thực hiện là `2026-09-05` (lệch 1 ngày, do `/new-task` chạy sát nửa đêm). Không ảnh hưởng nội dung.

---

## 4.5 TC trùng lặp nội dung

> Đã rà **toàn bộ 12 TC** theo 4 yếu tố (`mã quan điểm` × `loại case` × `đối tượng + thao tác` × `tiền đề tương đương` → `expected` tương đương).

| Nhóm trùng | TC giữ lại | TC đề nghị xóa / gộp | Loại trùng | 4 yếu tố trùng nhau | Severity |
|---|---|---|---|---|---|
| DUP-1 | `TC-DATA001-02` (NEW-13) | `TC-OUTTRUTH001-01` (NEW-4) — **GỘP, KHÔNG xóa** | `DUP-SUBSET` (một phần) | Cùng thao tác (dừng 1 remind trong popup) · cùng `Normal` · expected của NEW-4 ("hiển thị đúng người thao tác + 操作日時, khớp dữ liệu lưu thực tế") **nằm trọn** trong expected của NEW-13. **Khác** ở tiền đề: NEW-4 = 1 remind active, NEW-13 = ≥2 remind → chưa phải trùng hoàn toàn | `[MINOR]` |

- **Gate đã chạy**: giả định xóa `TC-OUTTRUTH001-01` → chạy lại §3 + §3.6 trên 11 TC còn lại → **mất cover**: nó là **TC duy nhất** mang mã `OUT-TRUTH-001` (Cao) và là 1 trong 2 TC cover `D1`. ⇒ **đổi đề xuất từ "xóa" sang "GỘP"**: giữ cả 2, hoặc nếu muốn gọn thì giữ NEW-13 và chuyển mã `OUT-TRUTH-001` sang nó. **Không xóa NEW-4 khi chưa làm việc đó.**
- `DUP-INFLATE`: **không có** — không nhóm TC trùng nào đang làm một quan điểm/impact trông như đủ chiều.
- `DUP-CONFLICT`: **không có** — không cặp TC nào cùng tiền đề + cùng steps mà expected mâu thuẫn.
- Đối chiếu thêm với kho: `TC-DATA001-02` ≈ kho `TC-FORM-354` (cùng ý định "dừng remind A, remind B giữ nguyên") — **expected NHẤT QUÁN**, không conflict; xem §6.
- Chồng lấn nhẹ (không đề nghị xử lý): `TC-DATA001-01` (NEW-5) có expected phụ *"Popup vẫn hiển thị đúng câu trả lời đang xem"* trùng với NEW-1/NEW-2, nhưng ý định chính (giữ trang N + khoảng lọc) là riêng → **giữ nguyên**.
- Xóa/sửa thật do human thực hiện trên Studio (`testcase_update` / `testcase_delete`) — report này **không sửa TC nào**.

---

## 5. TCs đề xuất bổ sung

**Đã đối chiếu trước khi viết** (BƯỚC 5a/5b):

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | [`kho-tcs/fa011-taobieumau-フォーム作成.md`](../../kho-tcs/fa011-taobieumau-フォーム作成.md) — 481 TC; đọc chọn lọc 2 nhóm liên quan: **「Item remind」** (8 TC: TC-FORM-170…177) và **「Màn kết quả trả lời」** (16 TC: TC-FORM-344…359) |
| Vùng regression phát hiện từ kho | `TC-FORM-353` (tab remind ở màn chi tiết — có trạng thái **trống** khi user không chọn option / form không có remind) · `TC-FORM-354` (dừng remind option A, option B giữ nguyên — **chạy PRODUCTION**) · `TC-FORM-351` (xóa câu trả lời → **số người trả lời giảm**) · `TC-FORM-352` (phân trang 100 bản ghi, disable nút ở trang đầu/cuối) · `TC-FORM-176` (**form CŨ có item remind**) |
| Conflict expected vs kho | **Không.** `TC-FORM-354` expected ghi *"màn chi tiết hiện trạng thái đã dừng kèm người thao tác và thời gian"* → **khớp hoàn toàn** hành vi sau fix (xem §6 — đây là bằng chứng hành vi đúng đã được biết từ trước, không cần update spec) |
| GAP dùng lại TC kho (không viết mới) | `GAP-2` (DEPLOY-ASSET-001) → **không viết TC mới**, TC-DEPLOYASSET001-01 đã tồn tại, chỉ cần **chạy thật** (xem `B-02`) · `M-10` phần luồng xóa → dùng lại ý của `TC-FORM-351` bằng cách **bổ sung expected vào TC-REGSHARED001-03**, không đẻ TC mới |
| Xác nhận chống trùng | Đã đối chiếu **12** TC ở BƯỚC 0 + **24** TC kho liên quan — **không TC đề xuất nào trùng** (mỗi TC dưới đây đều khác ≥1 trong 4 yếu tố so với mọi TC đã có) |

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-CONC001-01 | UI | CONC-001 | Màn kết quả trả lời | Abnormal | manual | product | Bấm 配信停止 hai lần liên tiếp chỉ dừng nhắc lịch đúng một lần | - Đăng nhập admin bot A<br>- Form V3 có câu trả lời U1 với 1 nhắc lịch đang hoạt động<br>- Mở popup chi tiết U1, tab リマインド | 1. Bấm 「配信停止」, ở hộp thoại bấm 「配信停止」 xác nhận<br>2. **Ngay khi hộp thoại đóng, bấm liên tiếp 2 lần nữa vào vị trí nút 配信停止 trong lúc danh sách còn đang tải**<br>3. Chờ tải xong, đọc tab リマインド<br>4. Mở DevTools > Network, đếm số request tới đường dẫn dừng nhắc lịch<br>5. Mở lại popup U1 sau khi F5 | Thao tác double-click trong khoảng thời gian danh sách đang reload | Chỉ **1** request dừng nhắc lịch được gửi đi (hoặc request thứ 2 bị hệ thống từ chối, có thông báo rõ) · tab リマインド hiển thị **đúng 1** dòng trạng thái đã dừng với 1 tên người thao tác và 1 giá trị 操作日時 · không xuất hiện dòng trùng, không lỗi JS · sau F5 trạng thái không đổi | | Lấp `GAP-4 / B-04` · cover impact `F1` · Đánh giá spec: Spec không ghi (đã hỏi Dev — câu hỏi 2 §3.5) · Evidence: screenshot DevTools Network đếm số request + screenshot tab リマインド sau F5 · RULE-08 (race → product) |
| TC-CONC001-02 | UI | CONC-001 | Màn kết quả trả lời | Abnormal | manual | product | Dừng cùng một nhắc lịch từ 2 tab trình duyệt của cùng tài khoản | - Đăng nhập admin bot A<br>- Câu trả lời U1 có 1 nhắc lịch đang hoạt động<br>- Mở **2 tab** cùng trỏ tới màn kết quả của form đó, cả 2 tab đều đã mở popup chi tiết U1 ở tab リマインド | 1. Ở tab 1 bấm 「配信停止」 và xác nhận, chờ hoàn tất<br>2. Chuyển sang **tab 2 (chưa refresh)**, bấm 「配信停止」 và xác nhận<br>3. Quan sát phản hồi ở tab 2<br>4. F5 cả 2 tab và so sánh trạng thái nhắc lịch | 2 tab cùng tài khoản, tab 2 giữ trạng thái màn hình cũ | Tab 2 **không** báo dừng thành công lần thứ hai — hiển thị thông báo lỗi/xung đột hoặc trạng thái đã dừng sẵn có · sau F5 cả 2 tab hiển thị **cùng một** tên người thao tác và **cùng một** 操作日時 (của lần dừng đầu tiên) · không phát sinh bản ghi dừng thứ hai | | Lấp `GAP-4 / B-04` · cover impact `F1` · Đánh giá spec: Spec không ghi (đã hỏi Dev) · Evidence: screenshot 2 tab cạnh nhau sau F5 · RULE-08 |
| TC-CONC001-03 | UI | CONC-001 | Màn kết quả trả lời | Boundary | manual | product | Bản ghi đang xem bị người khác xóa ngay trước khi dừng nhắc lịch | - 2 tài khoản admin cùng bot A (staff X và staff Y)<br>- Câu trả lời U1 có nhắc lịch đang hoạt động<br>- Staff X mở popup chi tiết U1, tab リマインド<br>- Staff Y đang ở màn kết quả cùng form | 1. Staff Y xóa câu trả lời U1 và xác nhận<br>2. Staff X (popup vẫn đang mở, **chưa refresh**) bấm 「配信停止」 và xác nhận<br>3. Quan sát popup của staff X sau khi danh sách tải lại<br>4. Staff X bấm F5 rồi mở lại màn kết quả | Bản ghi đang xem đã bị xóa ở phiên khác trước khi thao tác dừng | Popup của staff X **không** hiển thị trạng thái "đã dừng" cho một bản ghi không còn tồn tại · hệ thống báo rõ bản ghi không còn (hoặc đóng popup) thay vì im lặng giữ dữ liệu cũ · sau F5, câu trả lời U1 biến khỏi danh sách · không lỗi JS, không trắng màn | | Lấp `GAP-10 / M-18` · cover impact `F1`, `F2` · Đánh giá spec: Spec không ghi (đã hỏi Dev — câu hỏi 3 §3.5) · Evidence: video 2 phiên + screenshot popup staff X · Đây chính là branch guard Dev tự nêu ở mục TỰ REVIEW và TC-CONC003-01 đã chủ động loại bỏ · RULE-08 |
| TC-COMPATLEGACY001-01 | UI | COMPAT-LEGACY-001 | Item remind | Normal | manual | Tất cả | Màn kết quả của form đời cũ: dừng nhắc lịch vẫn hoạt động sau khi deploy fix | - Có form đời cũ F_old với `using_old_version=1`, có item remind theo cơ chế cũ<br>- F_old đã có ≥1 câu trả lời chọn option remind, nhắc lịch đang hoạt động<br>- Đã deploy branch fix | 1. Mở màn kết quả trả lời của F_old<br>2. Ghi lại đường dẫn màn hình và tên file JavaScript màn này tải (DevTools > Network)<br>3. Mở chi tiết câu trả lời có nhắc lịch, tìm tab/khu vực nhắc lịch<br>4. Nếu có nút dừng gửi → bấm và xác nhận<br>5. Quan sát màn hình sau khi dừng | Form đời cũ (`using_old_version=1`) có item remind cũ | Màn kết quả của F_old mở được bình thường sau deploy · ghi nhận rõ màn này dùng file JS nào (cùng file với V3 hay file khác) · nếu có nút dừng gửi: dừng thành công, hiển thị đúng người thao tác + thời điểm, **và màn hình không bị đóng đột ngột** · nếu không có nút dừng gửi thì ghi nhận làm bằng chứng đóng phạm vi | | Lấp `GAP-3 / B-03` · cover impact `T1` · regression · dẫn từ kho `TC-FORM-176` · Đánh giá spec: Spec ghi rõ (`BR-09` `using_old_version`) · Evidence: screenshot DevTools Network (tên file JS) + screenshot màn sau khi dừng · RULE-09 — bắt buộc chụp CẢ hai nhánh cũ/mới |
| TC-COMPATLEGACY001-02 | UI | COMPAT-LEGACY-001 | Item remind | Abnormal | manual | Tất cả | Form đời cũ được lưu lại qua giao diện mới rồi dừng nhắc lịch | - Form đời cũ F_old (`using_old_version=1`) có item remind cũ và câu trả lời có nhắc lịch đang hoạt động<br>- Đã deploy branch fix | 1. Mở F_old ở màn chỉnh sửa và bấm lưu (theo `BR-09`, lưu qua giao diện mới sẽ chuyển form về bản v3)<br>2. Mở lại màn kết quả trả lời của F_old<br>3. Mở chi tiết câu trả lời có nhắc lịch cũ, vào tab リマインド<br>4. Bấm 「配信停止」 và xác nhận | Form chuyển từ đời cũ sang v3 trong khi đã tồn tại nhắc lịch tạo theo cơ chế cũ | Nhắc lịch tạo theo cơ chế **cũ** vẫn hiển thị đầy đủ trong tab リマインド của giao diện mới · dừng thành công · popup **vẫn mở** và hiển thị đúng người thao tác + 操作日時 · không mất dữ liệu nhắc lịch cũ, không lỗi JS | | Lấp `GAP-3 / B-03` · cover impact `T1` · regression · dẫn từ kho `TC-FORM-176` · Đánh giá spec: Spec ghi rõ (`BR-09`: "Mọi lần lưu qua v3 API đều set `using_old_version=0`") · Evidence: screenshot tab リマインド trước và sau khi lưu form · Không có Boundary cho cặp cũ/mới (chỉ 2 nhánh rời rạc, không có trục biên) — miễn trừ RULE-01 theo RULE-03 |
| TC-FUNC001-01 | UI | FUNC-001 | Màn kết quả trả lời | Abnormal | manual | Tất cả | Hủy hộp thoại xác nhận thì không dừng nhắc lịch và popup giữ nguyên | - Đăng nhập admin bot A<br>- Câu trả lời U1 có nhắc lịch đang hoạt động<br>- Mở popup chi tiết U1, tab リマインド | 1. Bấm 「配信停止」 → hộp thoại xác nhận 「リマインドの停止」 hiện ra<br>2. Bấm 「閉じる」 (hoặc dấu X) để đóng hộp thoại<br>3. Đọc lại tab リマインド<br>4. Lặp lại bước 1, lần này bấm ra vùng ngoài hộp thoại / phím Esc<br>5. F5 rồi mở lại popup U1 | Thao tác hủy hộp thoại bằng 閉じる, X, Esc | Nhắc lịch **vẫn ở trạng thái đang hoạt động**, nút 「配信停止」 còn nguyên, không xuất hiện dòng "đã dừng" · popup chi tiết **không bị đóng** và vẫn hiển thị đúng câu trả lời U1 · danh sách phía sau **không bị tải lại** · sau F5 nhắc lịch vẫn hoạt động | | Lấp `GAP-9 / M-17` · cover impact `F1` · dẫn từ kho `TC-FORM-354` (bước 3) · Đánh giá spec: Spec không ghi (đã hỏi Dev) · Evidence: screenshot tab リマインド sau khi hủy + sau F5 |
| TC-DATAID001-02 | UI | DATA-ID-001 | Màn kết quả trả lời | Boundary | manual | Tất cả | Hai câu trả lời trùng tên hiển thị và trùng ngày: dừng đúng bản ghi đang xem | - Đăng nhập admin bot A<br>- Hai LINE user có **cùng tên hiển thị** (VD cả hai đều là `山田`) cùng trả lời form V3 **trong cùng một ngày**, tạo ra 2 dòng trùng tên + trùng ngày<br>- Cả 2 câu trả lời đều có nhắc lịch đang hoạt động<br>- Nội dung trả lời của 2 người khác nhau rõ ràng để phân biệt | 1. Mở popup chi tiết của bản ghi **thứ hai** trong 2 dòng trùng tên, ghi lại nội dung ở tab 回答内容<br>2. Chuyển tab リマインド, bấm 「配信停止」 và xác nhận<br>3. Sau khi danh sách tải lại, đọc nội dung tab 回答内容 của popup<br>4. Đóng popup, mở bản ghi **thứ nhất** trong 2 dòng trùng tên và đọc tab リマインド | 2 câu trả lời trùng tên hiển thị + trùng ngày trả lời | Sau khi tải lại, popup vẫn hiển thị **đúng bản ghi thứ hai** — nội dung tab 回答内容 giữ nguyên như bước 1, không đổi sang bản ghi trùng tên còn lại · nhắc lịch của bản ghi thứ hai chuyển sang trạng thái đã dừng · nhắc lịch của **bản ghi thứ nhất vẫn đang hoạt động** | | Lấp `GAP / M-09` · cover impact `F1`, `D1` · Đánh giá spec: Spec không ghi (đã hỏi Leader) · Evidence: screenshot 2 dòng trùng tên trong danh sách + screenshot popup sau khi dừng + screenshot bản ghi còn lại · Đây là điều kiện đúng của DATA-ID-001 mà TC-DATAID001-01 chưa dựng |
| TC-FUNCSEQ001-01 | UI | FUNC-SEQ-001 | Màn kết quả trả lời | Normal | manual | Tất cả | Chuỗi thao tác liên tiếp sau khi dừng nhắc lịch không làm sai danh sách | - Form V3 có ≥150 câu trả lời (đủ để phân trang) và ≥1 câu trả lời có nhắc lịch hoạt động ở trang 2<br>- Đang lọc theo một khoảng ngày cụ thể có dữ liệu | 1. Sang trang 2, mở popup chi tiết câu trả lời có nhắc lịch, dừng nhắc lịch và xác nhận<br>2. **Không tải lại trang**, đổi thứ tự sắp xếp cột ngày giờ trả lời<br>3. **Không tải lại trang**, đổi số dòng hiển thị mỗi trang<br>4. **Không tải lại trang**, đổi sang tab danh sách còn lại rồi quay về<br>5. Bấm **F5** và so sánh với trạng thái ngay sau bước 4 | Chuỗi: dừng nhắc lịch → sort → đổi số dòng → đổi tab → F5 | Sau mỗi bước, danh sách hiển thị đúng theo thao tác vừa thực hiện, không nhảy về trang 1 ngoài ý muốn, không mất điều kiện lọc ngày · sau **F5**, dữ liệu và thứ tự sắp xếp **giống hệt** trạng thái ngay sau bước 4 · nhắc lịch đã dừng vẫn ở trạng thái đã dừng · không lỗi JavaScript ở console qua toàn bộ chuỗi | | Lấp `GAP-5 / M-08` · cover impact `F2`, `T2` · regression · Đánh giá spec: Spec ghi rõ (`SCR-FA11-09`) · Evidence: 2 screenshot cạnh nhau — sau bước 4 và sau F5 |
| TC-DATACOUNT001-01 | UI | DATA-COUNT-001 | Màn kết quả trả lời | Normal | manual | Tất cả | Số bản ghi và số người trả lời không đổi sau khi dừng nhắc lịch | - Form V3 có đúng **5** câu trả lời (biết trước con số)<br>- 1 trong 5 câu trả lời có nhắc lịch đang hoạt động<br>- Ghi lại trước: tổng số bản ghi trên màn kết quả và số người trả lời hiển thị ở màn danh sách form | 1. Ghi nhận số người trả lời ở màn danh sách form (kỳ vọng `5人`) và tổng số dòng ở màn kết quả<br>2. Mở popup chi tiết câu trả lời có nhắc lịch, dừng nhắc lịch và xác nhận<br>3. Sau khi danh sách tải lại, đếm lại số dòng và đọc lại tổng số bản ghi<br>4. Quay về màn danh sách form, đọc lại số người trả lời<br>5. Tải file CSV kết quả và đếm số dòng dữ liệu | Bộ dữ liệu biết trước: 5 câu trả lời, dừng 1 nhắc lịch (phép tính tay: 5 → **vẫn 5**) | Dừng nhắc lịch **không** làm thay đổi số lượng câu trả lời: màn kết quả vẫn 5 dòng, tổng số bản ghi vẫn 5 · màn danh sách form vẫn hiển thị `5人` · CSV vẫn 5 dòng dữ liệu · 3 nguồn (màn kết quả / màn danh sách form / CSV) khớp nhau | | Lấp `GAP-6 / M-10` · cover impact `F2`, `T2` · Đánh giá spec: Spec ghi rõ (`SCR-FA11-09` bước 2 + `EP-19` CSV) · Evidence: bảng đối chiếu 3 nguồn + phép tính tay · dẫn từ kho `TC-FORM-351`, `TC-FORM-355` |
| TC-DATACACHE001-01 | UI | DATA-CACHE-001 | Màn kết quả trả lời | Abnormal | manual | product | Tab đang mở xuyên qua thời điểm deploy vẫn thao tác dừng nhắc lịch đúng | - Trước khi deploy: mở sẵn màn kết quả trả lời của form V3 trên 1 tab và **để nguyên, không refresh**<br>- Câu trả lời U1 có nhắc lịch đang hoạt động<br>- Thực hiện deploy branch fix trong lúc tab đó vẫn mở | 1. Trước deploy: mở tab, mở popup chi tiết U1 rồi đóng popup lại, giữ nguyên tab<br>2. Tiến hành deploy bản fix<br>3. Quay lại **đúng tab cũ đó, không refresh**, mở popup chi tiết U1, vào tab リマインド<br>4. Bấm 「配信停止」 và xác nhận<br>5. Quan sát màn hình và tab Console của DevTools<br>6. F5 tab đó rồi thao tác lại trên một câu trả lời khác có nhắc lịch | Tab giữ bản JavaScript trước fix, thao tác sau khi server đã lên bản mới | Ghi nhận rõ hành vi của tab cũ: nếu tab còn dùng JS cũ thì popup sẽ **đóng** (triệu chứng bug gốc) — kết quả này phải được ghi lại làm bằng chứng cho quyết định cache-busting, **không** báo Đạt · không phát sinh lỗi JavaScript lạ hay trắng màn · sau F5, luồng dừng nhắc lịch chạy đúng bản fix: popup **vẫn mở** và hiển thị trạng thái đã dừng | | Lấp `GAP-7 / M-12` · cover impact `D2`, `T5` · Đánh giá spec: Spec không ghi (đã hỏi Dev — câu hỏi 4 §3.5) · Evidence: screenshot Console + Network của tab cũ trước và sau F5 · RULE-08 — asset/deploy bắt buộc product · Bổ trợ cho TC-DEPLOYASSET001-01, **không thay thế** |
| TC-UI003-01 | UI | UI-003 | Màn kết quả trả lời | Boundary | manual | Tất cả | Tab nhắc lịch hiển thị đúng ở trạng thái rỗng và khi mạng chậm | - Form V3 có: câu trả lời U1 chọn option remind (có nhắc lịch), câu trả lời U2 **không chọn** option remind nào, và form F3 **không có** item remind nào<br>- DevTools bật sẵn để bật Network throttling (Slow 3G) | 1. Mở popup chi tiết U2, vào tab リマインド và quan sát<br>2. Mở màn kết quả của form F3, mở popup chi tiết một câu trả lời, vào tab リマインド và quan sát<br>3. Quay về form ban đầu, bật Network throttling Slow 3G<br>4. Mở popup chi tiết U1, tab リマインド, bấm 「配信停止」 và xác nhận<br>5. Quan sát màn hình trong suốt thời gian chờ cho tới khi tải xong | U2 không có nhắc lịch · F3 không có item remind · mạng Slow 3G | Bước 1–2: tab リマインド hiển thị trạng thái **rỗng** rõ ràng, không lỗi, không trắng vùng nội dung · Bước 4–5: trong lúc chờ có chỉ báo đang xử lý, **không loading vô hạn**, **không** hiện trạng thái "đã dừng" trước khi máy chủ trả kết quả · khi tải xong popup vẫn mở và hiển thị đúng trạng thái đã dừng | | Lấp `GAP-8 / M-13` + `M-19` (edge state cho AP-3) · cover impact `F1`, `T1` · dẫn từ kho `TC-FORM-353` · Đánh giá spec: Spec không ghi (đã hỏi Leader) · Evidence: screenshot 3 trạng thái (rỗng U2 / rỗng F3 / đang chờ khi Slow 3G) |

> **RULE-01 — ghi chú miễn trừ**: `CONC-001` (Cao) được đề xuất đủ 3 chiều (Abnormal ×2 + Boundary ×1); chiều `Normal` đã có sẵn `TC-TOOLKNOW002-01` (một lần bấm → xử lý đúng một lần) nên không viết lại. `COMPAT-LEGACY-001` (Cao) chỉ có Normal + Abnormal — miễn trừ Boundary vì quan điểm này là **so sánh 2 nhánh cũ/mới rời rạc**, không có trục biên (ghi lý do theo RULE-03).

---

## 6. Spec update needed

| # | Section spec | Nội dung cần update | Nguồn mâu thuẫn | Ai chốt |
|---|---|---|---|---|
| 1 | [`spec-features/admin/form-answer/feature-spec.md`](../../spec-features/admin/form-answer/feature-spec.md) — `SCR-FA11-09` (Trang kết quả trả lời) | Spec mô tả màn kết quả có "panel chi tiết inline" nhưng **không mô tả tab リマインド trong panel, nút 「配信停止」, hộp thoại xác nhận 「リマインドの停止」, và hành vi màn hình sau khi dừng**. Đây chính là hành vi bị bug và được fix — hiện không có chuẩn spec nào để đối chiếu Expected. Đề nghị bổ sung 1 bước vào bảng luồng `SCR-FA11-09`: *"Click 配信停止 ở tab リマインド → hộp thoại xác nhận → dừng thành công thì **panel chi tiết GIỮ NGUYÊN mở**, tab リマインド hiển thị người thao tác + 操作日時"*, kèm endpoint `POST /ajax/stop-item-remind`. | Bug #34051 (KH nêu expected) + `TC-FORM-354` của kho (đã ghi expected tương đương) + bản fix `6daa778302` — **cả 3 nguồn nhất quán**, chỉ riêng spec là thiếu | `PM / Leader` |
| 2 | `spec-features/admin/form-answer/` — Business Rules | Bổ sung business rule cho **backup guard của thao tác dừng nhắc lịch**: `BR-06` hiện chỉ ghi backup lock cho thao tác **tạo/sửa/xóa form**, nhưng endpoint `EP-55` `/ajax/stop-item-remind` cũng có guard này (theo `Điều kiện tiền đề` của TC-TOOLERRHYG001-01) và trả thông báo 「削除できません」. | `TC-TOOLERRHYG001-01` (Studio) mô tả guard này vs `BR-06` trong spec không nhắc tới | `Dev / PM` |
| 3 | — (không phải spec sản phẩm) | `spec-features/admin/index.md` dòng 21 vẫn ghi **FA-011 = CHƯA** ở cả 6 cột trong khi `spec-features/admin/form-answer/` đã HOÀN THÀNH. Đã được ghi nhận sẵn ở kho (`MT-00`) nhưng chưa xử lý — làm người review dễ kết luận nhầm "không có spec". | Kho `fa011` mục `MT-00` | `Leader` |

> **Không có `DUP-CONFLICT`** ở §4.5 và **không có conflict expected với kho** ở §5 → 3 mục trên là **bổ sung spec còn thiếu**, không phải sửa spec sai.
