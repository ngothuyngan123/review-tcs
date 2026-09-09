# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | `#35968 — [Sort folder, sort tên] Check 4 bug sort ở các màn qrcode, form, template, url, cross, scenario` |
| Reviewer (Leader) | `<điền>` (draft do /review-tc sinh) |
| Tester được review | `<member điền — file 04 chưa ghi tên>` |
| Ngày review | `2026-06-25` |
| Version TCs | `v1` (fetch từ Sheet tab `#35968`, gid 898638988) |
| Vòng review | `Round 1` |

> **Spec reference**: KHÔNG có `02-spec-reference.md` cho task này → dùng `templates/LME-SYSTEM-SPEC.md` tổng + checklist `C.8 Sort`. Không phát hiện mâu thuẫn spec với cách fix (fix thuần FE, không đổi business rule / backend).

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — Có issue MAJOR, cần fix + review lại vòng 2

**Lý do ngắn gọn**: Bộ 161 TCs **cover rất tốt 4 triệu chứng bug chính** (kéo-thả → click nút sort lên/xuống) trên cả 6 màn + folder — đây là điểm mạnh. Nhưng bị **REJECTED** vì 6 nhóm MAJOR: (1) file `03-dev-impact.md` chưa được tester tick verify; (2) **mâu thuẫn Cross sort-item**: 21 TC mô tả "Kéo" nhưng Dev nói màn này button-based + KHÔNG sửa; (3) thiếu chiều **sort template TRONG folder** (path `items_sort`/`group_open` của F3/F10); (4) thiếu dimension **cross-browser/OS** cho 1 fix kéo-thả; (5) cột Status đang "OK staging" nhưng là build CŨ — fix branch `ai_fixbug_35968` **chưa test runtime**; (6) nhiều Expected mơ hồ ("theo chuẩn sort", "theo chuẩn").

---

## 2. Tóm tắt cho member

Bộ TC rất công phu và bám sát 4 bug gốc: mỗi màn đều có chuỗi "kéo item → click nút sort ở vị trí đầu/2/3/cuối" verify đúng cả 2 phần của fix (nút disable đúng biên = bug 3,4; click phản hồi & di chuyển đúng = bug 1,2). Khen phần này. Cần xử lý trước khi approve: (a) hỏi Dev xác nhận màn **Cross sort-item** là kéo-thả hay button (21 TC đang ghi "Kéo" nhưng impact note nói button + không sửa); (b) thêm TC **sort template khi đang mở trong folder**; (c) **reset Status** toàn bộ về "Chưa test" và re-test trên build có fix; (d) thêm matrix **Win+Mac / Chrome+Safari** cho thao tác kéo-thả; (e) làm rõ các Expected ghi "(theo chuẩn sort)".

---

## 3. Coverage Matrix

> Map suy luận từ Title/Steps/Expected (file 04 không có cột Map to Impact). Không có data impact (mục 4.2 = "Không có"). Fix thuần FE đồng bộ thứ tự hiển thị.

| Impact | Loại | Priority | TCs map (suy luận) | # TC | Status |
|---|---|---|---|---|---|
| **BUG** — 4 triệu chứng sau kéo-thả (no-response / nhảy sai / disable-lên sai / disable-xuống sai) | Fix | — | TC001-012, TC030-041, TC059-070, TC107-118, TC133-144 (drag→click nút) | ~60 | **OK** (trừ Cross — xem §4.2) |
| **F1** — Cross `.sort-folder` rebuild `arrGroupSort` | Function | Direct | TC154-160 | 7 | OK |
| **F2** — Form `openModalSortItem/Folder` rebuild `dataSortForm`/`arrGroupSort` | Function | Direct | TC059-086 | 28 | OK |
| **F3** — Template `.sort-folder` + `.sort-list` (`items_default_sort`/`items_sort` theo `group_open`) | Function | Direct | TC001-028 | 28 | **RISK** — path sort item TRONG folder chưa rõ |
| **F4** — QR `openModalSortQr/Folder` rebuild `arrItemsSort`/`arrGroupSort` | Function | Direct | TC030-057 | 28 | OK |
| **F5** — Scenario `.sort-folder` + `.sort-list` rebuild `item_all` | Function | Direct | TC107-131 | 25 | OK |
| **F6** — Cross `:key` `sort_folder.blade` | Function | Direct | TC154-160 | 7 | OK |
| **F7** — Form folder `:key` | Function | Direct | TC080-086 | 7 | OK |
| **F8** — Form sort-item `:key` (`dataSortForm`) | Function | Direct | TC059-079 | 21 | OK |
| **F9** — Template folder `:key` | Function | Direct | TC022-028 | 7 | OK |
| **F10** — Template `:key="index"`→`:key="item.id"` (`items_default_sort` + `items_sort`) | Function | Direct | TC001-021 | 21 | **RISK** — chỉ verify list default, chưa thấy `items_sort` (in-folder) |
| **F11** — QR folder `:key` | Function | Direct | TC051-057 | 7 | OK |
| **F12** — QR sort-item `:key` (`arrItemsSort`) | Function | Direct | TC030-050 | 21 | OK |
| **F13** — Scenario item+folder `:key="index"`→`item.id` | Function | Direct | TC107-131 | 25 | OK |
| **F14** — URL `:key` (`list_url_sort` + `folders_sort`, button-based) | Function | Direct | TC088-106 | 19 | OK |
| **D —** | Data | — | Không có data impact (mục 4.2) | — | N/A |
| **T1** — Màn QR (item + folder) | Feature | Medium | TC030-058 | 29 | OK |
| **T2** — Màn Form (form + folder) | Feature | Medium | TC059-087 | 29 | OK |
| **T3** — Màn Message template (template + folder) | Feature | Medium | TC001-029 | 29 | **RISK** — thiếu in-folder template sort |
| **T4** — Màn URL (button-based) | Feature | Low | TC088-106 | 19 | OK |
| **T5** — Màn Cross (folder fixed; item = ajax+button, không sửa) | Feature | Low | TC133-161 | 29 | **RISK** — TC item ghi "Kéo" mâu thuẫn impact |
| **T6** — Màn Scenario (item + folder) | Feature | Medium | TC107-132 | 26 | OK |

### ORPHAN TCs (nếu có)

| TC ID | Title | Lý do orphan | Hành động đề xuất |
|---|---|---|---|
| TC133–TC153 | [Cross] Sort Cross (item) — chuỗi "Kéo Cross…" | Mục 3 + 4.3 dev-impact: Cross **sort item dùng ajax + nút (không kéo-thả), đã có `:key`, KHÔNG cần sửa**. 21 TC đang test path code KHÔNG bị fix, lại mô tả bằng thao tác "Kéo" → có thể không khớp UI thật (AP-5 over-coverage). | **Hỏi Dev xác nhận** Cross item là kéo-thả hay button. Nếu button → sửa steps (bỏ "Kéo"), re-label thành regression; nếu kéo-thả → cập nhật lại mục 3/4.3 dev-impact (Dev note sai). |

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| Fix shape (đọc mục 2 dev-impact) | **FE state-sync** (Vue `:key="item.id"` + dựng lại mảng dữ liệu Vue sau kéo-thả). **KHÔNG** thuộc 6 shape chuẩn (không phải error-handler / validation / race / N+1 / soft-delete / migration). |
| Trigger space cần cover | Fix gồm 2 phần độc lập: **(P1)** `:key` đúng → trạng thái `:disabled` nút lên/xuống khớp item ở biên; **(P2)** dựng lại mảng → click nút lên/xuống phản hồi + di chuyển đúng hướng. Cả 2 chỉ lộ **SAU thao tác kéo-thả**. Cần thêm: id-set thay đổi (tạo mới / xóa) rồi kéo-sort; save → reload giữ thứ tự; đa browser/OS. |
| Số trigger TCs hiện cover | P1 ✓ (TC001 disable-lên @vị trí 1, TC003 disable-xuống @cuối, …); P2 ✓ (drag→click nhiều vị trí). **Thiếu**: xóa item rồi kéo-sort (chỉ URL có delete→sort TC101-103); in-folder template (F10 `items_sort`); reload sau save chưa verify tường minh; cross-browser. |
| KH report dạng | **Có root cause cụ thể** — 4 triệu chứng là hành vi nút sort rất xác định (không phản hồi / nhảy lên / disable sai), Leader note xác nhận root cause = desync jQuery sortable ↔ Vue, đã có **mẫu chuẩn màn Tag** chạy production. **KHÔNG phải symptom-only mơ hồ** → AP-2 không áp dụng. |
| Alternative root causes cần verify | N/A — root cause đã xác định + đã được duyệt ở màn Tag. |
| Anti-patterns dính | **AP-5** (over-coverage: Cross item drag TCs test code không sửa). **AP-3 nhẹ** (nhiều TC happy-path; thiếu edge-state: list rỗng/1 item, xóa về biên rồi sort trên màn kéo-thả). AP-1/AP-2/AP-6 không áp dụng. AP-4: PR link CÓ (`bitbucket .../10350`) → reviewer chưa đọc diff để chốt `:key` áp đủ 14 chỗ — khuyến nghị Dev/Leader đối chiếu diff. |

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- _Không có BLOCKER._ Không phát hiện màn in-scope nào bị **GAP hoàn toàn** ở reproduction 4 bug. (Các vấn đề bên dưới là thiếu chiều / process, không phải bỏ lọt root cause.)

### 4.2 Major (nên fix)

- `[MAJOR] FIX-SHAPE` **GAP-1 (Template in-folder)**: F3/F10 cho biết template sort có **2 path** — `items_default_sort` (list ngoài) và `items_sort` theo `group_open` (sort template **đang mở trong folder**). Toàn bộ TC001-021 chỉ test list mặc định, **không có TC nào sort template khi đang ở trong 1 folder mở** → path `items_sort` chưa được verify. Thêm TC (xem §5 TC-NEW-01/02).
- `[MAJOR] AP-5` **TC133–TC153 (Cross item)**: 21 TC mô tả "Kéo Cross từ dưới lên" nhưng mục 3 + 4.3 dev-impact khẳng định **Cross sort-item dùng ajax + nút, KHÔNG kéo-thả, KHÔNG sửa**. Mâu thuẫn → steps có thể không thực thi được trên UI thật. **Hỏi Dev chốt mô hình tương tác**, rồi sửa steps hoặc đính chính dev-impact.
- `[MAJOR]` **Dev impact chưa verify**: `03-dev-impact.md` checkbox "Tester verify auto-fill chính xác" (auto-filled `2026-06-09 by /new-task`) **CHƯA tick**. F/D/T có thể chưa đầy đủ/đúng mapping. Yêu cầu tester đọc lại journal #119876 + #120468 Redmine và tick trước khi review có giá trị. _(Lưu ý: `01-bug-task.md` ĐÃ tick — chỉ file 03 còn thiếu.)_
- `[MAJOR]` **Status không tin cậy**: cột Status toàn bộ là `OK/Done staging/OK` — nhưng fix branch `ai_fixbug_35968` mới verify `node -c` + `php -l`, **CHƯA test runtime** (file 03 + note env file 04). Status đang phản ánh build CŨ. **Reset toàn bộ về "Not test"/"Chưa re-test fix"** và chạy lại trên Staging sau khi deploy branch fix.
- `[MAJOR] CL-NonF-1 (Compatibility)`: fix tâm điểm là **kéo-thả jQuery UI sortable** — hành vi chuột/drag nhạy cảm theo browser/OS. Không TC nào chỉ định môi trường. Thêm matrix **Win + Mac × Chrome + Safari** cho ≥ 1 luồng drag→click mỗi màn kéo-thả (Template/QR/Form/Scenario/Cross-folder).
- `[MAJOR]` **Expected mơ hồ (B.1)**: rất nhiều TC có Expected = `(theo chuẩn sort)` hoặc `(theo chuẩn)` — không đo lường được, 2 tester chạy ra 2 kết quả. Đặc biệt nghiêm trọng ở các TC "Check account staff" (TC029/058/087/106/132/161) — cả 1 mục checklist (CL-Func-1) bị rút gọn thành "(theo chuẩn)". Viết rõ Expected: staff không quyền → chặn access; staff có quyền → sort/lưu OK.

### 4.3 Minor (có thể fix sau)

- `[MINOR]` **Typo verbatim từ Sheet** (đã được note ở file 04, nên sửa khi chỉnh): TC065 ghi "Tag B đang ở vị trí số 2" (đúng phải "Form B"); TC139 ghi "scen B đang ở vị trí số 2" (đúng phải "Cross B").
- `[MINOR]` **Steps folder lẫn tên item**: các TC sort folder lại tham chiếu tên item — TC025 "Click vào Template vừa sort (Template A…)", TC054 "Click vào QR vừa sort", TC083 "Click vào Form vừa sort", TC128 "Click vào scen vừa sort", TC157 "Click vào Cross vừa sort". Đổi thành "folder".
- `[MINOR]` **Expected folder garbled**: TC026/055/084/120/129/158 ghi "Thực hiện click vào **nút folder đúng X lên** thành công" — câu lỗi. Sửa thành "click nút sort folder lên thành công".
- `[MINOR] CL-Func-2`: các TC "save lại list đã sort" (TC013/027/042/056/071/085/…/145/159) Expected chỉ "hiển thị về vị trí mong muốn" — **chưa verify reload trang** sau save không lỗi/không reset thứ tự. Bổ sung bước reload.
- `[MINOR]` **Type/Priority để trống** toàn bộ 161 TC — member/Leader cần điền (Positive/Negative/Boundary/Regression) để đánh giá tỷ lệ chiều (mục C review-checklist).

### 4.4 Nit (gợi ý)

- `[NIT] CL-Func-5 (Double click)`: chưa có TC double-click nút sort / nút save ở lần thao tác cuối → khả năng duplicate/ghi đè thứ tự. Rủi ro thấp nhưng nên thêm 1 TC/màn đại diện.
- `[NIT] AP-3`: thêm edge-state cho màn kéo-thả: list chỉ **1 item** (cả 2 nút phải disable), list **rỗng**, và **xóa item về sát biên rồi kéo-sort** (hiện chỉ URL có delete→sort).
- `[NIT]` **Scope note**: Dev note màn khác cùng pattern (popup, image_richmenu, sales, reply, conversion, events, action_schedules, booking_event, rich_menu, infor_friend…) là **横展開 ticket sau** — đúng, KHÔNG tính GAP cho ticket này. Ghi lại để Leader theo dõi ticket kế.
- `[NIT]` **Đọc PR diff (AP-4)**: PR `bitbucket .../10350` có sẵn — khuyến nghị Leader/Dev đối chiếu 14 điểm sửa (F1-F14) với diff để chắc `:key` + rebuild áp đủ, vì container chưa chạy runtime.

---

## 5. TCs đề xuất bổ sung

> Member copy vào `04-tc-list.md` round tiếp theo.

| TC ID gợi ý | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| TC-NEW-01 | [Template] Sort template TRONG folder đang mở — kéo rồi click nút sort | Có ≥ 1 folder chứa ≥ 6 template; mở folder đó (group_open) | 1. Mở folder → list template trong folder hiện ra<br>2. Kéo 1 template từ dưới lên vị trí 2<br>3. Click template vừa kéo, rồi click nút sort lên/xuống | - Nút sort lên/xuống disable đúng biên trong context folder<br>- Click phản hồi, di chuyển đúng hướng<br>- Thứ tự trong folder hiển thị đúng | High | Regression | **F3, F10** (`items_sort`/`group_open`) |
| TC-NEW-02 | [Template] Sort template ngoài vs trong folder — không ảnh hưởng chéo | Có template ở list default + template trong folder | 1. Sort template ở list default<br>2. Mở folder, sort template trong folder<br>3. Đóng folder, kiểm tra lại list default | - 2 list (`items_default_sort` vs `items_sort`) độc lập, sort list này không đảo thứ tự list kia | High | Regression | **F10** |
| TC-NEW-03 | [Cross] Xác nhận mô hình sort item (kéo-thả hay button) | Màn Cross có ≥ 6 item | 1. Quan sát UI sort item màn Cross: có handle kéo-thả không?<br>2. Theo kết quả: chạy đúng thao tác (kéo HOẶC nút) → click nút sort | - Khớp với dev-impact (item = ajax+button, đã có `:key`)<br>- Nếu là button: TC133-153 phải sửa steps bỏ "Kéo" | High | Regression | **T5** (làm rõ orphan) |
| TC-NEW-04 | [All drag screens] Cross-browser drag→click sort | Mỗi màn kéo-thả có 6 item | Lặp luồng "kéo item lên vị trí 2 → click nút sort lên/xuống" trên: Win-Chrome, Win-Safari(n/a→Edge), Mac-Chrome, Mac-Safari | - Hành vi kéo-thả + disable nút + đồng bộ thứ tự **giống nhau** trên mọi browser/OS | High | Compatibility | **CL-NonF-1, BUG** |
| TC-NEW-05 | [All screens] Xóa item về sát biên rồi kéo-sort | List 6 item | 1. Xóa bớt còn 2 item<br>2. Kéo item dưới lên trên<br>3. Click nút sort 2 chiều | - `:key` map đúng dù id-set đã đổi<br>- Nút disable đúng (list 2 item: item đầu disable-lên, item cuối disable-xuống)<br>- Không rớt/nhân đôi item | Medium | Boundary | **F (`:key`), BUG** |
| TC-NEW-06 | [All screens] Account staff — Expected cụ thể | 1 staff KHÔNG quyền + 1 staff CÓ quyền màn tương ứng | 1. Login staff không quyền → mở màn sort<br>2. Login staff có quyền → kéo-sort + save | - Staff không quyền: bị chặn access/không thấy nút sort<br>- Staff có quyền: sort + lưu giống account chính | Medium | Negative/Positive | **CL-Func-1** (thay Expected "(theo chuẩn)") |
| TC-NEW-07 | [All screens] Reload sau save giữ thứ tự | List đã kéo-sort | 1. Kéo-sort → Save<br>2. **Reload trang (F5)**<br>3. Mở lại modal/list sort | - Sau reload thứ tự đúng như đã lưu, không lỗi console, không reset về thứ tự cũ | Medium | Regression | **CL-Func-2, BUG (P2 persistence)** |

---

## 6. Spec update needed (nếu có)

- [x] **Không cần update spec** — fix thuần FE đồng bộ thứ tự hiển thị; business rule sort + API lưu thứ tự (`#array_sort`/`#array_sort_fol`/`#array_sort_qr`) giữ nguyên. Không mâu thuẫn LME-SYSTEM-SPEC.

---

## 7. Checklist đã chạy

- [x] A. Coverage — A.1✓ (BUG cover tốt), A.2/A.4✓, **A.3 N/A** (không data impact), A.5✓ (phát hiện orphan Cross), **A.6 fix-shape**✓ (FE state-sync)
- [x] B. Chất lượng từng TC — B.1 **fail** (nhiều Expected "(theo chuẩn)"), B.2/B.3 OK, B.4 OK
- [x] C. Chất lượng bộ TC — Type/Priority trống → chưa đánh giá được tỷ lệ chiều; **thiếu Compatibility** (drag cross-browser)
- [x] D. Spec alignment — OK, không mâu thuẫn
- [x] E. Hành chính — TC ID chuẩn TCxxx; file đúng folder; **tester chưa ký tên/ngày** (file 04 để trống)
- [x] F. Base checklist LME
  - [x] **F.1 web**: CL-Func-1 (staff) có nhưng Expected mơ hồ; CL-Func-2 (reload) thiếu; CL-Func-4 (thao tác liên tục) partial (tạo mới + save liên tục có; Delete→Sort chỉ URL); CL-Func-5 (double click) thiếu; CL-Func-9 (search JP→sort) ✓; CL-Func-12/15 (max/phân trang) partial; **A.2 Compatibility thiếu** (MAJOR)
  - [x] **F.2 job**: N/A — fix thuần FE, không chạm job/callback/google sync
  - [x] **F.3 tính năng chung**: **C.8 Sort** = trọng tâm, cover 6 màn in-scope ✓ (24+ màn còn lại để ticket 横展開 sau, ngoài scope). C.7 plan-limit: sort không tạo data nên không áp dụng limit.

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | | |
| Tester | (đã đọc & hiểu feedback) | |
