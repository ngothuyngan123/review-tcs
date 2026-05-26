# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | `KH-36384` — [Redmine #36384](https://redmine.watermelon.vn/issues/36384) |
| Reviewer (Leader) | _Pending_ — draft do Claude sinh, Leader verify |
| Tester được review | Ngô Thúy Ngần |
| Ngày review | 2026-05-14 |
| Version TCs | v1 |
| Vòng review | Round 1 |

---

## 1. Verdict

- [ ] **APPROVED** — TCs đạt, không cần chỉnh sửa
- [ ] **APPROVED WITH CHANGES** — Approve sau khi fix các issue MINOR (không cần review lại)
- [x] **REJECTED** — Có issue BLOCKER/MAJOR, cần fix và review lại

**Lý do ngắn gọn**: Bộ TCs cover tốt **regression** cho 2 feature impact (T1 Edit, T2 Save template) ở cả folder default lẫn folder khác, nhưng **bỏ lọt 3 GAP BLOCKER** quan trọng: (1) không có TC reproduce flow KH thật (URL chứa `/?utm_*`), (2) không có TC boundary cho input `template_child_id` chứa ký tự đặc biệt (chính là root cause), (3) không có TC standalone verify "click folder không lỗi" — chính là behavior user-facing mà KH báo.

---

## 2. Tóm tắt cho member

Bộ TC 56 case của em đã **cover rất chắc regression** cho 2 nhóm tính năng bị ảnh hưởng (Edit / Save template, cả 2 loại folder, đủ 7 loại template con) — đây là điểm tốt, đảm bảo fix không phá tính năng cũ. Tuy nhiên **chưa có TC nào reproduce trực tiếp flow KH** (paste URL kèm hậu tố `utm_*` → click Save) và **chưa có TC boundary** cho input `template_child_id` (string vs int, chứa `/?utm`, alphabetic, max length...) — đây chính là root cause fix, cần bổ sung trước khi merge. Ngoài ra checkbox "Tester verify auto-fill" ở `01-bug-task.md` chưa tick — em đọc lại detail Redmine #36384 và tick xác nhận giúp.

---

## 3. Coverage Matrix

> Mapping suy luận từ Title / Steps / Expected của 56 TCs trong `04-tc-list.md`. File 04 không có cột "Map to Impact" — Claude infer.

| Impact | Loại | Priority Dev đánh giá | TCs map | # TC | Status |
|---|---|---|---|---|---|
| **BUG (root cause)** — reproduce flow KH với URL chứa `/?utm_*` | Fix | — | _(none)_ | **0** | **GAP** |
| **F1 — `createTemplate`** (`app/Http/Controllers/Basic/TemplateV2Controller.php`) | Function | Direct | TC001-056 (mọi TC đều đi qua createTemplate khi tạo/edit/save) | 56 | **RISK** — có TC nhưng **thiếu boundary** cho input gây bug (`template_*_id` dạng `int/?utm`) |
| **D1** | Data | — | _(D1 = none — dev journal ghi rõ "k có")_ | N/A | N/A |
| **T1 — Edit template** | Feature | Medium | TC013-025 (folder default: edit group, edit từng loại template con + edit template đơn), TC041-053 (folder khác default tương tự) | 26 | **OK** |
| **T2 — Save template** | Feature | Medium | Mọi TC đều có bước Save → cover toàn bộ | 56 | **OK** |
| **T-implicit — List template / Click folder template** (trigger user-visible của bug, Ngần đã flag trong dev impact) | Feature | High (KH-visible) | Một số TC có ghi note "back ra list template, verify không error" trong Steps (TC001-056) — không TC standalone | 0 (standalone) | **GAP** — không có TC nào có title/scope chính là "Click folder template hiển thị list bình thường" |
| **Boundary input `template_*_id`** (chính là cách fix — ép `int`) | Function (sub-coverage F1) | High | _(none)_ | **0** | **GAP** |

### ORPHAN TCs (nếu có)

Không có ORPHAN. Cả 56 TCs đều thuộc scope F1 / T1 / T2.

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- **[BLOCKER] GAP-1 — Không TC nào reproduce flow KH thật**: Bug task ghi rõ reproduction (journal #118361): paste URL `/basic/template-v2/add-template?template_group_id=13305886&template_child_id=13305944/?utm_source=line&utm_medium=social&utm_id=syanai20260515` → Save template con → back ra list folder → lỗi. Toàn bộ 56 TCs **không có case nào** mô phỏng đúng flow này. Đây là yêu cầu §A.1 trong [framework/review-checklist.md](../../framework/review-checklist.md) — TC root cause **bắt buộc**. Đề xuất TC bổ sung: xem TC-NEW-01.
- **[BLOCKER] GAP-2 — Không TC boundary cho input `template_child_id` chứa ký tự đặc biệt**: Bug root cause là parse `template_child_id=13305944/?utm_source=line` thành nguyên string thay vì int `13305944`. Fix là ép `int`. Không có TC nào verify ép int hoạt động đúng với input: chuỗi chứa `/`, `?`, `=`, `&`, `#`; alphabetic không phải số; negative; float; max length; empty string. Đề xuất TC bổ sung: xem TC-NEW-02, TC-NEW-07.
- **[BLOCKER] GAP-3 — Không TC standalone verify "click folder template hiển thị list bình thường"**: Đây là behavior **user-facing** mà KH report (`テンプレートフォルダ「定期配信用」をクリックするとエラーが表示される`). 56 TCs đều flow create / edit / copy / save — không TC nào **chỉ riêng** click vào folder và verify list render. Mọi TC chỉ có note "back ra list template, verify không error" ở step cuối — không atomic. Đề xuất: xem TC-NEW-03.

### 4.2 Major (nên fix)

- **[MAJOR] 01-bug-task — Checkbox "Tester verify auto-fill chính xác" chưa tick**: File auto-filled `2026-05-14 by /write-tc (fetch qua MCP redmine)`. Per `/review-tc` protocol, member phải đọc lại detail Redmine (description + 3 journals + attachment) rồi tick checkbox xác nhận đầy đủ. Hiện chưa tick → review trên file 01 chưa đủ độ tin cậy.
- ~~[MAJOR] 02-spec-reference — File còn nguyên template, chưa có spec reference~~ → **RESOLVED 2026-05-14**: đã fill `02-spec-current.md` (tham chiếu LME-SYSTEM-SPEC §3.8 FA-010 + api-spec EP-30). **Phát hiện thêm**: spec API ghi rõ `template_child_id: integer` — bug 36384 là **implementation gap** (code chưa enforce kiểu), KHÔNG phải spec gap.
- **[MAJOR] Dev impact F1 chỉ liệt kê 1 function — và có mismatch với spec endpoint**: Journal Ngần đã raise nghi vấn (mục 3 trong `03-dev-impact.md`): có thể còn `storeTemplate`/`updateTemplate`/`cloneTemplate` cùng pattern parse query string từ request. **Bổ sung 2026-05-14** sau khi đọc spec: [api-spec EP-30 (line 244-246)](../../spec-features/admin/message-template/web/api-spec.md) ghi save endpoint là `POST /ajax/template-v2/save-template` → delegate sang `TemplateV2Service@saveTemplateByType()`. Nhưng dev impact F1 ghi fix nằm ở `createTemplate` trong `TemplateV2Controller`. **Có thể là 2 endpoint khác nhau** (controller create vs service save). Cần Dev confirm: (a) endpoint nào KH thực tế hit, (b) fix có cover cả 2 không. Nếu chỉ fix `createTemplate` mà KH thực tế hit `save-template` → bug **vẫn còn** sau fix.
- **[MAJOR] Checklist LME §A.2 Security không cover**: Bug này gốc là **input injection qua URL** (user paste URL với query lạ → server parse sai → corrupt DB). Checklist LME §A.2 Security yêu cầu test "đổi param ID URL bằng của user/bot khác → từ chối access". Không TC nào test security tại đây. Đề xuất TC-NEW-04 (cross-account access) + TC-NEW-08 (URL injection trên user/bot khác).
- **[MAJOR] Checklist LME §A.1 CL11 (CRUD đúng bản ghi account)**: Bug 36384 đã làm corrupt content của `template_group_id=13305886` trên bot KH thật. Không TC nào verify bug có lây sang account/bot khác không (vd: nếu user paste URL `template_group_id=X` từ bot khác → hệ thống có save sai content của bot khác không?). Cần TC verify `WHERE bot_id`.
- **[MAJOR] Checklist LME §A.1 CL22 (Upload file — preview trước/sau save)**: Bug làm content template (string của các template_child_id) sai sau khi save. CL22 yêu cầu verify preview / path **trước và sau khi save** giống nhau. TC hiện có note "verify hiển thị ở list / edit / preview" trong Expected nhưng **không tách step kiểm tra trước-sau** rõ ràng. Đề xuất tách step.
- **[MAJOR] Recovery verification — data production**: Journal #118251 ghi Ngọc Ánh đã recover bug data `template_group_id=13305886` ngày 2026-05-13. Không TC nào verify data sau recover (content = `13305887,13305944` thay vì `13305887,13305944/?utm_source=line`). Cần TC-NEW-05.

### 4.3 Minor (có thể fix sau)

- **[MINOR] TC Type phân loại thiếu chiều**: 56/56 TCs đều label `Regression`. Không có TC label `Positive` (verify fix hoạt động), `Negative` (input invalid), `Boundary` (giá trị biên). Đề xuất re-label các TC mới bổ sung (TC-NEW-*) và relabel một số TC hiện tại (vd TC028, TC056 duplicate-click save → `Negative`).
- **[MINOR] TC IDs trùng namespace**: Đang dùng `TC001`-`TC056` flat. Khi push lên sheet master cùng với TCs của bug khác sẽ trùng. Đề xuất prefix theo bug ID, vd `KH36384-TC001` hoặc dùng row trace sẵn có `(sheet R574)`.
- **[MINOR] Title TC dài**: Sau khi flatten hierarchy, title một số TC ~150 ký tự (vd TC003 lồng 6 cấp). Đề xuất rút gọn: bỏ phần `Sub5` mô tả dài, đẩy vào Precondition hoặc Output note.
- **[MINOR] Steps cuối dùng số `N` / `N+1`**: Manual tester đọc hơi confusing. Đề xuất đánh số cụ thể (vd 6, 7).
- **[MINOR] Folder slug `template-folder-click-error`**: Tên đúng theo subject KH báo nhưng không phản ánh root cause (URL utm-suffix). Đề xuất rename `template-utm-suffix-parse-error` để future search dễ hơn (optional).

### 4.4 Nit (gợi ý)

- **[NIT] 28 TCs folder default + 28 TCs folder khác default đối xứng**: Logic test giống hệt nhau, chỉ khác Precondition (folder loại nào). Có thể merge thành 1 nhóm 28 TC với column "Variant" hoặc Precondition liệt kê 2 loại folder. Nhưng nếu team prefer split để chạy nhanh trên sheet → giữ nguyên.
- **[NIT] Không có TC i18n / locale**: Bug data có ký tự JP (`定期配信用`). Có thể thêm 1 TC verify name folder có ký tự JP + emoji + ký tự đặc biệt vẫn render OK sau fix. (Không bắt buộc — bug này không phải về i18n.)
- **[NIT] Không có TC sort folder (Checklist §C.8)**: Template feature có sort trong list checklist §C.8. Bug này không chạm sort, có thể skip — nhưng nếu Leader muốn smoke test thêm thì có thể thêm 1 TC sort.

---

## 5. TCs đề xuất bổ sung

> Member copy vào `04-tc-list.md` ở round tiếp theo. **TC-NEW-01 → 03** là BLOCKER (bắt buộc), TC-NEW-04 → 07 là MAJOR.

| TC ID gợi ý | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| **TC-NEW-01** | Reproduce KH flow — Edit template_child qua URL chứa `/?utm_source=...` → Save → back ra list folder không lỗi | - Đã login bot test trên Staging.<br>- Đã có sẵn 1 template_group (id X) chứa ≥1 template con (id Y). | 1. Mở URL: `/basic/template-v2/add-template?template_group_id=X&template_child_id=Y/?utm_source=line&utm_medium=social&utm_id=syanai20260515`<br>2. Quan sát màn Edit template con load đúng template Y (không phải template khác).<br>3. Sửa nội dung text bất kỳ (vd thêm 1 ký tự).<br>4. Click **Save**.<br>5. Back ra màn list template — click vào folder chứa group X.<br>6. (Bonus) Mở DB / API debug check `content` của template_group X. | - Bước 2: load đúng template Y (không hiển thị error).<br>- Bước 4: Save thành công, không alert lỗi.<br>- Bước 5: List template render bình thường, **không có error**.<br>- Bước 6: `content` của template_group X = chuỗi int CSV, **không chứa** `/?utm_source` hay bất kỳ ký tự non-numeric nào. | **High** | **Positive** (verify fix) | **BUG** (root cause) + F1 |
| **TC-NEW-02** | Boundary — input `template_child_id` dạng chuỗi chứa `/`, `?`, `=` được ép về int đúng | - Đã có template_group X với template con Y (id=12345).<br>- Có tool gửi raw request (Postman / curl). | 1. Gửi POST/PUT tới endpoint save template con với body: `template_child_id=12345/?utm_source=line&utm_medium=social`.<br>2. Bắt response.<br>3. Query DB hoặc gọi GET API để check `template_group.content`.<br>4. Lặp lại với các input: `12345abc`, `abc12345`, `12345.5`, `-12345`, `12345 ` (trailing space), empty string. | - Bước 2: response 200 OK (server xử lý được, không 500).<br>- Bước 3: `content` chứa **chỉ `12345`** (đã strip phần `/?utm_*`), không chứa chuỗi gốc.<br>- Bước 4: với invalid input (`abc12345`, empty) → server reject với 400 hoặc validation error, **không** lưu chuỗi sai vào DB. | **High** | **Boundary** | F1 (createTemplate ép int) |
| **TC-NEW-03** | Click folder template chứa template con — hiển thị list không lỗi (verify trực tiếp KH-visible) | - Đã có folder template `定期配信用` chứa ≥1 template_group, mỗi group ≥1 template con.<br>- Data template không bị corrupt (verify content của các group là int CSV). | 1. Vào màn list template.<br>2. Click vào folder `定期配信用`.<br>3. Quan sát list template_group trong folder.<br>4. Click tiếp vào 1 template_group.<br>5. Quan sát list template con trong group. | - Bước 3: list template_group hiển thị đầy đủ, không error message, không spinner mãi.<br>- Bước 5: list template con hiển thị đầy đủ, click vào template con mở được màn Edit.<br>- Console browser không có error / warning. | **High** | **Positive** | **T-implicit** (Click folder — KH-visible behavior) |
| **TC-NEW-04** | Cross-account / Security — user bot A paste URL edit template của bot B → từ chối | - Đã login bot A.<br>- Biết template_group_id và template_child_id của bot B (do staff bot A từng có quyền).<br>- (Checklist LME §A.2 Security + CL11) | 1. Login bot A.<br>2. Paste URL `/basic/template-v2/add-template?template_group_id={B_group}&template_child_id={B_child}`.<br>3. Quan sát màn load.<br>4. Cố click Save với nội dung mới. | - Bước 3: hệ thống **từ chối access** (redirect / 403 / hiển thị message lỗi), không load template của bot B.<br>- Bước 4: không lưu được — không corrupt data bot B. | **High** | **Negative** (security) | F1 + Checklist LME §A.2 Security + §A.1 CL11 |
| **TC-NEW-05** | Verify data sau recovery production (#118251 — Ngọc Ánh recover) | - Truy cập production (`step.lme.jp`) với account read-only (staff không phá data).<br>- Biết `template_group_id=13305886` của bot KH (`myroom.activecampaign@gmail.com`). | 1. Vào màn list template của bot KH.<br>2. Click vào folder chứa group 13305886.<br>3. Mở DB / API check `template_group.content` của id=13305886.<br>4. Mở từng template con (id 13305887, 13305944) trong group. | - Bước 2: list render bình thường.<br>- Bước 3: `content = "13305887,13305944"` (không có `/?utm_source`).<br>- Bước 4: mở được cả 2 template con, hiển thị Edit screen bình thường. | **High** | **Positive** (recovery verify) | BUG (post-fix verify production) |
| **TC-NEW-06** | Compatibility — verify fix trên Win/Chrome + Mac/Safari (CL §A.2 Compatibility) | - Có máy Win + Mac, browser Chrome + Safari.<br>- Test data như TC-NEW-01. | Lặp lại Steps của TC-NEW-01 trên 4 cặp: Win/Chrome, Win/Safari (nếu có), Mac/Chrome, Mac/Safari. | Mọi cặp: kết quả giống TC-NEW-01, không có quirk browser. | **Medium** | **Regression** | Checklist LME §A.2 Compatibility |
| **TC-NEW-07** | Negative — `template_child_id` invalid (`abc`, empty, SQL injection, XSS payload) | - Account test có quyền template.<br>- Tool gửi raw request (Postman). | 1. Gửi save template con với các value `template_child_id`:<br>  a. `abc` (alphabetic)<br>  b. `''` (empty)<br>  c. `1' OR '1'='1` (SQL injection)<br>  d. `<script>alert(1)</script>` (XSS)<br>  e. `99999999999999999` (overflow int) | - Mọi case: server response 4xx (validation fail), KHÔNG 500.<br>- DB không có row nào với content chứa payload nguyên dạng.<br>- Màn list template không bị crash khi reload. | **High** | **Negative** | F1 + Checklist LME §A.2 Security |
| **TC-NEW-08** | Verify storeTemplate / updateTemplate / cloneTemplate cũng ép int đúng (sau khi Dev confirm scope) | - **Chỉ chạy sau khi Dev confirm các function này cùng nhận `template_*_id` từ request.**<br>- (Liên quan note QA trong `03-dev-impact.md`) | Với mỗi function (store / update / clone), gọi endpoint với input `template_child_id=12345/?utm_source=line` → check `content` DB. | Cả 3 function đều ép int đúng — không function nào lưu chuỗi gốc. | **Medium** | **Boundary** | F1 (nếu scope mở rộng) |

---

## 6. Spec update needed (nếu có)

- [x] **Không cần update spec ở phần schema** — spec API EP-30 (`template_*_id: integer`) đã đúng. Bug là code không enforce.
- [ ] **Nên bổ sung spec (optional, không block bug fix)** — chi tiết:
  - **Section**: [api-spec EP-30](../../spec-features/admin/message-template/web/api-spec.md) — thêm rule validation + error case.
  - **Nội dung cần bổ sung**:
    1. **Validation rule**: Server **must** validate `template_*_id` là integer thuần trước khi save. Nếu fail → trả `success: false` với message chuyên dụng (vd `"Invalid template ID"`). Hiện EP-30 list 4 case lỗi (Data empty / Gần broadcast / Save error / Image map area) nhưng **không có** case ID invalid.
    2. **Behavior khi parse `content` fail** (UI list template): graceful degradation thay vì crash màn list. Hiện spec không định nghĩa rõ.
    3. **Manual user** (https://lme.jp/manual/): tùy chọn thêm note "Không paste URL từ LP có UTM tracking khi edit template — hãy paste URL gốc, hoặc tool sẽ tự strip query string." Đây là điểm UX — nếu Dev đã làm auto-strip thì manual không cần note.
  - **Người chịu trách nhiệm update**: Dev (Kieu Son Tung) — owner code + spec implementation; PM tùy quyết định ưu tiên.

---

## 7. Checklist đã chạy

- [x] A. Coverage — phát hiện 3 GAP BLOCKER (BUG, F1 boundary, T-implicit)
- [x] B. Chất lượng từng TC — Title flatten hơi dài (MINOR), Steps dùng `N` (MINOR), atomic OK
- [x] C. Chất lượng bộ TC tổng thể — 56 TCs đều Regression, thiếu chiều Positive/Negative/Boundary (MINOR)
- [x] D. Spec alignment — `02-spec-reference.md` chưa fill (MAJOR), spec cần update (mục 6)
- [x] E. Hành chính — Tester đã ký (Ngần, 2026-05-14, v1), TC ID flat namespace (MINOR)
- [x] F. Base checklist LME
  - [x] F.1 Checklist web — CL5 (double-click) ✓, CL22 (preview before/after save) RISK, CL11 (CRUD đúng account) chưa cover, §A.2 Security chưa cover, §A.2 Compatibility chưa cover
  - [x] F.2 Checklist job — không liên quan (không chạm job)
  - [x] F.3 Các tính năng chung — §C.2 Send message basic OK, §C.8 Sort không liên quan (out-of-scope bug này)

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | _Pending — Leader verify draft_ | |
| Tester | Ngô Thúy Ngần (cần đọc & confirm fix) | |

---

## Phụ lục — Note về quy trình

- **MCP Redmine đã reconnect** lúc fetch issue (sau lần disconnect đầu).
- **MCP google-sheets vẫn off** — TC list được fetch qua MCP Google Drive (xlsx export, parse openpyxl) thay vì sheet API. Khi MCP google-sheets reconnect, có thể chạy `/sync-tc` để push 56 TC này + (sau khi member bổ sung) TC-NEW-01 → 08 lên master sheet.
- **TCs trong file 04 đã được flatten từ hierarchy 7 cột** (Main Function + Sub1..Sub6) của sheet master. Để trace ngược về sheet, mỗi TC có ghi `(sheet R<num>)` cuối Title.
