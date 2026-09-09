# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | `#36270 — [QL Popup] Sau khi tạo item không lưu folder_id → bị back về folder default` |
| Reviewer (Leader) | `<Leader verify>` |
| Tester được review | `<chưa điền trong 04>` |
| Ngày review | `2026-06-09` |
| Version TCs | `<chưa điền trong 04>` |
| Vòng review | `Round 1` |

> **Spec reference**: Không có `02-spec-reference.md` riêng → dùng `templates/LME-SYSTEM-SPEC.md` tổng. Không có spec riêng cho hành vi cookie folder của màn Popup; mọi suy luận behavior dựa trên mục 1+2 `03-dev-impact.md`.

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — Có issue BLOCKER/MAJOR, cần fix và review lại

**Lý do ngắn gọn**: Bộ TC cover rất tốt chiều "giữ folder sau thao tác" (T1), nhưng **bỏ trống chiều isolation** vốn là 1 nửa mục đích của fix ("clear cookie khi logout / đổi user **để tránh lẫn dữ liệu giữa các tài khoản**" + cookie lưu **theo từng bot**): không có TC đa-bot, không có TC đổi-user, và **TC-PFP-020 có Expected mâu thuẫn với cách fix**. Thêm 2 checkbox "Tester verify auto-fill" ở 01/03 chưa tick → review chưa có nền tảng chắc chắn.

---

## 2. Tóm tắt cho member

Bộ TC rất chắc ở phần chính: 32 case cover gần như đủ mọi thao tác giữ folder (tạo/sửa/copy/xóa/move/sort/back/validation) ở cả folder default lẫn non-default — phần này làm tốt, có cả case folder ở giữa danh sách (TC-024) và case rời form không lưu (TC-021/022). **Điểm cần fix**: fix này không chỉ "nhớ folder" mà còn **cô lập cookie theo bot và xóa cookie khi logout/đổi user**; bộ TC gần như chưa chạm nửa sau này — thiếu hẳn case **2 bot**, case **đổi sang user khác**, và **TC-PFP-020 đang expect ngược với fix** (fix clear cookie khi logout, nhưng TC lại expect vẫn nhớ folder). Bổ sung các TC isolation ở §5 + confirm lại hành vi logout với Dev là đủ để pass.

---

## 3. Coverage Matrix

| Impact | Loại | Priority | TCs map (suy luận) | # TC | Status |
|---|---|---|---|---|---|
| BUG — tạo item xong giữ đúng folder (không về default) | Fix | — | TC-001, TC-002, TC-031 | 3 | **OK** |
| F1 — route `popupSetCookie` (`/basic/popup/set-cookie`) | Function | Direct | TC-001, TC-005 (gián tiếp qua đổi folder) | 2 | OK |
| F2 — `folderSetCookie()` case `popup` (set cookie) | Function | Direct | TC-001, TC-003, TC-005 (đổi folder → lưu cookie) | nhiều | OK |
| F3 — `PopupController@index` đọc/**validate** cookie (đúng bot / đúng kind / chưa xóa → reset 0) | Function | Direct | TC-002, TC-026 (chỉ nhánh "folder bị xóa", 1 phần) | 1–2 | **RISK** — thiếu nhánh "đúng bot" & "đúng kind" & stale-cookie reload |
| F4 — `created()` đọc cookie set `group_open` khi load | Function | Direct | TC-002, TC-023 (reload / browser back) | 2 | OK |
| F5 — `showGroup()` ajax lưu cookie khi đổi folder | Function | Direct | TC-005, TC-014 (click qua lại folder) | 2 | OK |
| F6 — blade truyền `folder_cookie` + route cho JS | Function | Direct | TC-001 (render đúng folder) | gián tiếp | OK |
| F7 — `loginUserById()` clear cookie khi đổi/đăng nhập user khác | Function | Indirect | TC-019 (chỉ verify "thao tác bình thường", KHÔNG verify cookie không lẫn) | 1 | **RISK → GAP chiều isolation** |
| F8 — `logout()` clear cookie khi logout | Function | Indirect | TC-020 (**Expected mâu thuẫn fix**) | 1 | **GAP / sai expected** |
| D1 — Cookie `folder_popup` (lưu theo từng bot; CREATE/UPDATE/DELETE) | Data | — | CREATE/UPDATE: TC-001..TC-018 (nhiều); DELETE khi logout: TC-020 (sai); boundary đa-bot/stale: — | nhiều | **RISK** — thiếu negative (đa-bot, đổi user) + boundary (cookie trỏ folder đã xóa) |
| T1 — Màn Quản lý Popup: giữ folder sau thao tác | Feature | Medium(High thực tế) | TC-001..018, TC-021..031 | ~28 | **OK** |
| T2 — Luồng logout / đăng nhập user khác (clear cookie) | Feature | Medium | TC-019, TC-020 | 2 | **GAP** — không có case verify cookie KHÔNG lẫn giữa user/bot |

### ORPHAN / Over-coverage TCs

| TC ID | Title | Lý do | Hành động đề xuất |
|---|---|---|---|
| TC-012, TC-013, TC-032 | "...+ gán/gửi action cho Popup thành công" | Phần "gửi action" của Popup **không thuộc** code path fix lần này (fix chỉ chạm cookie folder). Xem AP-5 / memory root-cause-layer-focus. | Giữ phần verify folder; **bỏ hoặc tách** phần verify gửi action thành regression riêng, không tính là cover fix. |

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| Fix shape (mục 2 dev-impact) | **Specific code check / Validation** — thêm cơ chế cookie `folder_popup` + `PopupController@index` validate folder (`đúng bot` / `đúng kind` / `chưa xóa`) → nếu invalid reset về 0. Kèm **state-cleanup** (clear cookie khi logout/đổi user). KHÔNG phải generic catch-all. |
| Trigger space cần cover | (1) tạo/sửa/copy/xóa/move/sort → giữ folder ✅; (2) reload/back → đọc lại cookie ✅; (3) **validate reset**: cookie trỏ folder của **bot khác** ❌ / folder **kind khác** ❌ / folder **đã xóa** ⚠️(1 phần qua TC-026); (4) **clear cookie**: logout ⚠️(TC-020 sai expected) / **đổi user** ❌. |
| Số trigger TCs hiện cover | Nhóm (1)(2): đầy đủ. Nhóm (3)(4) — **cô lập/validate**: ~1/5 (chỉ TC-026 chạm 1 phần nhánh "folder đã xóa"). |
| KH report dạng | **Có root cause cụ thể** — Dev xác định rõ "màn popup chưa có cookie ghi nhớ folder, `group_open` luôn về 0 sau reload". Không phải symptom-only thuần (AP-2 nhẹ). |
| Alternative root causes cần verify | N/A đáng kể (root cause rõ + có PR). Lưu ý 1 biến thể: redirect sau create có thể mất folder qua URL param thay vì cookie — Dev đã chọn hướng cookie, không cần TC thêm. |
| Anti-patterns dính | **AP-3** (happy-path-only regression cho T2: logout/đổi user chỉ có case "thao tác bình thường", thiếu negative isolation); **AP-5** (over-coverage "gửi action" ở TC-012/013/032); AP-4 nhẹ (nên enumerate 3 điều kiện validate của F3 để cover từng cái). AP-1/AP-2/AP-6 **không dính** (mục 3 có list caller, fix không generic-catch). |

> Trigger space nhóm (3)(4) cover **< tổng** → flag ở §4.1 / §4.2.

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- **[BLOCKER] FIX-SHAPE — TC-PFP-020**: Expected **mâu thuẫn cách fix**. Fix ghi rõ *"Clear cookie `folder_popup` khi logout / đổi user"*, nhưng TC-020 expect *"sau khi login lại sẽ mở vào folder đã chọn ở bước 1"* (tức **vẫn nhớ** folder). Nếu cookie thực sự bị clear khi logout thì sau re-login phải mở **folder default 未分類**, không phải folder cũ → Expected hiện tại SAI. **Đề xuất**: confirm với Dev hành vi đúng cho case **logout rồi login lại CHÍNH user đó**; sửa Expected TC-020 cho khớp fix (xem TC-NEW-03). Đây là điểm dễ làm tester pass nhầm 1 TC verify sai bản chất fix.

- **[BLOCKER] FIX-SHAPE / GAP-iso — Đa bot (cookie lưu "theo từng bot" + validate "đúng bot")**: Fix lưu cookie `folder_popup` riêng theo bot và `PopupController@index` validate folder phải **đúng bot** mới giữ. **Không có TC nào** chuyển giữa 2 bot. Rủi ro lọt prod: cookie folder của Bot A áp nhầm sang Bot B → hiển thị sai folder hoặc lỗi (lẫn dữ liệu giữa account). Liên quan **CL11** (CRUD đúng account/bot). **Đề xuất**: thêm TC-NEW-01.

### 4.2 Major (nên fix)

- **[MAJOR] GAP-iso — Đổi user (F7 `loginUserById` clear cookie)**: Mục đích nửa-sau của fix là *"tránh lẫn dữ liệu giữa các tài khoản"*, nhưng **không có TC** verify: User A chọn folder X → đổi sang User B (super admin login-as / login user khác) → User B phải thấy folder default, **không** thấy folder X của A. TC-019 chỉ verify "thao tác bình thường", không verify isolation. **Đề xuất**: TC-NEW-02.

- **[MAJOR] FIX-SHAPE — Validate F3 chưa đủ nhánh**: `PopupController@index` reset về 0 khi folder **không hợp lệ** (đúng bot / đúng kind / **chưa xóa**). Chỉ TC-026 chạm 1 phần nhánh "folder bị xóa" (xóa folder đang active trong cùng phiên). Thiếu case **stale cookie**: cookie trỏ folder đã bị xóa ở tab/phiên khác → reload màn popup → phải reset về default, **không lỗi/blank**. **Đề xuất**: TC-NEW-04 (+ TC-NEW-05 cho nhánh "kind khác", có thể whitebox/Dev hỗ trợ set cookie).

- **[MAJOR] AUTO-FILL chưa verify — `01-bug-task.md`**: Field "Auto-filled: 2026-06-09 by /new-task" nhưng checkbox **"Tester verify auto-fill chính xác" CHƯA tick**. Yêu cầu tester đọc lại detail Redmine #36270 (mô tả + steps) và tick trước khi review có giá trị.

- **[MAJOR] AUTO-FILL chưa verify — `03-dev-impact.md`**: Tương tự, checkbox verify chưa tick. F1–F8 / D1 / T1–T2 có thể chưa đủ hoặc mapping sai — đề nghị tester đối chiếu lại với journal Dev + PR Bitbucket rồi tick.

### 4.3 Minor (có thể fix sau)

- **[MINOR] CL5 — Double click tạo popup**: Fix đổi flow save (showGroup ajax + redirect). Chưa có TC double-click nút tạo/lưu popup → verify không duplicate bản ghi + folder vẫn đúng. Đề xuất TC-NEW-06.
- **[MINOR] CL7 / multi-tab — Cookie dùng chung 2 tab**: Mở 2 tab màn popup, đổi folder ở tab 1, tạo popup ở tab 2 → cookie shared có thể gây folder không nhất quán. Chưa có TC. Đề xuất TC-NEW-07.
- **[MINOR] `01` — Môi trường phát hiện = `<chưa rõ>`**: Redmine không ghi rõ Production/Staging. Tester điền để cố định env reproduce.
- **[MINOR] `03` — Branch = `<chưa rõ>`**: Chỉ có PR Bitbucket #10229, không có tên branch. Bổ sung nếu cần trace code.
- **[MINOR] Phân loại Type**: 32 TC chỉ có `Positive` / `Edge Case`, không có nhãn `Negative` rõ ràng cho các case isolation/validate (vốn mang tính negative). Khi thêm TC-NEW, gắn đúng Type để tỷ lệ P/N/B/R cân bằng hơn.

### 4.4 Nit (gợi ý)

- **[NIT][AP-5] TC-012 / TC-013 / TC-032**: phần "gán/gửi action cho Popup" nằm ngoài scope cookie-fix → cân nhắc tách thành regression riêng hoặc bỏ để bộ TC tập trung đúng impact.
- **[NIT] Regression màn dùng chung `folderSetCookie`**: fix chỉ THÊM case `popup` (không sửa case cũ) → rủi ro thấp; nếu muốn chắc, thêm 1 smoke regression cho 1 màn liền kề dùng cookie folder (vd Template/Tag) vẫn nhớ folder đúng.

---

## 5. TCs đề xuất bổ sung

> Member copy vào `04-tc-list.md` ở round tiếp theo. Map to Impact ghi theo tag F/D/T + mục checklist LME.

| TC ID gợi ý | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| TC-NEW-01 | Đa bot — cookie folder Popup cô lập theo từng bot | Admin sở hữu ≥ 2 bot (Bot A, Bot B); mỗi bot có ≥ 1 folder popup non-default. | 1. Vào Bot A → màn Popup → chọn folder X (non-default)<br>2. Chuyển sang Bot B → vào màn Popup<br>3. Chuyển lại Bot A → vào màn Popup | - Bot B mở **folder default 未分類** (hoặc folder đã chọn trước đó CỦA RIÊNG Bot B), KHÔNG dùng cookie folder X của Bot A<br>- Bot A vẫn nhớ đúng folder X<br>- Không lỗi/blank | High | Negative (isolation) | F2, F3 (đúng bot), D1, CL11 |
| TC-NEW-02 | Đổi user — cookie folder Popup không lẫn giữa tài khoản | 2 tài khoản admin khác nhau (hoặc super admin login-as 2 user) cùng truy cập màn Popup. | 1. User A đăng nhập → màn Popup → chọn folder X (non-default)<br>2. Logout A / đổi sang User B (login-as hoặc login trực tiếp)<br>3. User B vào màn Popup | - User B mở **folder default 未分類**, KHÔNG thấy folder X của A (cookie đã clear khi đổi user)<br>- Không lỗi | High | Negative (isolation) | F7 `loginUserById`, F8 `logout`, D1, T2, CL11 |
| TC-NEW-03 | Logout rồi login lại CHÍNH user — cookie đã clear (thay/đối chiếu TC-020) | 1 tài khoản admin; đang ở màn Popup. | 1. Chọn folder X (non-default)<br>2. Logout<br>3. Login lại đúng user đó<br>4. Vào màn Popup | - Theo fix "clear cookie khi logout" → màn Popup mở **folder default 未分類** (KHÔNG nhớ folder X)<br>⚠ **Confirm hành vi đúng với Dev**: nếu spec muốn giữ folder khi same-user re-login thì fix/clear-on-logout cần xem lại | High | Positive (verify cleanup) | F8 `logout`, D1, T2 |
| TC-NEW-04 | Stale cookie — folder đã bị xóa → reload reset về default, không lỗi | Có folder non-default X chứa cookie đang trỏ tới; có cách xóa X (tab/phiên khác). | 1. Chọn folder X (set cookie `folder_popup`=X)<br>2. Ở tab/phiên khác (hoặc account có quyền) xóa folder X<br>3. Quay lại reload màn Popup ban đầu | - `PopupController@index` validate thấy folder X không còn → **reset về folder default 未分類**<br>- Màn list hiển thị đúng default, KHÔNG lỗi / KHÔNG trang trắng | Medium | Boundary | F3 (chưa xóa), D1 |
| TC-NEW-05 | Cookie trỏ folder sai kind/bot → validate reset default (whitebox) | Có thể set thủ công cookie `folder_popup` = id folder thuộc kind khác (vd template) hoặc bot khác. | 1. Set cookie `folder_popup` = folder id không thuộc kind popup / không thuộc bot hiện tại<br>2. Load màn Popup | - Validate fail → reset `group_open` về 0 → mở folder default, không lỗi | Low | Negative | F3 (đúng kind / đúng bot) |
| TC-NEW-06 | Double click nút tạo/lưu Popup ở folder non-default | Đang ở folder non-default. | 1. Chọn folder non-default<br>2. Tạo mới Popup, nhập hợp lệ<br>3. **Double click** nhanh nút「保存」 | - Chỉ tạo **1** Popup (không duplicate)<br>- List giữ đúng folder vừa thao tác, không về default | Medium | Boundary | T1, D1, CL5 |
| TC-NEW-07 | Multi-tab — cookie folder dùng chung giữa 2 tab | Mở màn Popup trên 2 tab cùng bot/user. | 1. Tab 1: chọn folder X<br>2. Tab 2: chọn folder Y rồi tạo Popup<br>3. Quan sát cả 2 tab sau reload | - Hành vi folder nhất quán theo cookie mới nhất (Y), không lỗi/blank ở tab nào; xác nhận không reset bừa về default | Low | Edge Case | D1, CL7 (multi-tab) |

---

## 6. Spec update needed (nếu có)

- [x] Không cần update spec (chưa có `02-spec-reference.md`; behavior cookie folder thuần internal, dựa mục 1+2 dev-impact)
- [ ] Cần update spec
- ⚠ **1 điểm cần Dev/PM chốt behavior** (không phải spec doc, nhưng ảnh hưởng Expected TC): **logout rồi login lại CHÍNH user** → có giữ folder cũ không? (liên quan TC-020 / TC-NEW-03). Chốt xong mới finalize Expected.

---

## 7. Checklist đã chạy

- [x] A. Coverage — A.1 BUG OK; A.2 Function (F3/F7/F8 thiếu chiều isolation); A.3 Data (D1 thiếu negative đa-bot/đổi user + boundary stale); A.4 Feature (T1 OK, T2 GAP); A.5 ORPHAN (TC-012/013/032 over-coverage); A.6 Fix-shape (xem §3.5)
- [x] B. Chất lượng từng TC — Title/Steps/Expected nhìn chung rõ; TC-020 expected sai bản chất
- [x] C. Chất lượng bộ TC — thiếu nhãn Negative cho isolation; phân bổ Priority hợp lý
- [x] D. Spec alignment — không có spec riêng (dùng LME-SYSTEM-SPEC tổng)
- [x] E. Hành chính — `04` chưa điền Tester/Version/Ngày submit (nhắc member điền)
- [x] F. Base checklist LME
  - [x] F.1 Web — **CL5** (double click) GAP → TC-NEW-06; **CL11** (CRUD đúng bot) GAP → TC-NEW-01; CL1 (staff) OK qua TC-025; CL2 (reload sau save) OK; CL4 (thao tác liên tục) OK qua TC-003/004/007; CL8/C.8 Sort OK qua TC-003/004/013
  - [x] F.2 Job — không chạm callback / google sync → N/A
  - [x] F.3 C.1–C.7 — không chạm bill/send msg/friend info/tag/google sheet/calendar/plan limit → N/A; **C.8 Sort** OK; **CL7 multi-tab** GAP → TC-NEW-07

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | | |
| Tester | (đã đọc & hiểu feedback) | |
