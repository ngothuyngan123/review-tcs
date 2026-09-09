<!-- sync-target: https://docs.google.com/spreadsheets/d/1ADqqyfszLKBkXNetsoTbsPgthCCDL_Cj710cUrbONU8/edit?gid=898638988#gid=898638988 -->
# 04 (DRAFT delta) — TC bổ sung cho #35968

> ⚠️ **File này là DELTA** — chỉ chứa TC **bổ sung** chưa được cover ở 161 TC cũ (`04-tc-list.md`, tab `#35968`, read-only).
> - TC cũ (TC001–TC161) **giữ nguyên 100%**, KHÔNG sửa/override.
> - TC delta đánh số tiếp **TC162+** để khi `/sync-tc` append xuống dưới TC161 trong cùng tab `#35968` không trùng ID.
> - Member đọc lại từng TC, chỉnh data thật, rồi submit cho Leader.
>
> **Vì sao cần delta:** 161 TC cũ kiểm rất kỹ hành vi sort theo vị trí + trạng thái disable nút trên 6 màn, nhưng **thiếu** các case gắn trực tiếp cơ chế fix (`:key="item.id"` chống node-reuse, rebuild mảng Vue sau kéo-thả, lọc id rỗng) và một số mục checklist LME (CL1/CL2/CL4/CL5/CL10). Delta lấp các gap đó.

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | `<member điền>` |
| Ngày submit | `<member điền>` |
| Version TCs | `v1-delta` |
| Link TC gốc (nếu có) | https://docs.google.com/spreadsheets/d/1ADqqyfszLKBkXNetsoTbsPgthCCDL_Cj710cUrbONU8/edit?gid=898638988#gid=898638988 (tab `#35968`) |

> **Quy ước môi trường:** test trên **Staging** (`staging.lme.jp`). Fix `ai_fixbug_35968` **chưa được Dev test runtime** (chỉ `node -c` + `php -l`) → cần test thủ công kỹ.
> **6 màn trong scope (T1–T6):** QR code, Form answer, Message template, URL, Cross analysis, Scenario.
> Trong đó **5 màn kéo-thả** (jQuery UI sortable): QR / Form / Message template / Cross / Scenario. **URL** là button-based (chỉ nút lên/xuống, KHÔNG kéo-thả) — chỉ thêm `:key` (F14). **Cross — sort item** dùng ajax+nút (không sửa); Cross chỉ fix **sort folder**.

---

## TC List (delta)

| TC ID | Title | Type | Priority | Precondition | Steps | Expected result | Output note | Assignee | Status |
|---|---|---|---|---|---|---|---|---|---|
| TC162 | [BUG repro 1+2] Item ở vị trí số 2 → click nút sort → phản hồi đúng, không nhảy sai vị trí (6 màn) | Positive | High | Trên mỗi màn (QR/Form/Template/URL/Cross-folder/Scenario): có ≥ 4 item/folder hiển thị (vd Template tên A,B,C,D). Account staff đủ quyền, Staging. | 1. Mở list, xác định item đang ở **vị trí số 2**.<br>2. Hover icon 3 chấm của item vị trí 2 → click nút **sort xuống** một lần.<br>3. Quan sát phản hồi.<br>4. Lặp lại với click nút **sort lên** ở item vị trí 2.<br>5. Thực hiện lần lượt cho cả 6 màn (URL dùng nút lên/xuống, không kéo-thả). | - Click có **phản hồi ngay** (KHÔNG đứng im — bug1 đã fix).<br>- Item di chuyển **đúng 1 bước** theo hướng bấm (xuống → vị trí 3; lên → vị trí 1), KHÔNG tự nhảy lên đầu hay sai vị trí (bug2 đã fix).<br>- Các item khác giữ thứ tự tương đối đúng. | | | |
| TC163 | [BUG repro 3] Item ở vị trí số 2 → nút sort LÊN phải enable (6 màn) | Positive | High | Như TC162, list có ≥ 3 item, item đang xét ở **vị trí số 2** (giữa list). | 1. Mở list.<br>2. Hover item ở **vị trí số 2** → quan sát 2 nút sort lên / sort xuống.<br>3. Lặp cho 6 màn (item + folder).<br>4. Bổ sung: kéo-thả 1 item từ cuối lên vị trí 2 rồi hover lại item đó (kiểm tra sau khi DOM đổi thứ tự). | - Item ở giữa list (vị trí 2): **CẢ nút sort lên VÀ sort xuống đều enable** (bug3 đã fix — không còn disable nhầm nút lên).<br>- Sau kéo-thả, trạng thái nút vẫn đúng theo vị trí hiển thị thực tế (không bị gán nhầm sang item khác do node-reuse). | | | |
| TC164 | [BUG repro 4] Item dưới cùng → nút sort XUỐNG phải ẩn/disable (6 màn) | Positive | High | Như TC162, item đang xét ở **vị trí cuối cùng** của list. | 1. Mở list.<br>2. Hover item **cuối cùng** → quan sát nút sort xuống.<br>3. Lặp cho 6 màn (item + folder).<br>4. Bổ sung: kéo-thả 1 item xuống cuối rồi hover lại (kiểm tra sau khi DOM đổi thứ tự). | - Item cuối: nút sort xuống **KHÔNG hiển thị / bị disable** (bug4 đã fix), chỉ còn nút sort lên enable.<br>- Item đầu: ngược lại — nút sort lên disable, nút sort xuống enable.<br>- Đúng cả sau khi kéo-thả (không gán nhầm trạng thái). | | | |
| TC165 | [:key item.id] Sort 2 item TRÙNG TÊN nhưng khác id → đúng item di chuyển (5 màn kéo-thả + URL) | Boundary | High | Trên mỗi màn tạo ≥ 2 item **cùng tên hiển thị** (vd 2 Template đều tên `キャンペーン`) ở vị trí cạnh nhau, phân biệt bằng nội dung/ngày tạo. | 1. Mở list/modal sort.<br>2. Kéo-thả (hoặc dùng nút) để đổi vị trí **một trong hai** item trùng tên.<br>3. Mở/hover từng item kiểm tra nội dung chi tiết để xác định đúng item nào đã di chuyển.<br>4. Save → reload → kiểm lại.<br>5. Lặp cho QR/Form/Template/Cross/Scenario + URL. | - **Đúng item được chọn** (đúng id) di chuyển, item trùng tên còn lại **không bị đổi nhầm** (xác nhận `:key="item.id"` track đúng, không còn node-reuse theo index).<br>- Sau save+reload, thứ tự đúng, không có item nào bị mất hay nhân đôi. | | | |
| TC166 | [Rebuild mảng] Sau kéo-thả: số lượng item KHÔNG đổi, không rớt/trùng item (5 màn kéo-thả) | Boundary | High | Mỗi màn có **đúng N item** (vd N=6) đã ghi nhớ trước. Account staff, Staging. | 1. Đếm/ghi nhớ N item và tên từng item.<br>2. Thực hiện chuỗi kéo-thả nhiều lần (đảo đầu↔cuối, chèn giữa).<br>3. Đếm lại số item + đối chiếu tên.<br>4. Save → reload → đếm lại.<br>5. Lặp cho QR/Form/Template/Cross/Scenario. | - Sau mọi thao tác và sau save/reload: **vẫn đúng N item**, đầy đủ tên cũ, KHÔNG rớt item (xác nhận map id→item dựng lại đúng + lọc id rỗng không xoá nhầm), KHÔNG có dòng trống/trùng. | | | |
| TC167 | [Desync] Kéo-thả rồi bấm nút lên/xuống xen kẽ NHIỀU lần (chưa save) → index luôn khớp hiển thị | Boundary | High | Màn kéo-thả, list ≥ 5 item. | 1. Kéo item E từ cuối lên vị trí 2.<br>2. KHÔNG save. Bấm nút sort xuống cho item vị trí 2.<br>3. Kéo tiếp item khác.<br>4. Bấm nút sort lên/xuống vài item.<br>5. Sau mỗi thao tác, kiểm nút bấm có tác động đúng item đang hover.<br>6. Lặp cho QR/Form/Template/Cross/Scenario. | - Sau mỗi lần kéo-thả, nút sort lên/xuống luôn **tác động đúng item hiển thị** (mảng Vue rebuild ngay sau kéo-thả nên index không lệch — bug1/2 không tái phát dù thao tác liên tục, chưa save). | | | |
| TC168 | [Modal sort] Kéo-thả trong modal → đóng/hủy không save → mở lại → thứ tự về default (position) | Regression | Medium | Màn có modal sort riêng (Template/QR/Form/Cross/Scenario 並べ替え). | 1. Mở modal sort, kéo-thả đổi thứ tự vài item.<br>2. Đóng modal (X / hủy) **không bấm save**.<br>3. Mở lại modal sort.<br>4. Quan sát thứ tự. | - Thứ tự trong modal mở lại = **thứ tự default theo position đã lưu** (clear data về default, không giữ thay đổi chưa save) — đồng nhất hành vi mô tả ở TC cũ TC019/048/077/151 (sort theo cột rồi mở modal → clear về position). | | | |
| TC169 | [Template in-folder] Sort template BÊN TRONG folder đang mở (group_open) → đúng thứ tự, không lẫn nhóm | Positive | High | Màn Message template: có ≥ 1 folder chứa ≥ 3 template, và có template ở ngoài folder. Mở (expand) folder đó. | 1. Mở folder (group_open).<br>2. Kéo-thả / bấm nút sort các template **trong folder**.<br>3. Kiểm thứ tự template trong folder + trạng thái nút lên/xuống.<br>4. Save → reload → mở lại folder kiểm thứ tự.<br>5. Đối chiếu: template ngoài folder không bị ảnh hưởng. | - Sort template trong folder hoạt động đúng (rebuild `items_sort` theo `group_open`), thứ tự lưu đúng sau reload.<br>- Template **ngoài folder** (`items_default_sort`) giữ nguyên, không bị trộn thứ tự.<br>- Nút lên/xuống đúng trạng thái theo vị trí trong folder. | | | |
| TC170 | [CL2 + API unchanged] Save thứ tự sort → reload trang → thứ tự được giữ đúng, không lỗi (6 màn) | Regression | High | Mỗi màn có list đã sort theo thứ tự tùy chỉnh. | 1. Thực hiện sort + save trên mỗi màn (item và folder).<br>2. **Reload (F5)** trang.<br>3. Kiểm thứ tự hiển thị.<br>4. (Tùy chọn) đăng nhập account khác cùng bot → xem thứ tự.<br>5. Lặp cho 6 màn. | - Sau reload: thứ tự **đúng như đã save** (xác nhận logic submit ô ẩn → API lưu position KHÔNG đổi — mục 3 dev impact).<br>- Màn list không lỗi JS/console sau reload (CL2). | | | |
| TC171 | [CL5] Double-click nhanh nút sort lên/xuống ở biên → không lỗi, không nhảy quá vị trí | Negative | Medium | Màn kéo-thả + URL, list ≥ 4 item. | 1. Hover item ở vị trí 2 → **double-click** nhanh nút sort lên.<br>2. Quan sát.<br>3. Double-click nút sort xuống ở item áp cuối.<br>4. Double-click nút sort lên ở item ĐẦU (nút đang disable).<br>5. Lặp vài màn. | - Double-click không gây item **nhảy 2 bước ngoài ý muốn** hoặc lỗi JS/đứng UI; item dừng ở vị trí hợp lệ.<br>- Bấm nút đang disable (item đầu/ cuối) không có tác động, không lỗi. | | | |
| TC172 | [CL4] Thao tác liên tục: Tạo mới → Sort → Edit → Sort → Xóa → Sort (item + folder) | Boundary | Medium | Màn item (QR/Form/Template/Scenario/Cross-folder) + URL. | 1. Tạo mới 1 item → kiểm vị trí (đầu list).<br>2. Sort item vừa tạo xuống giữa.<br>3. Edit tên item khác → Sort lại.<br>4. Xóa 1 item → Sort các item còn lại.<br>5. Sau mỗi bước kiểm thứ tự + trạng thái nút.<br>6. Lặp cho item và folder. | - Sau mỗi thao tác xen kẽ: thứ tự + trạng thái nút lên/xuống luôn đúng theo list hiện tại, không lệch index, không rớt item (CL4). | | | |
| TC173 | [CL1] Account staff sort: không quyền → không access/không thao tác; có quyền → giống account chính | Negative | Medium | 2 staff: 1 **không** được cấp quyền màn tương ứng, 1 **được** cấp quyền. | 1. Login staff **không quyền** → mở màn QR/Form/Template/URL/Cross/Scenario.<br>2. Thử truy cập chức năng sort.<br>3. Login staff **có quyền** → thực hiện sort + save.<br>4. Đối chiếu kết quả với account chính. | - Staff không quyền: **không access được** màn / không thấy chức năng sort (theo phân quyền).<br>- Staff có quyền: sort + save hoạt động **giống hệt account chính**, thứ tự lưu đúng (CL1). | | | |
| TC174 | [CL10] Xóa 1 item giữa list đang sort → vị trí + trạng thái nút các item còn lại vẫn đúng | Boundary | Medium | Màn item/folder, list ≥ 4 item đã sort tùy chỉnh. | 1. Xóa 1 item ở **giữa** list.<br>2. Quan sát các item còn lại: vị trí, nút sort lên/xuống (đặc biệt item mới thành cuối / đầu).<br>3. Sort tiếp 1 item → kiểm.<br>4. Save → reload kiểm thứ tự.<br>5. Lặp vài màn. | - Sau xóa: list re-index đúng, item mới ở vị trí cuối có nút xuống disable, item đầu có nút lên disable (bug3/4 không tái phát sau xóa).<br>- Sort tiếp vẫn đúng; reload giữ thứ tự. | | | |
| TC175 | [Regression :key main list] Thêm :key vào list màn chính → render đúng, folder expand/collapse + CRUD không lỗi | Regression | High | Màn Form / Template / Scenario / URL (các blade list màn chính được thêm :key: F7/F9/F13/F14). | 1. Mở màn list chính (ngoài modal sort).<br>2. Expand/collapse các folder nhiều lần.<br>3. Tạo mới / sửa / xóa item + folder.<br>4. Kiểm item hiển thị đúng folder, không trùng/mất, không lỗi render.<br>5. Chuyển trang phân trang (CL15) → kiểm. | - List màn chính render đúng sau khi thêm `:key` (không mất item, không nhân đôi, expand/collapse mượt).<br>- CRUD item/folder hiển thị cập nhật đúng vị trí, không lỗi JS — xác nhận việc thêm `:key` ở list màn chính không gây regression hiển thị. | | | |

### Chú thích cột

- **Type**: Positive / Negative / Boundary / Regression.
- **Priority**: High = block release nếu fail / Medium = có workaround / Low.
- **Output note / Assignee / Status**: để trống — QA fill sau khi run.

### Environment (note)

Mặc định **Staging** (`staging.lme.jp`). Một số TC nên test thêm trên **Dev** (`form.watermeru.com`) để reproduce timing/race của kéo-thả nếu Staging khó tái hiện. Fix chưa qua test runtime của Dev → ưu tiên test kỹ TC162–TC167.

---

## Member tự check trước khi submit

### Coverage check
- [x] Đã đọc kỹ `01-bug-task.md` (4 bug từ màn Tag, 横展開 sang 6 màn)
- [ ] Đã đọc kỹ `02-spec-reference.md` (chưa có file 02 — tham chiếu `templates/LME-SYSTEM-SPEC.md` nếu cần)
- [x] Đã đọc kỹ `03-dev-impact.md`, hiểu 4 mục
- [x] **Mỗi impact** F/D/T có ≥ 1 TC verify (xem mapping nội bộ ở summary; D = không có data nên không cần TC data)
- [x] Có ≥ 1 TC verify trực tiếp bug fix (TC162–TC164 reproduce 4 bug)
- [x] Có ≥ 1 TC regression cho mỗi tính năng T1–T6 (TC170/TC175 chạy đủ 6 màn + 161 TC cũ)
- [ ] Có ≥ 1 negative + 1 boundary cho mỗi data quan trọng trong 4.2 → **N/A** (4.2 không có data — chỉ sửa FE)
- [x] Mọi TC có steps rõ ràng, expected đo lường được
- [x] Title TC chứa keyword (bug số, :key, màn, CL) giúp Leader map impact

### Base checklist LME (mục đã cover bởi delta — xem [framework/checklist-lme.md](../../framework/checklist-lme.md))

**§A.1 Function checklist**:
- [x] CL1 — account staff (TC173)
- [x] CL2 — reload sau save/sort không lỗi (TC170)
- [x] CL4 — thao tác liên tục (TC172)
- [x] CL5 — double click (TC171)
- [x] CL10 — xóa item ảnh hưởng list đang sort (TC174)
- [x] CL15 — phân trang (TC175 + TC cũ TC017/046/075/123/149)
- [ ] CL9 — search (đã cover ở TC cũ TC018/047/076/124/150)

**§A.2 Non-function**:
- [x] Regression (TC168/TC170/TC174/TC175 + 161 TC cũ)
- [ ] Security — **N/A** (không có URL/màn mới)
- [ ] Compatibility — nên check Win+Mac/Chrome+Safari cho kéo-thả (UI thay đổi nhẹ)

**§C Tính năng chung**:
- [x] C.8 Sort ← **trọng tâm task** (6 màn)

<!-- Source: delta sinh bởi /write-tc ngày 2026-06-09, dựa trên 01-bug-task.md + 03-dev-impact.md (đã verify). TC cũ TC001-161 (tab #35968) là read-only reference — KHÔNG sửa. Delta đánh số TC162+ để /sync-tc append dưới TC161 trong cùng tab #35968 (gid 898638988). -->
