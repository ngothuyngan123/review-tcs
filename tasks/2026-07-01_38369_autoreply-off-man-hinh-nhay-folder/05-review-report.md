# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | `#38369 — [Auto reply] Khi OFF tự động trả lời màn nhảy sang folder khác` |
| Reviewer (Leader) | `<Leader verify>` |
| Tester được review | `Kim Cúc` (nguồn TC Sheet) |
| Ngày review | `2026-07-01` |
| Version TCs | `v1` |
| Vòng review | `Round 1` |

> **Spec reference**: Không có `02-spec-reference.md` trong folder → dùng `templates/LME-SYSTEM-SPEC.md` tổng (feature Auto Reply / 自動応答), không có spec riêng cho task này.

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — Có issue BLOCKER/MAJOR, cần fix và review lại

**Lý do ngắn gọn**: Bộ TC cover khá tốt luồng bật/tắt rule + folder 未分類, nhưng **thiếu hoàn toàn TC cho `searchByKeyWord` (F3/T2)** — 1 trong 5 function đã bị sửa code (Direct impact) → nguy cơ bỏ lọt regression. Ngoài ra nhiều TC **steps trống** (TC008/009/010/012/013) không chạy được, và cả 2 file input auto-fill từ Redmine **chưa được tester verify** (checkbox chưa tick) nên coverage review chưa có giá trị pháp lý cuối.

---

## 2. Tóm tắt cho member

Bộ TC bám sát bug rất tốt: có cover cả OFF lẫn ON, folder tự tạo lẫn 未分類, reload, cancel sort, add/edit folder và cả regression "auto reply vẫn gửi được" — đúng tinh thần fix chạm 5 hàm. **Điểm cần fix quan trọng nhất**: fix này sửa `searchByKeyWord` (tìm kiếm auto reply theo từ khoá) nhưng chưa có TC nào verify sau khi search thì màn không nhảy folder → phải bổ sung ngay. Thứ hai: 5 TC đang để **steps trống** (TC008/009/010/012/013), member điền đủ Precondition/Steps/Expected để người khác chạy ra cùng kết quả. Cuối cùng nhớ tick 2 checkbox "verify auto-fill" ở file 01 + 03 sau khi đọc lại Redmine.

---

## 3. Coverage Matrix

> File 04 không có cột "Map to Impact" → mapping dưới đây **suy luận** từ Title / Steps / Expected mỗi TC.

| Impact | Loại | Priority | TCs map | # TC | Status |
|---|---|---|---|---|---|
| BUG (root cause — màn nhảy folder khi bật/tắt) | Fix | — | TC001, TC002, TC005, TC009, TC010 | 5 | **OK** |
| F1 — `turnOnItem` / `turnOffItem` | Function | Direct | TC001, TC002, TC003, TC004, TC008, TC009, TC010 | 7 | **OK** |
| F2 — `changeStatusReply` | Function | Direct | TC001, TC002, TC004 | 3 | **OK** |
| F3 — `searchByKeyWord` | Function | **Direct** | — | **0** | **GAP** |
| F4 — `addGroup` (thêm/sửa thư mục) | Function | Direct | TC006, TC011 | 2 | **OK** |
| F5 — `cancelSorted` | Function | Direct | TC007, TC008 | 2 | **OK** |
| F6 — `ajaxGetListCategory` | Function | Indirect | TC005 (reload → gọi list category) | 1 | RISK (chỉ 1 TC regression gián tiếp) |
| D — (không có data impact) | Data | — | N/A | — | N/A |
| T1 — Auto Reply bật/tắt rule | Feature | Medium | TC001, TC002, TC003, TC004, TC005, TC008, TC009, TC010 | 8 | **OK** |
| T2 — Auto Reply tìm kiếm từ khoá | Feature | Low | — | **0** | **GAP** |
| T3 — Auto Reply thêm/sửa thư mục | Feature | Low | TC006, TC011 | 2 | **OK** |
| T4 — Auto Reply huỷ sắp xếp (cancel sort) | Feature | Low | TC007, TC008 | 2 | **OK** |

### ORPHAN TCs (nếu có)

| TC ID | Title | Lý do orphan | Hành động đề xuất |
|---|---|---|---|
| — | — | Không có TC lạc chủ đề — toàn bộ 13 TC đều thuộc scope BUG / F* / T* hoặc checklist LME (staff account). | — |

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| Fix shape (đọc mục 2 dev-impact) | **Khác — "State-source fix"**: thay bộ chọn DOM quá rộng `$(.active).attr(data-id)` bằng state Vue `group_open` (nguồn dữ liệu chuẩn cho folder đang mở). KHÔNG phải generic-catch / validation / race / cache / migration / soft-delete. |
| Trigger space cần cover | Fix áp dụng cho **5 entry point** cùng dùng folder hiện tại: bật rule (`turnOnItem`), tắt rule (`turnOffItem`), search từ khoá (`searchByKeyWord`), thêm/sửa folder (`addGroup`), huỷ sort (`cancelSorted`). Mỗi entry point × 2 loại folder (folder tự tạo có `group_open != 0` / folder 未分類 có `group_open = 0`). |
| Số trigger TCs hiện cover | **4/5 entry point** — thiếu `searchByKeyWord`. Boundary `group_open=0` (未分類) có cover (TC009/010). |
| KH report dạng | **Symptom-only** — KH chỉ mô tả hiện tượng "màn nhảy sang folder khác", không nêu error/root cause. Dev đã xác định 1 root cause cụ thể (`$(.active)` bắt nhầm `#popupTerm`) có bằng chứng git log. |
| Alternative root causes cần verify | Xác suất thấp (root cause deterministic theo DOM, có evidence). Vẫn nên hỏi Dev: ngoài popup `#popupTerm`, còn phần tử `.active` nào khác trong header/sidebar có thể bị `$(.active)` bắt nhầm không? (fix `group_open` xử lý triệt để mọi trường hợp `.active`, nên regression risk thấp). |
| Anti-patterns dính | **AP-3** (Happy-path-only regression — thiếu edge state cho vài feature); nguy cơ **AP-5** thấp. AP-1/AP-2/AP-4/AP-6 KHÔNG dính (không generic-catch, mục 3 dev-impact có list caller đầy đủ, có commit hash). |

> Fix shape này là **multi-entry state-source fix** → rủi ro chính KHÔNG phải "trigger space error code" mà là **bỏ sót 1 entry point trong 5 hàm đã sửa**. Coverage matrix đã lộ đúng điểm đó: `searchByKeyWord` (F3) = GAP → flag BLOCKER §4.1.

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- **[BLOCKER] FIX-SHAPE / GAP-1 (F3, T2)**: Fix sửa `searchByKeyWord` để dùng `group_open` thay `$(.active)`, nhưng **không có TC nào** verify hành vi tìm kiếm auto reply theo từ khoá. Đây là 1 trong 5 entry point Direct đã đổi code → nếu sai, search sẽ lại nhảy về 未分類 mà không ai phát hiện. — **Fix**: thêm TC-NEW-01 (xem §5): search từ khoá trong folder tự tạo → verify màn giữ nguyên folder + reload vẫn đúng folder.

### 4.2 Major (nên fix)

- **[MAJOR] 01-bug-task.md auto-filled chưa verify**: File auto-fill `2026-07-01 by /new-task` nhưng checkbox "Tester verify auto-fill chính xác" **chưa tick** → yêu cầu tester đọc lại detail Redmine #38369 (description + steps) và tick checkbox trước khi review có giá trị. Đặc biệt: Steps to reproduce trong file 01 là **suy ra** từ mô tả (Redmine không có heading "Tái hiện bug" riêng) — cần tester confirm.
- **[MAJOR] 03-dev-impact.md auto-filled chưa verify**: File auto-fill `2026-07-01 by /new-task` nhưng checkbox "Tester verify auto-fill chính xác" **chưa tick** → F/D/T có thể chưa đầy đủ/mapping sai (đặc biệt mục 4.1 F2–F6 do `/new-task` tổng hợp thêm từ mục 3, không có sẵn trong report Dev). Yêu cầu tester đọc lại Redmine + tick checkbox.
- **[MAJOR] TC008 / TC009 / TC010: Steps trống** — 3 TC chỉ có Title + Expected, **không có Steps/Precondition** → không chạy được, 2 người chạy ra 2 kết quả khác nhau. Fix: điền Steps cụ thể (vd TC009: "1. Mở folder 未分類. 2. OFF một rule trong đó." / TC008: "1. Vào chế độ sort. 2. Kéo sắp xếp. 3. Thoát sort. 4. OFF một rule.").
- **[MAJOR] TC012 (send auto reply) / TC013 (account staff): thiếu Title/Steps** — TC012 không có Title + Steps (chỉ Expected "user nhận được action bình thường"); TC013 chỉ có Title "Check account staff", trống toàn bộ Steps/Expected. Đây là 2 regression quan trọng (auto reply **vẫn gửi được** sau fix + phân quyền staff — CL-Func-1). Fix: điền đủ (xem TC-NEW-02 gợi ý cho staff).
- **[MAJOR] SYMPTOM-ONLY (AP-2, mức nhẹ)**: KH report symptom-only. Dev đã có root cause cụ thể + bằng chứng, xác suất alternative root cause thấp — nhưng nên **hỏi Dev** xác nhận: ngoài `#popupTerm`, có phần tử `.active` nào khác (menu, sidebar, modal) đứng trước danh sách folder trong DOM có thể gây cùng symptom không. Fix `group_open` đã xử lý triệt để nên đây là câu hỏi confirm, không phải TC bắt buộc.

### 4.3 Minor (có thể fix sau)

- **[MINOR][AP-3] Thiếu regression edge-state cho vài feature**: TC006 (edit folder), TC011 (add folder), TC007 (cancel sort) chỉ chạy ở trạng thái "folder tự tạo bình thường". Nên có ít nhất 1 case thực hiện các thao tác này khi **đang ở folder 未分類** (group_open=0) để chắc boundary không bị nhảy.
- **[MINOR] TC006 Expected chưa đo lường chặt**: "Sau khi lưu vẫn ở folder vừa chỉnh sửa" — nên thêm "và tên folder hiển thị đúng giá trị mới, không reload về 未分類".
- **[MINOR] Compatibility (CL-NonF-1)**: Fix thuần frontend (jQuery DOM + Vue state) → hành vi có thể khác giữa Win/Mac × Chrome/Safari. Nên note 1 TC smoke cross-browser hoặc ghi rõ env test.
- **[MINOR] TC IDs**: Sheet gốc cột A trống → TC ID (`TC001`…) do `/new-task` sinh khi fetch. Member confirm lại ID chuẩn team trước khi sync ngược.

### 4.4 Nit (gợi ý)

- **[NIT] Thao tác liên tục (CL-Func-4)**: TC004 đã cover ON/OFF liên tục — có thể mở rộng thêm chuỗi "sort → edit folder → OFF rule" trong 1 TC để bắt state stale.
- **[NIT] Yokoten (đã vào scope)**: Dev đã fix bổ sung 7 màn cùng pattern `$(.active)` → xem §5.2 (TC tổ chức theo màn). Phần còn lại trong ~26 màn chưa fix vẫn cần ticket riêng — xem §6.

---

## 5. TCs đề xuất bổ sung

> Member copy vào `04-tc-list.md` ở round tiếp theo.

| TC ID gợi ý | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| TC-NEW-01 | [Auto reply] Search theo từ khoá trong folder không làm nhảy folder | Bot có ≥2 folder auto reply (A, B); folder A chứa ≥1 rule; đang mở folder A | 1. Mở màn Tự động trả lời, mở folder A.<br>2. Nhập từ khoá vào ô search auto reply.<br>3. Thực hiện search (Enter / nút tìm).<br>4. Xoá từ khoá / reload danh sách. | - Kết quả search hiển thị đúng trong phạm vi folder A.<br>- Màn **vẫn ở folder A**, KHÔNG nhảy về "未分類".<br>- Sau reload vẫn ở folder A. | High | Regression | **F3, T2, BUG** |
| TC-NEW-02 | [Auto reply] Account staff bật/tắt rule không nhảy folder + đúng phân quyền | 1 staff **được cấp quyền** Auto reply + 1 staff **không** được cấp quyền; bot có ≥2 folder | 1. Login staff có quyền → mở folder A → OFF/ON 1 rule.<br>2. Login staff không quyền → thử access màn Auto reply / URL trực tiếp. | - Staff có quyền: thao tác giống account chính, màn giữ nguyên folder A (không nhảy 未分類).<br>- Staff không quyền: bị từ chối access. | Medium | Regression | **CL-Func-1, F1, T1** |
| TC-NEW-03 | [Auto reply] Thao tác edit/add/cancel-sort khi đang ở folder 未分類 | Đang mở folder mặc định 未分類 (group_open=0), có ≥1 rule | 1. Ở folder 未分類 → đổi tên/thêm folder / vào sort rồi cancel / OFF 1 rule.<br>2. Reload danh sách. | - Sau mỗi thao tác vẫn ở đúng folder 未分類, KHÔNG nhảy folder khác.<br>- Reload giữ nguyên 未分類. | Medium | Boundary | **F4, F5, F1, BUG (group_open=0)** |

> Ngoài 3 TC mới, các TC008/009/010/012/013 **không cần thêm mới** — chỉ cần **điền đủ Precondition/Steps/Expected** (xem §4.2).

### 5.2 TCs bổ sung — Dev mở rộng fix (YOKOTEN 7 màn cùng pattern `$(.tag_left .active)`)

> **Bối cảnh**: Sau #38369, Dev **đã triển khai ngang (yokoten)** cùng cách fix sang **7 màn danh sách khác** cùng dính bug `$(.active)` quá rộng. **Cách fix**: scope selector thành **`$(.tag_left .active)`** (chỉ lấy tab folder trong sidebar trái `.tag_left`, bỏ qua `.active` khác như popup Điều khoản `#popupTerm`).
>
> **TC dưới đây được TỔ CHỨC THEO MÀN HÌNH** (mỗi màn 1 bảng). Trong mỗi màn:
> - **TC Dev sửa trực tiếp** (search / add-folder / cancel-sort — Map ghi `YOKOTEN ...`): scope kiểm thử chính.
> - **TC mở rộng** (switch-folder / reload / edit / delete / save-sort / liên tục / double-click / multi-tab / staff / chức năng chính / compatibility): theo quan điểm human + checklist LME, **phân bổ 3/7 màn** mỗi thao tác (xem §5.3 lý do + ma trận). Gồm cả **Gap-probe** — bắt Dev có fix ĐỦ operation chưa (FAIL = Dev sót → tạo issue).
> - **Pattern chung**: Precondition mặc định header render `#popupTerm`; mỗi thao tác phải giữ nguyên folder đang mở, KHÔNG nhảy folder mặc định, reload vẫn đúng folder.
> - **Boundary group_open=0** (folder mặc định) tách riêng ở cuối (TC-YOKO-50, chạy cả 7 màn).

#### FA-005 — Rich Menu Image Maker (リッチメニュー画像メーカー)

> Dev sửa trực tiếp: TC-YOKO-01, 02 · Mở rộng: TC-YOKO-03→07

| TC ID | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| TC-YOKO-01 | [FA-005 Rich Menu Image Maker] Add folder không nhảy folder | Màn Rich Menu Image Maker có ≥2 folder: 1 mặc định + folder B tự tạo; đang mở folder B; `#popupTerm` render | 1. Mở màn, mở folder B.<br>2. Thêm 1 folder mới (nhập tên → lưu).<br>3. Reload danh sách. | - Sau khi thêm: màn vẫn ở đúng folder đang thao tác, KHÔNG nhảy về folder mặc định.<br>- Reload vẫn đúng folder. | Medium | Regression | YOKOTEN `addGroup` FA-005 (Dev) |
| TC-YOKO-02 | [FA-005 Rich Menu Image Maker] Cancel sort trả về đúng folder | ≥2 folder, đang mở folder B | 1. Mở folder B.<br>2. Vào chế độ sort.<br>3. Bấm Cancel. | - Quay về đúng folder B, KHÔNG nhảy về folder mặc định. | Medium | Regression | YOKOTEN `cancelSorted` FA-005 (Dev) |
| TC-YOKO-03 | [FA-005 Rich Menu Image Maker] Điều hướng chuyển qua lại giữa folder — active + list đúng | ≥3 mục: folder mặc định + A + B (item khác nhau); `#popupTerm` render | 1. Mở folder A (verify list A).<br>2. Chuyển sang B.<br>3. Chuyển sang folder mặc định.<br>4. Quay lại A.<br>5. Reload ở A. | - Mỗi lần chuyển: folder click **active/highlight đúng** ở `.tag_left`, list đúng folder, KHÔNG nhảy nhầm.<br>- Reload giữ folder A. | High | Regression | Folder-detection core |
| TC-YOKO-04 | [FA-005 Rich Menu Image Maker][Gap-probe] Đổi tên folder đang mở không nhảy folder | Màn có sửa tên folder; đang mở folder B | 1. Mở folder B.<br>2. Đổi tên folder B → lưu.<br>3. Reload. | - Sau lưu vẫn ở folder B (tên mới), KHÔNG nhảy mặc định.<br>- ⚠️ Gap-probe: nhảy folder = Dev sót edit-folder. | Medium | Regression | Gap-probe (edit-folder) |
| TC-YOKO-05 | [FA-005 Rich Menu Image Maker][Gap-probe] Lưu (confirm) sắp xếp folder giữ folder + thứ tự | Màn có sort folder; ≥3 folder, đang mở B | 1. Mở folder B.<br>2. Vào sort.<br>3. Kéo đổi thứ tự.<br>4. **Lưu** sort.<br>5. Reload. | - Thứ tự lưu đúng; vẫn ở folder B; reload giữ thứ tự + folder.<br>- ⚠️ Gap-probe: nhảy folder = Dev sót save-sort (Dev chỉ list cancel-sort). | Medium | Regression | C.8 + Gap-probe |
| TC-YOKO-06 | [FA-005 Rich Menu Image Maker] Multi-tab + chuyển nhanh khi API folder chưa xong | Mở 2 tab cùng màn cùng bot | 1. Tab A mở folder A.<br>2. Tab B mở folder B, thêm folder / đổi thứ tự.<br>3. Về tab A thao tác (chưa reload).<br>4. Chuyển nhanh giữa folder khi list chưa load xong. | - KHÔNG ghi đè sai, KHÔNG nhảy folder ngẫu nhiên, KHÔNG lỗi count/duplicate.<br>- State mỗi tab nhất quán sau reload. | Medium | Boundary | CL-Func-25 + CL-Func-3 |
| TC-YOKO-07 | [FA-005 Rich Menu Image Maker] Chức năng chính vẫn hoạt động trong folder sau fix | Có data trong folder B | Trong folder B: tạo/chỉnh 1 richmenu image → áp dụng. | - Richmenu image tạo/áp dụng đúng trong folder B, KHÔNG lỗi do đổi selector. | High | Regression | Functional-regression |

#### FA-025 — Conversion (コンバージョン)

> Dev sửa trực tiếp: TC-YOKO-08, 09 · Mở rộng: TC-YOKO-10→14

| TC ID | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| TC-YOKO-08 | [FA-025 Conversion] Add folder không nhảy folder | Màn Conversion có ≥2 folder; đang mở folder B; `#popupTerm` render | 1. Mở folder B.<br>2. Thêm 1 folder mới.<br>3. Reload. | - Vẫn ở đúng folder, KHÔNG nhảy mặc định.<br>- Reload đúng folder. | Medium | Regression | YOKOTEN `addGroup` FA-025 (Dev) |
| TC-YOKO-09 | [FA-025 Conversion] Cancel sort trả về đúng folder | ≥2 folder, đang mở folder B | 1. Mở folder B.<br>2. Vào sort.<br>3. Cancel. | - Quay về đúng folder B, KHÔNG nhảy mặc định. | Medium | Regression | YOKOTEN `cancelSorted` FA-025 (Dev) |
| TC-YOKO-10 | [FA-025 Conversion] Reload (F5) khi đang mở folder tự tạo giữ nguyên folder | Đang mở folder B; `#popupTerm` render | 1. Mở folder B.<br>2. F5 reload. | - Sau reload vẫn ở folder B, list đúng, KHÔNG nhảy mặc định. | Medium | Regression | CL-Func-2 |
| TC-YOKO-11 | [FA-025 Conversion][Gap-probe] Xóa folder → điều hướng đúng + không ghost | Màn có xóa folder; ≥3 folder; folder C có data | 1. Mở folder B.<br>2. Xóa folder C.<br>3. Xóa folder đang mở B.<br>4. Reload. | - Xóa C → vẫn ở B. Xóa B → điều hướng hợp lệ.<br>- Data xử lý đúng, KHÔNG ghost.<br>- ⚠️ Gap-probe: nhảy sai = Dev sót delete-folder. | Medium | Regression | CL-Func-10 + Gap-probe |
| TC-YOKO-12 | [FA-025 Conversion] Thao tác liên tục không gây stale folder | ≥2 folder | Chạy chuỗi: add→add; add→sort→cancel; đổi tên→sort; xóa→add; sort→sort. | - Sau mỗi chuỗi: folder đang mở + active đúng, KHÔNG nhảy, KHÔNG stale. | Medium | Boundary | CL-Func-4 |
| TC-YOKO-13 | [FA-025 Conversion] Account staff thao tác folder đúng phân quyền | 1 staff có quyền + 1 staff không quyền | - Staff có quyền: mở folder B → add / cancel-sort → verify không nhảy.<br>- Staff không quyền: access URL màn trực tiếp. | - Staff có quyền: giống account chính, KHÔNG nhảy folder.<br>- Staff không quyền: bị redirect/chặn access. | Medium | Regression | CL-Func-1 + CL-NonF-2 |
| TC-YOKO-14 | [FA-025 Conversion] Compatibility Win/Mac × Chrome/Safari cho thao tác folder | — | Chạy add-folder + cancel-sort + chuyển folder trên: Win-Chrome, Mac-Chrome, Mac-Safari. | - Hành vi folder đồng nhất mọi trình duyệt, KHÔNG nhảy folder trên bất kỳ browser. | Low | Regression | CL-NonF-1 |

#### FA-015 — Friend Information (友だち情報)

> Dev sửa trực tiếp: TC-YOKO-15, 16 · Mở rộng: TC-YOKO-17→20

| TC ID | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| TC-YOKO-15 | [FA-015 Friend Information] Add folder không nhảy folder | Màn 友だち情報 có ≥2 folder (chưa phân loại + folder B tự tạo); đang mở folder B; `#popupTerm` render | 1. Mở folder B.<br>2. Thêm 1 folder mới.<br>3. Reload. | - Vẫn ở đúng folder, KHÔNG nhảy về "未分類"/default.<br>- Reload đúng folder. | High | Regression | YOKOTEN `addGroup` FA-015 (Dev) |
| TC-YOKO-16 | [FA-015 Friend Information] Cancel sort trả về đúng folder | ≥2 folder, đang mở folder B | 1. Mở folder B.<br>2. Vào sort.<br>3. Cancel. | - Quay về đúng folder B, KHÔNG nhảy "未分類"/default. | High | Regression | YOKOTEN `cancelSorted` FA-015 (Dev) |
| TC-YOKO-17 | [FA-015 Friend Information] Điều hướng chuyển qua lại giữa folder — active + list đúng | ≥3 folder (chưa phân loại + A + B, friend khác nhau); `#popupTerm` render | 1. Mở folder A (verify list A).<br>2. Chuyển sang B.<br>3. Chuyển sang "未分類".<br>4. Quay lại A.<br>5. Reload ở A. | - Mỗi lần chuyển: active đúng ở `.tag_left`, list friend đúng folder, KHÔNG nhảy nhầm về "未分類".<br>- Reload giữ folder A. | High | Regression | Folder-detection core |
| TC-YOKO-18 | [FA-015 Friend Information][Gap-probe] Xóa folder → điều hướng đúng + không ghost | Màn có xóa folder; ≥3 folder; folder C có friend | 1. Mở folder B.<br>2. Xóa folder C (khác folder đang mở).<br>3. Xóa folder đang mở B.<br>4. Reload. | - Xóa C → vẫn ở B. Xóa B → điều hướng folder hợp lệ (không lỗi).<br>- Friend trong folder xóa xử lý đúng theo spec, KHÔNG ghost.<br>- ⚠️ Gap-probe: nhảy sai = Dev sót delete-folder. | Medium | Regression | CL-Func-10 + Gap-probe |
| TC-YOKO-19 | [FA-015 Friend Information] Double click add-folder / lưu-sort không duplicate | — | Double click nhanh nút thêm folder / nút lưu sort. | - KHÔNG tạo folder trùng / lưu 2 lần; folder đang mở vẫn đúng. | Low | Boundary | CL-Func-5 |
| TC-YOKO-20 | [FA-015 Friend Information] Chức năng chính vẫn hoạt động trong folder sau fix | Có friend trong folder B | Trong folder B: xem list friend → mở 1 friend → sửa friend info → lưu. | - Friend info hiển thị/sửa/lưu đúng trong folder B, KHÔNG lỗi/regression do đổi selector. | High | Regression | Functional-regression |

#### FA-016 — Action Schedule (アクションスケジュール)

> Dev sửa trực tiếp: TC-YOKO-21, 22, 23 · Mở rộng: TC-YOKO-24→28

| TC ID | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| TC-YOKO-21 | [FA-016 Action Schedule] Search từ khoá không nhảy folder | Màn Action Schedule có ≥2 folder; folder B chứa data; đang mở folder B; `#popupTerm` render | 1. Mở folder B.<br>2. Nhập từ khoá vào ô search.<br>3. Search.<br>4. Xoá từ khoá / reload. | - Kết quả đúng phạm vi; màn vẫn ở folder B, KHÔNG nhảy mặc định.<br>- Reload vẫn folder B. | Medium | Regression | YOKOTEN `searchByKeyWord` FA-016 (Dev) |
| TC-YOKO-22 | [FA-016 Action Schedule] Add folder không nhảy folder | ≥2 folder, đang mở folder B | 1. Mở folder B.<br>2. Thêm 1 folder mới.<br>3. Reload. | - Vẫn ở đúng folder, KHÔNG nhảy mặc định.<br>- Reload đúng folder. | Medium | Regression | YOKOTEN `addGroup` FA-016 (Dev) |
| TC-YOKO-23 | [FA-016 Action Schedule] Cancel sort trả về đúng folder | ≥2 folder, đang mở folder B | 1. Mở folder B.<br>2. Vào sort.<br>3. Cancel. | - Quay về đúng folder B, KHÔNG nhảy mặc định. | Medium | Regression | YOKOTEN `cancelSorted` FA-016 (Dev) |
| TC-YOKO-24 | [FA-016 Action Schedule] Reload (F5) khi đang mở folder tự tạo giữ nguyên folder | Đang mở folder B; `#popupTerm` render | 1. Mở folder B.<br>2. F5 reload. | - Sau reload vẫn ở folder B, list đúng, KHÔNG nhảy mặc định. | Medium | Regression | CL-Func-2 |
| TC-YOKO-25 | [FA-016 Action Schedule][Gap-probe] Đổi tên folder đang mở không nhảy folder | Màn có sửa tên folder; đang mở folder B | 1. Mở folder B.<br>2. Đổi tên folder B → lưu.<br>3. Reload. | - Sau lưu vẫn ở folder B (tên mới), KHÔNG nhảy mặc định.<br>- ⚠️ Gap-probe: nhảy folder = Dev sót edit-folder. | Medium | Regression | Gap-probe (edit-folder) |
| TC-YOKO-26 | [FA-016 Action Schedule] Thao tác liên tục không gây stale folder | ≥2 folder | Chạy chuỗi: add→add; add→sort→cancel; đổi tên→sort; xóa→add; sort→sort. | - Sau mỗi chuỗi: folder + active đúng, KHÔNG nhảy, KHÔNG stale. | Medium | Boundary | CL-Func-4 |
| TC-YOKO-27 | [FA-016 Action Schedule] Multi-tab + chuyển nhanh khi API folder chưa xong | Mở 2 tab cùng màn cùng bot | 1. Tab A mở folder A.<br>2. Tab B mở folder B, thêm/đổi thứ tự.<br>3. Về tab A thao tác.<br>4. Chuyển nhanh folder khi list chưa load. | - KHÔNG ghi đè sai / nhảy folder / lỗi count.<br>- State mỗi tab nhất quán sau reload. | Medium | Boundary | CL-Func-25 + CL-Func-3 |
| TC-YOKO-28 | [FA-016 Action Schedule] Compatibility Win/Mac × Chrome/Safari cho thao tác folder | — | Chạy add-folder + cancel-sort + chuyển folder trên: Win-Chrome, Mac-Chrome, Mac-Safari. | - Hành vi folder **đồng nhất** mọi trình duyệt, KHÔNG nhảy folder trên bất kỳ browser. | Low | Regression | CL-NonF-1 |

#### FA-021 — Event Booking (イベント予約 — menu-v2, KHÔNG phải 旧/legacy)

> Dev sửa trực tiếp: TC-YOKO-29, 30 · Mở rộng: TC-YOKO-31→34 · ⚠️ Toàn bộ test trên màn **menu-v2**, verify không nhầm sang màn legacy.

| TC ID | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| TC-YOKO-29 | [FA-021 Event Booking v2] Add folder không nhảy folder | Màn イベント予約 **menu-v2** có ≥2 folder; đang mở folder B; `#popupTerm` render | 1. Mở màn Event Booking **v2**, mở folder B.<br>2. Thêm 1 folder mới.<br>3. Reload. | - Vẫn ở đúng folder, KHÔNG nhảy mặc định.<br>- Reload đúng folder.<br>- ⚠️ Verify đúng trên màn v2, không nhầm sang legacy. | High | Regression | YOKOTEN `addGroup` FA-021 v2 (Dev) |
| TC-YOKO-30 | [FA-021 Event Booking v2] Cancel sort trả về đúng folder | Màn v2, ≥2 folder, đang mở folder B | 1. Mở màn v2, mở folder B.<br>2. Vào sort.<br>3. Cancel. | - Quay về đúng folder B, KHÔNG nhảy mặc định (test trên v2). | High | Regression | YOKOTEN `cancelSorted` FA-021 v2 (Dev) |
| TC-YOKO-31 | [FA-021 Event Booking v2] Điều hướng chuyển qua lại giữa folder — active + list đúng | Màn v2 có ≥3 folder; `#popupTerm` render | 1. Mở màn v2, mở folder A.<br>2. Chuyển B → mặc định → quay lại A.<br>3. Reload ở A. | - Active + list đúng mỗi lần chuyển, KHÔNG nhảy nhầm (test trên v2).<br>- Reload giữ folder A. | High | Regression | Folder-detection core |
| TC-YOKO-32 | [FA-021 Event Booking v2][Gap-probe] Lưu (confirm) sắp xếp folder giữ folder + thứ tự | Màn v2 có sort folder; ≥3 folder, đang mở B | 1. Mở folder B.<br>2. Vào sort.<br>3. Kéo đổi thứ tự.<br>4. **Lưu** sort.<br>5. Reload. | - Thứ tự mới lưu đúng; sau lưu vẫn ở folder B; reload giữ thứ tự + folder.<br>- ⚠️ Gap-probe: nhảy folder = Dev sót save-sort. | Medium | Regression | C.8 + Gap-probe |
| TC-YOKO-33 | [FA-021 Event Booking v2] Double click add-folder / lưu-sort không duplicate | Màn v2 | Double click nhanh nút thêm folder / nút lưu sort. | - KHÔNG tạo folder trùng / lưu 2 lần; folder đang mở vẫn đúng. | Low | Boundary | CL-Func-5 |
| TC-YOKO-34 | [FA-021 Event Booking v2] Account staff thao tác folder đúng phân quyền | 1 staff có quyền + 1 staff không quyền màn v2 | - Staff có quyền: mở folder B → add / cancel-sort → verify không nhảy.<br>- Staff không quyền: access URL màn trực tiếp. | - Staff có quyền: giống account chính, KHÔNG nhảy.<br>- Staff không quyền: bị chặn access. | Medium | Regression | CL-Func-1 + CL-NonF-2 |

#### FA-026 — Single Product / Sales (商品/物販 — sales/v2)

> Dev sửa trực tiếp: TC-YOKO-35, 36, 37 · Mở rộng: TC-YOKO-38→42

| TC ID | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| TC-YOKO-35 | [FA-026 Single Product/Sales v2] Search từ khoá không nhảy folder | Màn 商品/物販 **sales/v2** có ≥2 folder; folder B chứa item; đang mở folder B; `#popupTerm` render | 1. Mở màn sales/v2, mở folder B.<br>2. Nhập từ khoá search.<br>3. Search.<br>4. Xoá/reload. | - Kết quả đúng; màn vẫn folder B, KHÔNG nhảy mặc định.<br>- Reload vẫn folder B. | Medium | Regression | YOKOTEN `searchByKeyWord` FA-026 v2 (Dev) |
| TC-YOKO-36 | [FA-026 Single Product/Sales v2] Add folder không nhảy folder | Màn sales/v2, ≥2 folder, đang mở folder B | 1. Mở folder B.<br>2. Thêm 1 folder mới.<br>3. Reload. | - Vẫn ở đúng folder, KHÔNG nhảy mặc định.<br>- Reload đúng folder. | Medium | Regression | YOKOTEN `addGroup` FA-026 v2 (Dev) |
| TC-YOKO-37 | [FA-026 Single Product/Sales v2] Cancel sort trả về đúng folder | Màn sales/v2, ≥2 folder, đang mở folder B | 1. Mở folder B.<br>2. Vào sort.<br>3. Cancel. | - Quay về đúng folder B, KHÔNG nhảy mặc định. | Medium | Regression | YOKOTEN `cancelSorted` FA-026 v2 (Dev) |
| TC-YOKO-38 | [FA-026 Single Product/Sales v2] Reload (F5) khi đang mở folder tự tạo giữ nguyên folder | Màn sales/v2 đang mở folder B; `#popupTerm` render | 1. Mở folder B.<br>2. F5 reload. | - Sau reload vẫn ở folder B, list đúng, KHÔNG nhảy mặc định. | Medium | Regression | CL-Func-2 |
| TC-YOKO-39 | [FA-026 Single Product/Sales v2][Gap-probe] Xóa folder → điều hướng đúng + không ghost | Màn sales/v2 có xóa folder; ≥3 folder; folder C có item | 1. Mở folder B.<br>2. Xóa folder C.<br>3. Xóa folder đang mở B.<br>4. Reload. | - Xóa C → vẫn ở B. Xóa B → điều hướng hợp lệ.<br>- Item xử lý đúng, KHÔNG ghost.<br>- ⚠️ Gap-probe: nhảy sai = Dev sót delete-folder. | Medium | Regression | CL-Func-10 + Gap-probe |
| TC-YOKO-40 | [FA-026 Single Product/Sales v2] Thao tác liên tục không gây stale folder | Màn sales/v2, ≥2 folder | Chạy chuỗi: add→add; add→sort→cancel; đổi tên→sort; xóa→add; sort→sort. | - Sau mỗi chuỗi: folder + active đúng, KHÔNG nhảy, KHÔNG stale. | Medium | Boundary | CL-Func-4 |
| TC-YOKO-41 | [FA-026 Single Product/Sales v2] Multi-tab + chuyển nhanh khi API folder chưa xong | Mở 2 tab cùng màn sales/v2 cùng bot | 1. Tab A mở folder A.<br>2. Tab B mở folder B, thêm/đổi thứ tự.<br>3. Về tab A thao tác.<br>4. Chuyển nhanh folder khi list chưa load. | - KHÔNG ghi đè sai / nhảy folder / lỗi count.<br>- State mỗi tab nhất quán sau reload. | Medium | Boundary | CL-Func-25 + CL-Func-3 |
| TC-YOKO-42 | [FA-026 Single Product/Sales v2] Chức năng chính vẫn hoạt động trong folder sau fix | Có product trong folder B | Trong folder B: xem list product → mở 1 product → thao tác xem/mua (test). | - Product hiển thị/mua đúng trong folder B, KHÔNG lỗi do đổi selector. | High | Regression | Functional-regression |

#### FA-024 — Cross Analysis (クロス分析)

> Dev sửa trực tiếp: TC-YOKO-43, 44 · Mở rộng: TC-YOKO-45→49 · ⚠️ Màn dùng `addGroupV2` → nội bộ gọi `addGroup` nên cũng bị ảnh hưởng.

| TC ID | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| TC-YOKO-43 | [FA-024 Cross Analysis] Add folder (addGroupV2 → addGroup) không nhảy folder | Màn Cross Analysis có ≥2 folder; đang mở folder B; `#popupTerm` render | 1. Mở folder B.<br>2. Thêm 1 folder mới (màn dùng `addGroupV2`, nội bộ gọi `addGroup`).<br>3. Reload. | - Vẫn ở đúng folder, KHÔNG nhảy mặc định.<br>- Reload đúng folder.<br>- Xác nhận `addGroupV2` cũng đã được fix theo. | Medium | Regression | YOKOTEN `addGroupV2`→`addGroup` FA-024 (Dev) |
| TC-YOKO-44 | [FA-024 Cross Analysis] Cancel sort trả về đúng folder | ≥2 folder, đang mở folder B | 1. Mở folder B.<br>2. Vào sort.<br>3. Cancel. | - Quay về đúng folder B, KHÔNG nhảy mặc định. | Medium | Regression | YOKOTEN `cancelSorted` FA-024 (Dev) |
| TC-YOKO-45 | [FA-024 Cross Analysis][Gap-probe] Đổi tên folder đang mở không nhảy folder | Màn Cross Analysis có sửa tên folder; đang mở folder B | 1. Mở folder B.<br>2. Đổi tên folder B → lưu.<br>3. Reload. | - Sau lưu vẫn ở folder B (tên mới), KHÔNG nhảy mặc định.<br>- ⚠️ Gap-probe: nhảy folder = Dev sót edit-folder → tạo issue patch `$(.tag_left .active)` cho rename. | Medium | Regression | Gap-probe (edit-folder) |
| TC-YOKO-46 | [FA-024 Cross Analysis][Gap-probe] Lưu (confirm) sắp xếp folder giữ folder + thứ tự | Màn Cross Analysis có sort folder; ≥3 folder, đang mở B | 1. Mở folder B.<br>2. Vào sort.<br>3. Kéo đổi thứ tự.<br>4. **Lưu** sort.<br>5. Reload. | - Thứ tự lưu đúng; vẫn ở folder B; reload giữ thứ tự + folder.<br>- ⚠️ Gap-probe: nhảy folder = Dev sót save-sort. | Medium | Regression | C.8 + Gap-probe |
| TC-YOKO-47 | [FA-024 Cross Analysis] Double click add-folder / lưu-sort không duplicate | Màn Cross Analysis | Double click nhanh nút thêm folder / nút lưu sort. | - KHÔNG tạo folder trùng / lưu 2 lần; folder đang mở vẫn đúng. | Low | Boundary | CL-Func-5 |
| TC-YOKO-48 | [FA-024 Cross Analysis] Account staff thao tác folder đúng phân quyền | 1 staff có quyền + 1 staff không quyền màn Cross Analysis | - Staff có quyền: mở folder B → add / cancel-sort → verify không nhảy.<br>- Staff không quyền: access URL màn trực tiếp. | - Staff có quyền: giống account chính, KHÔNG nhảy.<br>- Staff không quyền: bị chặn access. | Medium | Regression | CL-Func-1 + CL-NonF-2 |
| TC-YOKO-49 | [FA-024 Cross Analysis] Compatibility Win/Mac × Chrome/Safari cho thao tác folder | — | Chạy add-folder + cancel-sort + chuyển folder trên: Win-Chrome, Mac-Chrome, Mac-Safari. | - Hành vi folder đồng nhất mọi trình duyệt, KHÔNG nhảy folder trên bất kỳ browser. | Low | Regression | CL-NonF-1 |

#### Cross-cutting — Boundary group_open=0 (chạy cả 7 màn)

| TC ID | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| TC-YOKO-50 | [YOKOTEN][Boundary] Thao tác trên folder MẶC ĐỊNH (group_open=0) không nhảy lung tung | Đang mở **folder mặc định** (default/未分類, group_open=0) của từng màn trong 7 màn; `#popupTerm` render | Với **mỗi** màn (FA-005/025/015/016/021/026/024): ở folder mặc định → thực hiện đúng (các) thao tác đã fix của màn đó (add-folder / cancel-sort / search).<br>Reload sau mỗi thao tác. | - Sau mỗi thao tác vẫn ở **đúng folder mặc định**, KHÔNG nhảy sang folder khác.<br>- Reload giữ nguyên folder mặc định.<br>- (Boundary quan trọng: selector mới `$(.tag_left .active)` phải trả đúng cả khi folder active là mặc định.) | High | Boundary | YOKOTEN toàn bộ 7 màn (group_open=0) |

> **Coverage yokoten (tổng 50 TC-YOKO, tổ chức theo màn)**:
> - Mỗi màn gồm **TC Dev sửa trực tiếp** (Map ghi `... (Dev)`) + **TC mở rộng** (regression / gap-probe / checklist LME).
> - Số TC mỗi màn: FA-005 = 7 · FA-025 = 7 · FA-015 = 6 · FA-016 = 8 · FA-021 = 6 · FA-026 = 8 · FA-024 = 7 · Boundary chung = 1.
> - search chỉ FA-016 (TC-YOKO-21) + FA-026 (TC-YOKO-35) — đúng danh sách Dev báo.
> - ⚠️ Màn v2/legacy: **FA-021** menu-v2 (KHÔNG phải 旧), **FA-026** sales/v2, **FA-024** `addGroupV2`→`addGroup`.

### 5.3 Lý do & chiến lược phân bổ TC mở rộng (mỗi thao tác 3/7 màn)

> **Lý do test rộng hơn 3 thao tác Dev đụng code**: bộ TC human màn Auto reply gốc (file 04) KHÔNG chỉ test đúng hàm Dev sửa mà test **toàn bộ thao tác điều hướng folder**. Vì fix đổi **cơ chế xác định folder** (`$(.tag_left .active)`) dùng chung cả màn nên:
> 1. **Regression**: mọi thao tác đọc/điều hướng folder có thể bị ảnh hưởng phụ (switch-folder, reload, thao tác liên tục, chức năng chính) → verify không vỡ.
> 2. **Gap-probe (yokoten sót)**: thao tác Dev **KHÔNG list** (edit-folder, delete-folder, save-sort) có thể **vẫn còn bug `$(.active)` chưa fix** → **FAIL = Dev sót operation, tạo issue patch tiếp**.
> 3. **Checklist LME bắt buộc**: CL-Func-1/2/4/5/10, CL-Func-25, C.8, CL-NonF-1/2.
>
> **Chiến lược phân bổ (theo yêu cầu Leader)**: thay vì chạy mỗi thao tác mở rộng trên **cả 7 màn** (x7), **phân bổ mỗi thao tác cho 3 màn** (x3) — balanced để mỗi màn nhận ~4-5 thao tác mở rộng, giảm khối lượng mà vẫn có ≥3 mẫu/thao tác. Nếu 1 thao tác FAIL ở bất kỳ màn nào → nghi ngờ cả 7 màn → mở rộng test màn còn lại.

| Thao tác mở rộng | Loại | Chạy ở 3 màn | TC-YOKO |
|---|---|---|---|
| Điều hướng chuyển folder | Regression | FA-005, FA-015, FA-021 | 03, 17, 31 |
| Reload (F5) | Regression | FA-025, FA-016, FA-026 | 10, 24, 38 |
| Đổi tên folder | **Gap-probe** | FA-024, FA-005, FA-016 | 45, 04, 25 |
| Xóa folder | **Gap-probe** | FA-015, FA-026, FA-025 | 18, 39, 11 |
| Lưu (save) sort | **Gap-probe** | FA-021, FA-024, FA-005 | 32, 46, 05 |
| Thao tác liên tục | Boundary | FA-025, FA-016, FA-026 | 12, 26, 40 |
| Double click | Boundary | FA-015, FA-021, FA-024 | 19, 33, 47 |
| Multi-tab / API race | Boundary | FA-005, FA-016, FA-026 | 06, 27, 41 |
| Account staff | Regression | FA-025, FA-021, FA-024 | 13, 34, 48 |
| Chức năng chính | Regression | FA-015, FA-026, FA-005 | 20, 42, 07 |
| Compatibility | Regression | FA-016, FA-024, FA-025 | 28, 49, 14 |

> **Ưu tiên (nếu thiếu resource)**: nhóm **Gap-probe** (đổi tên / xóa folder / save-sort — TC-YOKO-04, 05, 11, 18, 25, 32, 39, 45, 46) chạy TRƯỚC vì có thể lộ Dev fix chưa đủ. Nhóm Boundary/Compatibility (double-click, compatibility) có thể giảm sau.

---

## 6. Spec update needed (nếu có)

- [x] Không cần update spec cho #38369 (bug fix đúng behavior spec, không đổi nghiệp vụ).
- [ ] Cần update spec

> **Cập nhật (yokoten đã vào scope)**: Ghi chú ban đầu là "~26 màn khác cùng bug `$(.active)` — ngoài scope". Nay **Dev đã fix bổ sung 7 màn** (FA-005/015/016/021/024/025/026) bằng selector scoped `$(.tag_left .active)` → đã có **50 TC-YOKO** ở §5.2 (tổ chức theo màn) cover phần này. **Còn lại các màn khác trong ~26 màn CHƯA được fix** → vẫn cần theo dõi ticket triển khai ngang riêng cho phần chưa làm (Leader confirm danh sách 7 màn đã fix vs tổng ~26 để biết còn sót màn nào).

---

## 7. Checklist đã chạy

- [x] A. Coverage — GAP F3/T2 (search)
- [x] B. Chất lượng từng TC — nhiều TC steps trống (TC008/009/010/012/013)
- [x] C. Chất lượng bộ TC tổng thể — thiếu Negative (chấp nhận được với bug navigation UI); tỷ lệ Positive/Boundary/Regression hợp lý
- [x] D. Spec alignment — không mâu thuẫn spec
- [x] E. Hành chính — TC ID do /new-task sinh (Sheet gốc trống), member confirm
- [x] F. Base checklist LME
  - [x] F.1 Checklist web — **CL-Func-2** (reload sau save: TC005 OK), **CL-Func-4** (thao tác liên tục: TC004 một phần), **CL-Func-1** (staff account: TC013 trống → TC-NEW-02), **CL-NonF-1** (compatibility: chưa cover, MINOR), **CL-NonF-5→2** (security URL: staff access — TC-NEW-02)
  - [x] F.2 Checklist job — **không liên quan** (fix thuần frontend JS, không chạm job/callback/Google sync)
  - [x] F.3 Các tính năng chung — **C.8 Sort** (Auto reply có trong danh sách 24 màn sort: cancel sort TC007/008 OK, save sort không bị chạm code); C.1-C.7 không liên quan (không bill/send-job/friend info/tag/google/plan)

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | | |
| Tester | (đã đọc & hiểu feedback) | |
