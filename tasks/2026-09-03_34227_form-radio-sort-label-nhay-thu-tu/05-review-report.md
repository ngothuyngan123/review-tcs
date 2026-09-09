# 05 — Review Report

Bug #34227 — `[Form] Item radio, khi edit xong sort label => nhấn save các lable bị nhảy thứ tự`

---

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | **(1) MCP LME TEST STUDIO — task #204** |
| Vì sao không dùng nguồn ưu tiên cao hơn | N.A. — đã dùng nguồn ưu tiên cao nhất |
| Ticket · task_id · round · branch | `34227` · `#204` · round `1` · `ai_fixbug_34227` |
| Thời điểm fetch | `2026-09-03` |
| Tổng số TC review | `16` |
| Snapshot đã ghi | `04-tc-list.md` — đã là snapshot của **chính lần fetch này** (header `<!-- source: MCP LME TEST STUDIO — task_id=204 ... -->`), không cần refresh |
| Đối chiếu chéo nguồn | **KHÔNG** — đã dừng ở nguồn 1 |
| Tester được review | AI pipeline (Studio job `#614`) — 14 TC · `trangnq@mcp` — 2 TC |
| Vòng review | Round 1 |
| **Nguồn spec đã dùng** | [spec-features/admin/form-answer/feature-spec.md](../../spec-features/admin/form-answer/feature-spec.md) §5 Business Rules — **BR-09** (using_old_version), **BR-10** (form phân nhánh `next_page_setting`), **BR-11** (validation rules), **BR-12** (liên kết friend info) · §2 SCR-FA11-03/08 · §3 Data Model. Tra `FA-011` qua [templates/LME-SYSTEM-SPEC.md](../../templates/LME-SYSTEM-SPEC.md) dòng 687/798. |
| Studio task metadata | `status = done-ai` · `aiResult = pass` · `reviewState = leader` · `reviewed = false` · `openBugs = 0` · `submittedWithoutMcp = false` |

### 0.6 — Cảnh báo chất lượng nguồn (Studio)

| # | Chiều | Kết quả | Flag |
|---|---|---|---|
| 1 | Kết quả thực thi thật (`pass` mới là Đạt) | **14/16 pass (87,5%)** · 2 `skip` · 0 `fail` · 0 `error` · 0 chưa chạy | `OK` (≥80%) — nhưng 2 `skip` là **không có kết luận test**, xem §4 |
| 2 | TC `fail`/`error` + TC gắn ticket bug | **Không có TC fail/error.** Không TC nào gắn `bug_tickets` | `OK` |
| 3 | Môi trường đã chạy — RULE-08 / ENV-003 | `PROD 0` · `STAGING 16` · `LOCAL 0` (task-level `envAuto`: 2 run local + 2 run staging, **0 run prd**) | `OK` — task **không** chạm media / domain / job nền / loadbalance / bill tiền nên RULE-08 không bắt buộc production. ⚠️ Rủi ro riêng về **asset JS cache** xem `[MAJOR-04]` |
| 4 | Ai chạy (`last_exec.source` / `by`) | **16/16 `manual` bởi `trangnq`** (QA người), ngày 2026-09-03. Không có kết quả nào do AI pipeline tự chấm | `OK` — điểm tốt |
| 5 | Tác giả TC (`provenance.source`) | **14/16 do AI sinh** (87,5%, job `#614`) · 2/16 người viết (`trangnq@mcp`) · `reviewState = leader`, `reviewed = false` | `[MAJOR]` — ≥50% TC do AI sinh mà review chưa `done` |
| 6 | Mã quan điểm KHÔNG có trong `checklist-lme.md` | **4 mã / 4 lượt TC**: `TOOL-KNOW-002`, `TOOL-ERRHYG-001`, `TOOL-NEGCTRL-001`, `TOOL-OLDREC-001` | **Không tính là cover** ở §3 và §3.6 |

> ⚠️ **Hệ quả của mục 6 — đọc kỹ**: 4 TC bị loại khỏi coverage gồm cả `TC-TOOLKNOW002-01` (TC tái hiện bug ở chế độ *không liên kết*) và `TC-TOOLOLDREC001-01` (TC duy nhất cho impact `D2`). Đây **không** phải "TC sai", mà là TC mang mã nội bộ Studio. Cách xử lý đúng: **đổi mã quan điểm trên Studio sang mã tầng 1 tương ứng** (`TOOL-KNOW-002` → `FUNC-SEQ-001`; `TOOL-OLDREC-001` → `COMPAT-LEGACY-001`; `TOOL-ERRHYG-001` → `UI-003`; `TOOL-NEGCTRL-001` → `DATA-DB-001`) — xem `[MAJOR-01]`.

---

## 1. Verdict

# ⛔ REJECTED

**3 `[BLOCKER]`** — bộ TC bỏ trống hoàn toàn 3 vùng rủi ro cao mà chính `03-dev-impact.md` và spec FA-011 đã chỉ ra: nhóm câu hỏi dùng chung cơ chế kéo-thả (`T2`), form phân nhánh (BR-10), và dọn dẹp giá trị friend info khi options đổi (BR-12).

---

## 2. Tóm tắt cho member

**Điểm tốt**: bộ TC bám sát 5 callback Dev đã sửa, có TC đối chứng âm (item A không ảnh hưởng item B), có TC boundary kéo nhiều lần liên tiếp, và **toàn bộ 16 TC đã được QA người chạy tay trên staging** — không có kết quả nào do AI tự chấm.

**Phải fix**: bộ TC chỉ test **đúng phạm vi Dev khai trong mục 4.1 (file JS)** mà bỏ qua **mục 4.3 T2** — Dev nói rõ *"câu hỏi giới tính, chẩn đoán, nhắc lịch dùng chung cơ chế kéo-thả lựa chọn nên cũng được sửa theo"* nhưng **0 TC** chạm 3 loại câu hỏi này; riêng câu hỏi **nhắc lịch (remind)** nếu sort sai thì lịch nhắc đã đặt của friend gắn nhầm option. Ngoài ra spec FA-011 chỉ ra 2 hệ quả dây chuyền của việc "đổi thứ tự + sửa nội dung option" mà không TC nào kiểm: **form phân nhánh** map trang tiếp theo **bằng chuỗi label** (BR-10), và **liên kết friend info** sẽ **xóa `FriendInformationValue` không còn dùng** khi options thay đổi (BR-12). Cuối cùng: 5 TC của `REG-SHARED-001` (ưu tiên **Cao**) **đều là `Normal`** → vi phạm RULE-01.

---

## 3. Coverage Matrix

> `Exec` = `<số pass>/<số TC hợp lệ>`. TC mang mã quan điểm không có trong `checklist-lme.md` (§0.6 #6) **không được tính là cover** — ghi trong ngoặc để tham chiếu.

| Impact | Loại | TC cover (suy luận) | # TC | Exec | Status |
|---|---|---|---|---|---|
| **BUG** — thứ tự kéo-thả không ghi vào data ngay lúc thả, treo tới lúc Save | Fix | `TC-FUNCSEQ001-01` *(+ `TC-TOOLKNOW002-01` — mã không hợp lệ)* | 1 | 1/1 | `OK` |
| **F1** — `sortOptionItemForm` (thêm null-guard) | Function | *(chỉ `TC-TOOLERRHYG001-01` — mã không hợp lệ **và** đã `skip`)* | 0 | 0/0 | **`GAP`** |
| **F2** — `showItemComponent`, callback thả chuột (chọn lại câu hỏi) | Function | `TC-REGSHARED001-01`, `TC-FUNCSEQ001-04` | 2 | 2/2 | `OK` |
| **F3** — `initSortNotLink` (chế độ không liên kết) | Function | *(chỉ `TC-TOOLKNOW002-01` — mã không hợp lệ)*; các TC `FUNC-SEQ-001` khác **không ghi rõ chế độ** | 0 | — | **`GAP`** |
| **F4** — `initSortFriendInfo` (liên kết thông tin bạn bè) | Function | `TC-REGSHARED001-02` | 1 | 1/1 | `RISK` — chỉ `Normal`; không kiểm giá trị friend info đã tồn tại (BR-12) |
| **F5** — `changeTagAndFriend` (tag lựa chọn đơn) | Function | `TC-REGSHARED001-03` | 1 | 1/1 | `RISK` — chỉ `Normal` |
| **F6** — `changeTagCheckbox` (tag lựa chọn nhiều) | Function | `TC-REGSHARED001-04` | 1 | 1/1 | `RISK` — chỉ `Normal`; chế độ hiển thị **dropdown** không có TC (chính note của TC tự nêu nghi vấn) |
| **F7** — `saveFormAnswer` (lời gọi cũ thành bước dự phòng) | Function | Ngầm bởi mọi TC có bước Lưu: `TC-FUNCSEQ001-01..05`, `TC-REGSHARED001-01..05` | 10 | 10/10 | `OK` |
| **F8** — `FormAnswerController::saveV3` / `makeDataEditV3` (Dev xác nhận không sửa) | Function | `TC-FUNCSEQ001-01` (verify persist sau reload) | 1 | 1/1 | `OK` |
| **D1** — không có data bị update (fix thuần giao diện) | Data | — | — | — | `N/A` |
| **D2** — dữ liệu form lưu **sai thứ tự trước fix**, KHÔNG migrate | Data | *(chỉ `TC-TOOLOLDREC001-01` — mã không hợp lệ)* | 0 | — | **`GAP`** |
| **T1** — Form Builder: sắp xếp lựa chọn câu hỏi đơn/nhiều ở **3 chế độ** (không liên kết · tag · friend info) | Feature | không liên kết ✗ · tag `TC-REGSHARED001-01/03` ✓ · friend info `TC-REGSHARED001-02` ✓ | 3 | 3/3 | `RISK` — thiếu chế độ *không liên kết* (mã hợp lệ) + thiếu dropdown |
| **T2** — Form Builder: câu hỏi **giới tính · chẩn đoán · nhắc lịch** (dùng chung cơ chế kéo-thả) | Feature | **không có TC nào** | 0 | — | **`GAP`** ⛔ |

### ORPHAN TCs

| TC ID | Title | Lý do orphan | Hành động đề xuất |
|---|---|---|---|
| `TC-DEPLOYASSET001-01` | Kiểm tra tĩnh: asset `setting_form_items.js` đã chứa fix (5 callback + null-guard) | **Không orphan về scope** nhưng là **kiểm tra source code (white-box)**, không phải TC kiểm hành vi. Nó **không** thỏa Evidence của `DEPLOY-ASSET-001` (yêu cầu *screenshot DevTools Network + màn sau **F5 thường** trên browser còn cache bản cũ*). Hiện lại đang `skip` | Giữ làm bước tiền kiểm; **bổ sung** TC hành vi `TC-DEPLOYASSET001-02` (§5) |

Không có TC nào lạc hoàn toàn ngoài scope `BUG / F* / D* / T*`.

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| Fix shape (đọc mục 2 dev-impact) | **3 shape cùng lúc**: (a) **"sửa hàm dùng chung"** — *"5 chỗ khởi tạo kéo-thả"*, *"theo đúng mẫu đã duyệt ở màn quản lý tag"*, *"Quét ngang"* → `REG-SHARED-001`; (b) **"JS / asset"** — *"CHỈ sửa 1 file JS, KHÔNG bump số phiên bản tài nguyên tĩnh"* → `DEPLOY-ASSET-001`; (c) **"thêm kiểm tra điều kiện"** — *"Thêm kiểm tra tồn tại câu hỏi trước khi sắp xếp"* → `FUNC-002/003/004` |
| Trigger space cần cover | **(a)** 5 callback đã sửa + 3 loại câu hỏi dùng chung ở `T2` (giới tính · chẩn đoán · nhắc lịch) + **màn quản lý tag** (`public/js/tag/index_v2.js` — Dev tự khai cùng lớp lỗi) = **9 nơi**. **(b)** browser còn cache JS cũ, F5 thường (không Ctrl+F5). **(c)** chưa chọn câu hỏi · item chưa có `selectable.items` |
| Số trigger TCs hiện cover | **(a) 4/9** — cover: `showItemComponent`, `initSortFriendInfo`, `changeTagAndFriend`, `changeTagCheckbox`. **Không cover**: `initSortNotLink` (chỉ TC mã lạ), 3 loại câu hỏi `T2`, màn quản lý tag. **(b) 0/1** — TC duy nhất là kiểm tra tĩnh source **và đã `skip`**. **(c) 0/2** — TC null-guard đã `skip` |
| KH report dạng | **Symptom-only (một phần)** — file 01 có 4 bước tái hiện rõ nhưng `Actual result` chỉ ghi hiện tượng *"thứ tự lable bị nhảy"*, **không có** error message / console log / root cause. `Expected result` **trống** (Redmine không phát biểu) |
| Alternative root causes cần verify | 1. **Label trùng nội dung** → cơ chế "mã tạm bị đánh số lại" (mục 1 dev-impact) dễ gán nhầm khi 2 label giống hệt → `DATA-ID-001`. 2. **Server rebuild lại thứ tự** khi lưu — Dev **loại bằng đọc code** `saveV3`/`makeDataEditV3` nhưng **chưa chạy thực tế** (mục 6 VERIFY: *"MySQL... Connection refused, stack dev không chạy"*), và BR-10/BR-12 cho thấy server **có** rebuild `next_page_setting` + dọn `friend_info_option_selects` khi lưu. 3. **Browser cache JS cũ** (Dev không bump version) |
| Anti-patterns dính | **`AP-2`** (symptom-only) · **`AP-3`** (happy-path-only regression) |

**`AP-3` chi tiết**: mục 4.3 list `T1` + `T2`. `T2` = 0 TC. `T1` có TC nhưng **tiền đề của cả 10 TC đều là "Form Builder V3 tạo form MỚI"** — data sạch, không edge state. Không TC nào chạy trên: form **đã có câu trả lời** của friend, form **phân nhánh**, form **UI cũ** (`using_old_version=1`), form ở **giới hạn số option**.

---

## 3.6 Bảng quan điểm đối chiếu

> Trigger đối chiếu [framework/checklist-lme.index.md](../../framework/checklist-lme.index.md). Cột `Ưu tiên` in đậm khi khớp **điều kiện nâng lên Cao**.

### Quan điểm ◯ (Trigger khớp task)

| Mã quan điểm | Ưu tiên | Trigger khớp task? | TC cover (suy luận) | Exec | Kết luận |
|---|---|---|---|---|---|
| `FUNC-SEQ-001` ★ | Trung bình (Trigger **BẮT BUỘC** — màn có Sort) | ◯ — đúng tâm bug: Sort + Edit + Save trên cùng danh sách | `TC-FUNCSEQ001-01..05` (N/A/A/A/B) | 5/5 | `OK` — đủ 3 loại case. ⚠️ thiếu chuỗi `Sort→Sort` + `F5 sau mỗi chuỗi` theo mô tả `Kiểm tra` |
| `REG-SHARED-001` | **Cao** | ◯ — "5 chỗ dùng chung", "mẫu đã duyệt ở màn quản lý tag" | `TC-REGSHARED001-01..05` — **cả 5 đều `Normal`** | 5/5 | **`RISK`** — vi phạm **RULE-01** (thiếu `Abnormal` + `Boundary`, không ghi lý do) **và** thiếu 5/9 nơi ảnh hưởng |
| `OUT-TRUTH-001` | **Cao** | ◯ — thao tác Lưu có thông báo kết quả | `TC-OUTTRUTH001-01` (`Normal`) | 1/1 | **`RISK`** — RULE-01: thiếu `Abnormal` + `Boundary`; không có case "Lưu thất bại → thông báo đúng nguyên nhân" |
| `DEPLOY-ASSET-001` ★ | **Cao** | ◯ — release sửa file JS, **không bump version** | `TC-DEPLOYASSET001-01` — kiểm tra tĩnh, **`skip`** | 0/1 | **`GAP`** — không có TC F5-thường trên browser còn cache |
| `COMPAT-LEGACY-001` ★ | **Cao** | ◯ — chạm **form**; Form Builder **V3** (BR-09 `using_old_version`); tồn tại data lưu trước fix | *(chỉ `TC-TOOLOLDREC001-01` — mã không hợp lệ)* | — | **`GAP`** — RULE-09: chưa test nhánh cũ ⇄ mới |
| `FRIEND-001` | **Cao** | ◯ — BR-12: option liên kết friend info, ghi/xóa `FriendInformationValue` | `TC-REGSHARED001-02` chỉ kiểm *mapping*, không kiểm *value* của friend đã có | 0 | **`GAP`** ⛔ |
| `DATA-001` | **Cao** | ◯ — thứ tự option được tham chiếu ở: form public, `next_page_setting` (BR-10), `friend_info_option_selects` (BR-12), Google Spreadsheet (BR-08/BR-14) | `TC-OUTTRUTH001-01` (chỉ form public) | 1/1 | **`RISK`** — mới 1/4 nơi tham chiếu |
| `DATA-DB-001` ★ | **Cao** | ◯ — Save form = UPDATE | Expected của `TC-TOOLKNOW002-01` có nhắc `selectable.items`, nhưng TC mã không hợp lệ; TC hợp lệ chỉ verify qua UI sau reload | 0 | **`RISK`** — RULE-07: chưa verify tầng DB; chưa có case 2 bot/2 tài khoản kiểm `WHERE` scope |
| `DATA-ID-001` | Trung bình (**→ Cao** — màn chọn đối tượng để thao tác) | ◯ — root cause là "mã tạm bị đánh số lại"; label **có thể trùng nội dung** | không có | — | **`GAP`** |
| `UI-003` | Trung bình (**→ Cao** — rủi ro **false success**) | ◯ — bug này *chính là* false success: báo Lưu thành công nhưng thứ tự sai | *(chỉ `TC-TOOLERRHYG001-01` — mã không hợp lệ, `skip`)* | — | **`GAP`** |
| `FUNC-DRAFT-001` | Trung bình | ◯ — Trigger nêu đích danh **form builder**; kéo-thả chưa Save = nội dung soạn dở | `TC-FUNCSEQ001-04` (chuyển câu hỏi rồi quay lại) | 1/1 | `OK` |
| `UI-FIELD-001` | Trung bình | ◯ — chế độ liên kết (không liên kết / tag / friend info) là field cha, vùng option là field con | `TC-REGSHARED001-03/04/05` | 3/3 | `OK` |
| `FUNC-004` | **Cao** | ◯ — số lượng option có giới hạn; kéo sort ở biên | không có (`TC-FUNCSEQ001-05` là boundary về *số lần kéo*, không phải *số option*) | — | **`GAP`** |
| `LIST-001` | Trung bình | ◯ — `changePage` nằm trong caller đã check (mục 3); form nhiều trang | không có | — | **`GAP`** |
| `PERF-LARGE-001` | Trung bình | ◯ — kéo sort danh sách option lớn | không có | — | `GAP` (gộp vào TC boundary §5) |
| `DATA-CACHE-001` | Trung bình (**→ Cao** — output user-facing) | ◯ — release đổi JS, không bump version | không có | — | `GAP` (gộp với `DEPLOY-ASSET-001`) |
| `DATA-TEXT-001` | Trung bình | ◯ — label là text tự do, hiển thị trên LINE + export | không có | — | `GAP` — mức `[MINOR]`, xem §4.3 |
| `FUNC-001` / `FUNC-002` | **Cao** | ◯ — luồng chính + form nhập liệu | `TC-FUNCSEQ001-01` (luồng chính); validation label rỗng: không có | 1/1 | `RISK` |
| `CONC-003` ★ | Trung bình | ◯ — builder có nhiều request; kéo-thả trong lúc API chưa trả về | không có | — | `GAP` — mức `[MINOR]` (rủi ro thấp với fix này) |
| `LIFF-ENTRY-001` ★ | **Cao** | ◯ (hẹp) — form phát sinh URL cho LINE user | `TC-OUTTRUTH001-01` mở form public bằng browser | 1/1 | `RISK` — RULE-06: chưa mở **trên LINE app thật** |

### Quan điểm × (không áp dụng — RULE-03 ghi lý do)

| Mã | Lý do × |
|---|---|
| `DATA-MIG-001` | Fix **không đổi cấu trúc dữ liệu**; Dev xác nhận 4.2 "không đổi cấu trúc bảng". Phần "data cũ" đã chuyển sang `COMPAT-LEGACY-001` |
| `DATA-BACKUP-001` | Không thêm/đổi bảng DB |
| `ENV-003` | Không chạm media/file · URL/domain · job nền · thanh toán · không thêm server. Rủi ro asset JS đã tách sang `DEPLOY-ASSET-001` |
| `JOB-001`, `REG-RUN-001`, `PAY-*`, `MSG-*`, `BULK-001`, `MEDIA-*`, `SEC-*`, `PERM-*` | Fix thuần client-side trong màn builder, không chạm job nền · gửi tin · thanh toán · media · phân quyền · dữ liệu nhạy cảm |
| `INTG-SHEET-001` | Fix **không chạm** luồng ghi Google Spreadsheet (BR-08/BR-14). Ghi ở `[NIT-02]` để Leader quyết, không đề xuất TC (tránh over-coverage layer downstream) |
| `CONC-001` | Không có nút thực thi hành động quan trọng / batch / giới hạn dùng chung trong phạm vi fix |
| `REG-SPEC-001` | Không có thay đổi spec sau khi đã có TC |
| `DEPLOY-LIVE-001` ★ | ⚠️ **× có điều kiện** — release JS không bật maintain, user đang mở tab builder cũ. Không đề xuất TC riêng vì đã gộp vào `TC-DEPLOYASSET001-02` (§5). Leader thấy cần tách thì tách |

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

**`[BLOCKER-01]` GAP-1 — `T2` (giới tính · chẩn đoán · nhắc lịch) có 0 TC** — FIX-SHAPE: shared code
`03-dev-impact.md` §4.3 T2 ghi rõ: *"câu hỏi giới tính, chẩn đoán, nhắc lịch dùng chung cơ chế kéo-thả lựa chọn nên **cũng được sửa theo**"*. Dev **đã cung cấp** danh sách nơi ảnh hưởng, nhưng bộ TC **không test một nơi nào** trong 3 nơi đó → vi phạm `REG-SHARED-001` (*"test lại từng mục"*).
Nguy hiểm nhất là **câu hỏi nhắc lịch (remind)**: kho TCs `TC-FORM-174` cho thấy option remind gắn với **lịch nhắc đã đặt của friend** (xóa option chọn `配信を停止する` → hủy lịch remind chưa gửi). Nếu thứ tự option remind bị áp sai lúc lưu, lịch nhắc của friend có thể gắn nhầm option → **gửi/hủy nhắc sai người**.
→ **Fix**: bổ sung `TC-REGSHARED001-06` (remind, `Abnormal`) + `TC-REGSHARED001-07` (chẩn đoán + giới tính, `Normal`) — §5.

**`[BLOCKER-02]` GAP-2 — Form phân nhánh (`分岐タイプ`) có 0 TC, trong khi BR-10 map trang tiếp theo BẰNG CHUỖI LABEL**
Spec FA-011 **BR-10**: `next_page_setting` JSON `[{value: "label", pageId: N}]` — *"Khi lưu: **rebuild `next_page_setting` từ danh sách option hiện tại** để đảm bảo nhất quán"*. Nghĩa là điều kiện phân nhánh khoá theo **nội dung label**, và được **dựng lại từ mảng option** — đúng mảng mà fix này thay đổi thứ tự.
Flow của bug (**edit label rồi sort rồi save**) là tổ hợp nguy hiểm nhất với BR-10: label đổi nội dung + đổi vị trí trong cùng một lần lưu. Không TC nào (kể cả TC do người viết) chạy trên form `form_type=2`. Kho TCs đã tách riêng case này cho item (`TC-FORM-100` — *"Move item ở form rẽ nhánh"*) nhưng **chưa có** cho option bên trong item.
→ **Fix**: bổ sung `TC-FUNCSEQ001-06` — §5.

**`[BLOCKER-03]` GAP-3 — BR-12: options thay đổi thì hệ thống XÓA `FriendInformationValue`, không TC nào kiểm dữ liệu friend còn nguyên**
Spec FA-011 **BR-12**: *"Nếu loại select (`type_data=1`): upsert `friend_info_option_selects`, dọn dẹp options cũ. **Nếu options thay đổi → xóa `FriendInformationValue` và `FriendInfoOptionSelects` không còn dùng**"*.
`TC-REGSHARED001-02` (chế độ liên kết friend info) chỉ kiểm *"Mapping friend info của từng label vẫn đúng"* — trên **form mới, chưa có friend nào trả lời**. Không TC nào chạy trên form **đã có friend trả lời** để xác nhận **giá trị friend info của friend cũ không bị xóa** sau khi edit label + sort + Lưu. Đây là rủi ro **mất dữ liệu khách hàng thật**, thuộc `FRIEND-001` (Cao) + `DATA-DB-001` (RULE-07).
→ **Fix**: bổ sung `TC-FRIEND001-01` — §5.

### 4.2 Major (nên fix)

**`[MAJOR-01]` §0.6 #6 — 4 TC mang mã quan điểm nội bộ Studio, không map được coverage**
`TOOL-KNOW-002` · `TOOL-ERRHYG-001` · `TOOL-NEGCTRL-001` · `TOOL-OLDREC-001` không có trong `framework/checklist-lme.md` → 4 TC này **không tính là cover**, kéo theo `F1`, `F3`, `D2` thành `GAP` dù thực tế **có TC và đã pass**.
→ **Fix**: đổi `viewpoint` trên Studio (`testcase_update`), không viết TC mới: `TOOL-KNOW-002` → `FUNC-SEQ-001` · `TOOL-OLDREC-001` → `COMPAT-LEGACY-001` · `TOOL-ERRHYG-001` → `UI-003` · `TOOL-NEGCTRL-001` → `DATA-DB-001`. Sau khi đổi, chạy lại `/review-tc` thì `F1`/`F3`/`D2` sẽ lên `RISK`/`OK`.

**`[MAJOR-02]` RULE-01 — `REG-SHARED-001` (ưu tiên **Cao**) có 5 TC nhưng **cả 5 đều `Normal`****
Thiếu `Abnormal` + `Boundary`, **không TC nào ghi lý do** ở `Ghi chú`. Quan điểm này lại đúng là quan điểm chủ đạo của fix.
→ **Fix**: `TC-REGSHARED001-06` (`Abnormal`) + `TC-REGSHARED001-08` (`Boundary`) ở §5 lấp đủ.

**`[MAJOR-03]` RULE-01 — `OUT-TRUTH-001` (Cao) chỉ có 1 TC `Normal`**
Thiếu case "báo lỗi thì phải đúng nguyên nhân" — đúng mặt trái của bug này (`UI-003` false success).
→ **Fix**: `TC-OUTTRUTH001-02` — §5.

**`[MAJOR-04]` GAP-4 — `DEPLOY-ASSET-001` (Cao): TC duy nhất là kiểm tra tĩnh source VÀ đang `skip`**
Dev tự khai *"KHÔNG bump `config('sns-line.version')` ... trình duyệt đã cache bản JS cũ có thể cần tải lại cứng (Ctrl+F5)"*, đồng thời **mọi tiền đề TC đều yêu cầu "đã hard reload (Ctrl+F5)"** → bộ TC đang **né đúng rủi ro** mà Dev cảnh báo. Evidence bắt buộc của `DEPLOY-ASSET-001` là *"screenshot màn sau **F5 thường** trên browser còn cache bản cũ"* — không có TC nào làm điều này.
→ **Fix**: `TC-DEPLOYASSET001-02` — §5. Đồng thời **chạy lại** `TC-DEPLOYASSET001-01` (đang `skip`).

**`[MAJOR-05]` 2 TC `skip` = không có kết luận test**
`TC-TOOLERRHYG001-01` (null-guard — cover trực tiếp phần thứ 2 của mục 2 "Cách fix") và `TC-DEPLOYASSET001-01`. `skip` **không** phải `pass`; Studio ghi `aiResult = pass` dễ gây hiểu nhầm bộ TC đã xanh toàn bộ.
→ **Fix**: chạy lại 2 TC này, hoặc ghi lý do skip vào `note` trên Studio. Không đề xuất TC mới.

**`[MAJOR-06]` §0.6 #5 — 14/16 TC do AI sinh, `reviewState = leader`, `reviewed = false`**
Bộ TC chưa qua duyệt Leader trên Studio; `test_viewpoint_selection = null` → **không có bảng duyệt quan điểm tầng 1 nào kèm theo bộ TC**. Toàn bộ mapping quan điểm trong report này là do `/review-tc` tự dựng.
→ **Fix**: Leader duyệt trên Studio sau khi xử lý §5.

**`[MAJOR-07]` GAP — `T2`/`T1` chưa cover chế độ hiển thị **ドロップダウン (dropdown)****
`note` của chính `TC-REGSHARED001-04` tự nêu: *"select box (dropdown) chưa có callback drag riêng nên **tester confirm khi chạy**"* — nhưng **không có TC** để confirm, và TC đó vẫn được chấm `pass`. Kho TCs `TC-FORM-137` xác nhận `表示方法` có 2 dạng radio / dropdown dùng chung item.
→ **Fix**: `TC-REGSHARED001-09` — §5.

**`[MAJOR-08]` GAP-5 — `DATA-ID-001`: không TC nào dùng **label trùng nội dung****
Root cause (mục 1) là *"mã tạm của từng lựa chọn bị đánh số lại"* — chính xác là lớp lỗi mà `DATA-ID-001` nhắm tới. Mọi TC đều dùng label phân biệt (A, B, C, D / A1, A2, A3).
→ **Fix**: `TC-DATAID001-01` — §5.

**`[MAJOR-09]` `AP-2` SYMPTOM-ONLY — `Actual result` không có error/log, `Expected result` TRỐNG**
File 01 `Expected result` = *"Redmine không ghi rõ"*. Không có chuẩn phát biểu từ KH để đánh giá "đúng" là gì; mọi Expected trong TC đều do AI suy ra. Xem 3 alternative root cause ở §3.5.
→ **Fix**: hỏi Dev/KH xác nhận alternative root cause #2 (server rebuild — BR-10/BR-12) đã được loại **bằng chạy thực tế** chưa, vì mục 6 VERIFY ghi *"Không kiểm chứng được trên dev DB"*.

**`[MAJOR-10]` `AP-3` HAPPY-PATH-ONLY REGRESSION**
10/16 TC có tiền đề *"Form Builder V3 tạo form **MỚI**"* — data sạch, không edge state. Không TC nào chạy trên form đã có câu trả lời / form phân nhánh / form UI cũ / form ở giới hạn số option.
→ **Fix**: các TC §5 đều đặt tiền đề edge state.

**`[MAJOR-11]` Chất lượng TC — `TC-REGSHARED001-05` có bước điều kiện, expected không đo lường được**
Bước 3 = *"Kiểm tra vùng label sau khi mode thay đổi **và kéo sort lại nếu cần**"* → 2 người chạy ra 2 kịch bản khác nhau; Expected *"thứ tự label **cuối cùng được người dùng sắp xếp**"* không xác định được là thứ tự nào. (Rà chất lượng TC mục 3 + mục 4.)
Đáng tiếc vì đây là TC **giá trị nhất** — nó test đúng mô tả root cause *"danh sách lựa chọn có thể bị thay mới bởi các thao tác khác"*.
→ **Fix**: bỏ nhánh "nếu cần", chốt 1 kịch bản: sort thành `D,A,B,C` → đổi mode → **không** sort lại → Lưu → Expected `D,A,B,C`.

**`[MAJOR-12]` Chất lượng TC — 16/16 TC có `Trạng thái đánh giá spec` TRỐNG (`spec_status = null`)**
Trong khi có ít nhất 2 hành vi **spec KHÔNG ghi**: (a) sau khi kéo mà **không** Lưu thì state đã ghi vào data có bị rollback không; (b) `その他` có kéo được không. Không TC nào ghi `Spec không ghi` + đã hỏi ai → nguy cơ tự suy diễn rồi chấm Đạt.
→ **Fix**: điền `spec_status` cho toàn bộ 16 TC trên Studio.

**`[MAJOR-13]` GAP-8 — nhánh `checkHaveOther` (lựa chọn `その他`) không có TC trực tiếp**
`TC-FUNCSEQ001-02` chỉ ghi trong Expected *"trước lựa chọn 「khác」 **nếu có**"* — không có bước nào bật `その他項目を選択肢に自動追加`. Kho TCs `TC-FORM-144`: *"その他 cố định cuối danh sách, **không sửa/sort/xóa được**"* → đây là ràng buộc cứng mà fix có thể phá.
→ **Fix**: `TC-FUNCSEQ001-07` — §5.

**`[MAJOR-14]` GAP-11 — Màn **quản lý tag** (mẫu fix cùng lớp lỗi) không có TC regression**
Mục 6 VERIFY: *"Mẫu fix đã duyệt cho cùng lớp lỗi (kéo-thả jQuery UI không đồng bộ mảng Vue): `public/js/tag/index_v2.js` dòng 131-142 và 181-192"*. Fix hiện tại **sao chép pattern** từ đó. `REG-SHARED-001` yêu cầu *"Fix bug ở chức năng A → rà chức năng B có logic tương tự"*.
→ **Fix**: `TC-REGSHARED001-10` — §5 (chi phí thấp, giá trị regression cao).

**`[MAJOR-15]` GAP — `COMPAT-LEGACY-001` (Cao) / RULE-09: chưa test nhánh cũ ⇄ mới**
BR-09: `using_old_version=0` (v3) vs `=1` (UI cũ). Form Builder đã version-up. TC duy nhất chạm data cũ (`TC-TOOLOLDREC001-01`) mang mã không hợp lệ và chỉ dựng *"seed record shape cũ"*, không test form UI cũ thật.
→ **Fix**: `TC-COMPATLEGACY001-01` — §5.

**`[MAJOR-16]` Input chưa được tester verify — cả `01-bug-task.md` và `03-dev-impact.md`**
Cả 2 file có `Auto-filled: 2026-09-03 by /new-task` nhưng checkbox **"Tester verify auto-fill chính xác" CHƯA tick** ([01-bug-task.md:42](01-bug-task.md#L42), [03-dev-impact.md:17](03-dev-impact.md#L17)).
Riêng với ticket này rủi ro là **thật, không hình thức**: mục **4.1 của Dev chỉ ghi "File thay đổi"**, nên bảng `F1–F8` dùng làm base cho §3 là do `/new-task` **suy ra từ mục 2 + 3**, chưa có Dev xác nhận. Nếu bảng F sai/thiếu thì toàn bộ Coverage Matrix ở §3 sai theo.
→ **Fix**: tester đọc lại Redmine #34227 (description + journal `132716`), xác nhận bảng `F1–F8` và `T1/T2`, rồi tick 2 checkbox **trước khi** Leader dùng report này để giao việc.

### 4.3 Minor (có thể fix sau)

- **`[MINOR-01]`** RULE-02 — 16/16 TC có `Evidence thực tế` **trống** dù 14 TC đã chấm `pass`. `Ghi chú` cũng không ghi **loại** evidence bắt buộc. `FUNC-SEQ-001` yêu cầu *"screenshot sau chuỗi thao tác + sau F5 (**2 ảnh cạnh nhau**)"*.
- **`[MINOR-02]`** `DATA-TEXT-001` — không TC nào dùng label chứa emoji / `①②③` / `㈱`. Label được hiển thị trên LINE và export.
- **`[MINOR-03]`** `LIST-001` — `changePage` nằm trong caller Dev đã check (mục 3) nhưng không TC nào kéo sort ở **trang 2+** của form nhiều trang. (Kho có `TC-FORM-26` cho sort list form khi phân trang.)
- **`[MINOR-04]`** `CONC-003` — không TC nào kéo-thả trong lúc request trước chưa trả về (Slow 3G). Rủi ro thấp với fix này.
- **`[MINOR-05]`** Chất lượng TC mục 7 — `TC-FUNCSEQ001-01`/`TC-TOOLKNOW002-01` dùng label `A`, `B`, `C`, `D`, `A_edit`. Với bug về **thứ tự**, label 1 ký tự khiến screenshot khó đọc và không phát hiện được lỗi trùng tên (xem `[MAJOR-08]`).
- **`[MINOR-06]`** 15/16 TC gắn `env_tag = local-only` nhưng thực tế chạy `staging`; 16/16 gắn `exec_mode = auto` nhưng `last_exec.source = manual`. Metadata Studio sai lệch so với thực tế thực thi.

### 4.4 Nit (gợi ý)

- **`[NIT-01]`** `TC-DEPLOYASSET001-01` (đếm 5 callback + null-guard trong source) nên chuyển thành **bước tiền kiểm của task**, không phải test case — nó không sinh evidence hành vi.
- **`[NIT-02]`** BR-08/BR-14 (Google Spreadsheet): thứ tự option đổi **có** làm đổi dữ liệu ghi ra Spreadsheet của form không? Fix **không chạm** layer này nên tôi **không** đề xuất TC (tránh over-coverage layer downstream) — nêu để Leader quyết.
- **`[NIT-03]`** RULE-11 — §4 `checklist-lme.md` (`FORM-01`) chưa đủ bằng chứng, chỉ nêu ở mức gợi ý, không dùng để flag.

---

## 4.5 TC trùng lặp nội dung

Đã rà **16/16 TC** theo 4 yếu tố (`mã quan điểm` × `loại case` × `đối tượng + thao tác` × `tiền đề tương đương`). Phát hiện **1 nhóm trùng**.

| Nhóm trùng | TC giữ lại | TC đề nghị xóa / gộp | Loại trùng | 4 yếu tố trùng nhau | Severity |
|---|---|---|---|---|---|
| DUP-1 | `TC-FUNCSEQ001-01` (Studio `#15288`, người viết, mã quan điểm **hợp lệ**) | `TC-TOOLKNOW002-01` (Studio `#12833`) → **GỘP, không xóa thẳng** | `DUP-EXACT` | ① mã quan điểm: khác trên giấy (`TOOL-KNOW-002` vs `FUNC-SEQ-001`) nhưng `TOOL-KNOW-002` là mã nội bộ Studio, không phải quan điểm độc lập → coi như trùng. ② loại case: cả 2 `Normal`. ③ đối tượng + thao tác: **giống hệt** — item radio, edit label `A`→`A_edit`, kéo thành `D,A_edit,B,C`, Lưu, hard reload. ④ tiền đề: cùng "Form Builder V3, form mới sau fix, đã hard reload". Expected tương đương. | `[MINOR]` |

**Gate trước khi đề nghị xóa (đã chạy)**: giả định xóa `TC-TOOLKNOW002-01` → chạy lại §3 + §3.6 trên tập còn lại → **mất** 2 thứ mà `TC-FUNCSEQ001-01` không có: (a) tiền đề nêu **rõ chế độ "KHÔNG liên kết"** (= impact `F3` / `initSortNotLink`), (b) Expected có **oracle DB** (*"DB `selectable.items` lưu đúng thứ tự"*). Vì vậy **đổi đề xuất từ "xóa" sang "gộp"**:

> Bổ sung vào `TC-FUNCSEQ001-01`: tiền đề *"câu hỏi radio ở chế độ **KHÔNG liên kết**, ≥4 label"* + Expected *"DB `selectable.items` lưu đúng thứ tự và nội dung label mới"*. **Sau khi đã gộp** mới xóa `TC-TOOLKNOW002-01` trên Studio (`testcase_delete`).
> ⚠️ Nếu Leader chọn phương án `[MAJOR-01]` (đổi `viewpoint` của `TC-TOOLKNOW002-01` sang `FUNC-SEQ-001`) thì **giữ cả 2 TC cũng chấp nhận được** — khi đó chúng thành `TC-FUNCSEQ001-0x` và trùng lặp chỉ còn là dư thừa nhẹ, không che GAP nào.

Không phát hiện `DUP-SUBSET` / `DUP-INFLATE` / `DUP-CONFLICT` nào khác. Đặc biệt đã kiểm và **kết luận KHÔNG trùng**: `TC-REGSHARED001-05` (sort → đổi mode → Lưu) vs `TC-REGSHARED001-03/04` (đổi mode → sort → Lưu) — **thứ tự thao tác ngược nhau**, và chiều của `-05` mới đúng mô tả root cause.

---

## 5. TCs đề xuất bổ sung

### 5a — Đối chiếu kho TCs

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | [kho-tcs/fa011-taobieumau-フォーム作成.md](../../kho-tcs/fa011-taobieumau-フォーム作成.md) (FA-011, tra qua `LME-SYSTEM-SPEC.md` dòng 687) |
| Vùng regression phát hiện từ kho | `TC-FORM-142` (kéo thả sắp xếp option radio/dropdown) · `TC-FORM-144` (`その他` cố định cuối, không sort được) · `TC-FORM-137` (`表示方法` radio ⇄ dropdown) · `TC-FORM-173/174/175` (xóa **option remind** → hủy/giữ lịch remind của friend) · `TC-FORM-178` (item chẩn đoán `単一選択`/`複数選択`) · `TC-FORM-100` (move item ở **form rẽ nhánh**) · `TC-FORM-102` (sort option bên trong item checkbox) · `TC-FORM-118`/`TC-FORM-176` (data đời cũ) |
| Conflict expected vs kho | **Không** — không TC đề xuất nào mâu thuẫn expected của kho |
| GAP dùng lại TC kho (không viết mới) | **GAP-7** → `TC-FORM-142` — *"Kéo thả sắp xếp option: lưu thì giữ thứ tự mới, **không lưu thì giữ thứ tự cũ**"*. Đây là mặt trái trực tiếp của fix (fix ghi thứ tự vào data **ngay lúc thả**, nên phải chứng minh việc **không** bấm Lưu vẫn không làm đổi dữ liệu đã lưu). Chỉnh cho hợp bug: thêm bước **edit nội dung label trước khi kéo**, và rời trang bằng cả 2 cách (bấm Hủy / reload không lưu). |
| Xác nhận chống trùng | Đã đối chiếu **16 TC** ở BƯỚC 0 + kho `fa011` — **không TC đề xuất nào trùng** (kiểm theo 4 yếu tố; 12 TC dưới đây khác bộ BƯỚC 0 ở ít nhất yếu tố ③ *đối tượng + thao tác* hoặc ④ *tiền đề*) |

### 5b — TC bổ sung (14 cột)

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-REGSHARED001-06 | UI | REG-SHARED-001 | Item nhắc lịch (remind) | Abnormal | manual | staging | Kéo sort option của câu hỏi **nhắc lịch** rồi Lưu — lịch remind đã đặt của friend không gắn nhầm option | - Admin, đã chọn bot<br>- Form V3 có item **nhắc lịch (remind)** với 3 option remind: `R1 (7 ngày)`, `R2 (14 ngày)`, `R3 (30 ngày)`<br>- Đã có **2 friend thật** submit form: friend X chọn `R1`, friend Y chọn `R3` → 2 lịch remind đang chờ gửi<br>- Đã hard reload trước khi thao tác | 1. Mở item nhắc lịch trong Form Builder<br>2. Edit nội dung `R1` → `R1_edit`<br>3. Kéo-thả đổi thứ tự option thành `R3, R1_edit, R2`<br>4. Bấm Lưu 「保存」<br>5. Hard reload, mở lại item → đối chiếu thứ tự<br>6. Mở màn chi tiết friend X và friend Y → xem lịch remind đang chờ<br>7. Chờ tới mốc gửi (hoặc đẩy thời gian) → kiểm tin nhắc **nhận thật trên LINE app** | 3 option `R1(7d)`, `R2(14d)`, `R3(30d)`; thứ tự đích `R3, R1_edit, R2`; friend X chọn R1, friend Y chọn R3 | 1. Thứ tự option sau reload đúng `R3, R1_edit, R2`.<br>2. Lịch remind của friend X **vẫn gắn option R1_edit** (mốc 7 ngày, không đổi thành 30 ngày), friend Y **vẫn gắn R3** (mốc 30 ngày).<br>3. Tin nhắc nhận trên LINE app đúng friend, đúng mốc thời gian, đúng nội dung option tương ứng. | | Lấp GAP-1 / cover impact `T2` · dẫn từ `TC-FORM-174` · Đánh giá spec: **Spec không ghi** (đã hỏi Dev — chờ trả lời) · Evidence: screenshot thứ tự sau F5 + screenshot lịch remind của 2 friend trước/sau + ảnh tin nhắc trên LINE app thật (RULE-06) · regression |
| TC-REGSHARED001-07 | UI | REG-SHARED-001 | Item chẩn đoán & giới tính | Normal | manual | staging | Kéo sort option câu hỏi **chẩn đoán** và **giới tính** rồi Lưu — thứ tự đúng, kết quả chẩn đoán không đổi | - Admin, đã chọn bot<br>- Form V3 có item **chẩn đoán** `単一選択` với 4 option gắn kết quả chẩn đoán khác nhau, và 1 item **giới tính**<br>- Tab 診断コンテンツ đã cấu hình kết quả cho từng option<br>- Đã hard reload | 1. Mở item chẩn đoán, edit nội dung 1 option<br>2. Kéo-thả đổi thứ tự 4 option<br>3. Mở item giới tính, kéo đổi thứ tự option<br>4. Bấm Lưu 「保存」<br>5. Hard reload, mở lại cả 2 item<br>6. Mở form public, trả lời chọn option vừa edit → xem kết quả chẩn đoán trả về | Item chẩn đoán 4 option; item giới tính 2–3 option; đổi thứ tự cả 2 | 1. Thứ tự option của **cả 2 item** sau reload đúng như đã kéo.<br>2. Nội dung option đã edit giữ nguyên.<br>3. Kết quả chẩn đoán trả về **vẫn khớp option người dùng chọn** (không bị lệch sang kết quả của option khác do đổi thứ tự). | | Lấp GAP-1 / cover impact `T2` · dẫn từ `TC-FORM-178` · Đánh giá spec: Spec ghi rõ (feature-spec §2 SCR-FA11-06) · Evidence: screenshot 2 item sau F5 + screenshot kết quả chẩn đoán phía form public · regression |
| TC-REGSHARED001-08 | UI | REG-SHARED-001 | Item radio & dropdown | Boundary | manual | staging | Kéo sort ở **số option lớn nhất thực tế** (chế độ liên kết tag) rồi Lưu | - Admin, đã chọn bot<br>- Item radio chế độ **liên kết tag**, tạo **50 option** `OPT-01`…`OPT-50`, mỗi option gắn 1 tag riêng<br>- Ghi rõ nguồn giới hạn: hỏi Dev/tra spec số option tối đa; nếu spec không quy định → dùng quy mô khách lớn nhất<br>- Đã hard reload | 1. Edit nội dung `OPT-01` → `OPT-01_edit`<br>2. Kéo `OPT-50` lên đầu danh sách<br>3. Kéo `OPT-25` xuống cuối danh sách<br>4. Bấm Lưu 「保存」, bấm giờ thời gian phản hồi<br>5. Hard reload, mở lại item, đối chiếu **toàn bộ 50 dòng**<br>6. Đối chiếu mapping tag của `OPT-50`, `OPT-01_edit`, `OPT-25` | 50 option; thứ tự đích: `OPT-50, OPT-01_edit, OPT-02..OPT-24, OPT-26..OPT-49, OPT-25`; phép đếm tay: 50 dòng, 50 tag phân biệt | 1. Sau reload đủ **50** option, thứ tự khớp đúng thứ tự đích từng dòng.<br>2. Tag của từng option **vẫn đúng option đó** (không bị dịch theo vị trí).<br>3. Thời gian Lưu + render lại danh sách ≤ ngưỡng chấp nhận của màn builder, UI không treo. | | Lấp GAP-1 + RULE-01 (`Boundary` cho REG-SHARED-001) + `PERF-LARGE-001` + `FUNC-004` · Đánh giá spec: **Spec không ghi** giới hạn số option (đã hỏi Dev) · Evidence: screenshot đầu/cuối danh sách sau F5 + bảng đối chiếu mapping tag + số đo thời gian |
| TC-FUNCSEQ001-06 | UI | FUNC-SEQ-001 | Form phân nhánh (分岐タイプ) | Abnormal | manual | staging | Form **phân nhánh**: edit label của option dùng làm điều kiện chuyển trang rồi kéo sort → nhánh vẫn đúng | - Admin, đã chọn bot<br>- Form `form_type=2` (**分岐**) có ít nhất 3 trang<br>- Trang 1 có item radio 3 option: `Đi trang A`, `Đi trang B`, `Kết thúc`; đã cấu hình `next_page_type=2` map từng option sang trang tương ứng<br>- Đã hard reload | 1. Mở item radio ở trang 1<br>2. Edit label `Đi trang A` → `Đi trang A (mới)`<br>3. Kéo-thả đổi thứ tự thành `Kết thúc, Đi trang A (mới), Đi trang B`<br>4. Bấm Lưu 「保存」<br>5. Hard reload, mở lại cấu hình phân nhánh của trang 1<br>6. Mở form public, lần lượt chọn **từng** option và submit → xác nhận trang tiếp theo | 3 option map 3 nhánh; đổi cả nội dung lẫn thứ tự trong cùng 1 lần lưu | 1. Sau reload, thứ tự option đúng `Kết thúc, Đi trang A (mới), Đi trang B`.<br>2. Cấu hình phân nhánh vẫn map **đúng theo option**, không theo vị trí: chọn `Đi trang A (mới)` → sang trang A; `Đi trang B` → trang B; `Kết thúc` → kết thúc form.<br>3. Không option nào mất mapping (không rơi về nhánh mặc định). | | Lấp GAP-2 / cover impact `T1` · Nguồn spec: **BR-10** — `next_page_setting [{value:"label", pageId}]`, rebuild từ danh sách option khi lưu · dẫn từ `TC-FORM-100` · Đánh giá spec: Spec ghi rõ (BR-10) · Evidence: screenshot cấu hình phân nhánh sau F5 + video chọn từng option ở form public |
| TC-FRIEND001-01 | UI | FRIEND-001 | Item radio — liên kết thông tin bạn bè | Abnormal | manual | staging | Edit label + kéo sort ở chế độ **liên kết friend info** — giá trị friend info của friend đã trả lời KHÔNG bị xóa | - Admin, đã chọn bot<br>- Item radio chế độ **liên kết thông tin bạn bè**, friend info type `select` với 3 option `Nam`, `Nữ`, `Khác`<br>- Đã có **2 friend thật** submit form: friend X = `Nam`, friend Y = `Khác`<br>- Đã ghi lại số đếm `total_user_has_value` của friend info đó trước khi thao tác<br>- Đã hard reload | 1. Ghi lại: màn chi tiết friend X, friend Y đang hiển thị giá trị gì; số đếm friend info hiện tại<br>2. Mở item radio, edit label `Khác` → `Khác (mới)`<br>3. Kéo-thả đổi thứ tự thành `Khác (mới), Nam, Nữ`<br>4. Bấm Lưu 「保存」<br>5. Hard reload, mở lại item<br>6. Mở màn chi tiết friend X và friend Y<br>7. Mở màn quản lý thông tin bạn bè → đối chiếu danh sách option và số đếm<br>8. Click vào số đếm → xác nhận đúng danh sách friend | 3 option; friend X = `Nam`, friend Y = `Khác`; phép đếm tay: 2 friend có value, sau thao tác vẫn phải là 2 | 1. Thứ tự option sau reload đúng `Khác (mới), Nam, Nữ`.<br>2. Friend X **vẫn** = `Nam`; friend Y **vẫn** có giá trị (`Khác` hoặc `Khác (mới)` — ghi lại hành vi thực tế để chốt spec), **không bị rỗng**.<br>3. Số đếm `total_user_has_value` **vẫn = 2**, không giảm.<br>4. Danh sách option của friend info không sinh option mồ côi / không xóa nhầm option đang có người dùng.<br>5. Click số đếm mở đúng 2 friend X, Y. | | Lấp GAP-3 / cover impact `F4`, `T1` · Nguồn spec: **BR-12** — *"Nếu options thay đổi → xóa `FriendInformationValue` và `FriendInfoOptionSelects` không còn dùng"* · Đánh giá spec: **Spec không ghi** rõ hành vi khi label bị đổi tên (đã hỏi Dev) · Evidence: screenshot chi tiết 2 friend + số đếm **trước và sau** + ảnh danh sách option friend info (RULE-07 3 tầng) |
| TC-DEPLOYASSET001-02 | API | DEPLOY-ASSET-001 | Release asset JS Form Builder | Normal | manual | Tất cả | Browser còn cache JS cũ, chỉ **F5 thường** (không Ctrl+F5) — kéo sort + Lưu vẫn đúng | - Có 1 browser **đã mở màn Form Builder V3 bằng bản TRƯỚC fix** để cache `setting_form_items.js` bản cũ<br>- Sau đó deploy bản có fix (`ai_fixbug_34227`) lên môi trường test<br>- **KHÔNG** xóa cache, **KHÔNG** Ctrl+F5<br>- Dev xác nhận `config('sns-line.version')` **chưa** được bump | 1. Trên browser đã cache: bấm **F5 thường**<br>2. Mở DevTools → tab Network, lọc `setting_form_items.js`<br>3. Ghi lại: status code, query version, `from disk cache` hay `200`<br>4. Mở item radio ≥3 label, edit 1 label rồi kéo đổi thứ tự<br>5. Bấm Lưu 「保存」<br>6. F5 thường lần nữa, đối chiếu thứ tự<br>7. Lặp lại toàn bộ trên browser thứ 2 đã Ctrl+F5 để so sánh | Browser A: chỉ F5 thường. Browser B: Ctrl+F5. Cùng thao tác kéo sort giống nhau | 1. Ghi nhận rõ `setting_form_items.js` đang là **bản cũ hay mới** sau F5 thường (status + query version, không 404).<br>2. **Nếu browser A còn chạy JS cũ** → thứ tự label vẫn sai như trước fix ⇒ **phải kết luận rõ**: fix chỉ có hiệu lực sau khi đội release bump version, và ghi cảnh báo cho release note.<br>3. Browser B (Ctrl+F5) → thứ tự đúng.<br>4. Không có asset nào 404, font/icon không tofu. | | Lấp GAP-4 / cover impact `BUG` ở tầng phát hành · Gộp thêm `DATA-CACHE-001` + `DEPLOY-LIVE-001` · Đánh giá spec: Spec ghi rõ (checklist DEPLOY-ASSET-001) · Evidence: **screenshot DevTools Network** (query version + status) + screenshot màn sau **F5 thường** trên browser còn cache bản cũ · ⚠️ Phạm vi ENV = `Tất cả` vì phải đối chiếu staging ⇄ product (product mới là nơi cache thật của khách) |
| TC-DATAID001-01 | Data | DATA-ID-001 | Item radio & dropdown | Abnormal | manual | staging | Hai option **trùng nội dung** — kéo sort rồi Lưu không gộp / không hoán đổi nhầm | - Admin, đã chọn bot<br>- Item radio chế độ **liên kết tag** với 4 option, trong đó **2 option trùng nội dung y hệt**: `Hà Nội`, `Hà Nội`, `Đà Nẵng`, `HCM`<br>- 2 option `Hà Nội` gắn **2 tag KHÁC nhau**: `tag-HN-1`, `tag-HN-2`<br>- Đã hard reload | 1. Ghi lại option nào (thứ 1 hay thứ 2) đang gắn tag nào<br>2. Kéo option `Hà Nội` **thứ 2** lên vị trí đầu tiên<br>3. Bấm Lưu 「保存」<br>4. Hard reload, mở lại item<br>5. Đối chiếu từng dòng: nội dung + tag gắn kèm | 4 option, 2 option trùng tên `Hà Nội` gắn `tag-HN-1` / `tag-HN-2` | 1. Sau reload có **đủ 4** option, **không bị gộp thành 3**.<br>2. Option đầu tiên là `Hà Nội` gắn **`tag-HN-2`** (đúng option đã kéo), option còn lại gắn `tag-HN-1`.<br>3. Không option nào mất tag hoặc bị gán tag của option kia. | | Lấp GAP-5 · Đối chứng **alternative root cause #1** ở §3.5 (mã tạm bị đánh số lại) · Đánh giá spec: **Spec không ghi** (đã hỏi Dev) · Evidence: bảng đối chiếu 4 dòng option ↔ tag trước/sau + screenshot sau F5 |
| TC-REGSHARED001-09 | UI | REG-SHARED-001 | Item radio & dropdown — chế độ hiển thị dropdown | Normal | manual | staging | Chế độ hiển thị **ドロップダウン** — kéo sort option rồi Lưu giữ đúng thứ tự | - Admin, đã chọn bot<br>- Item câu hỏi lựa chọn, `表示方法` = **ドロップダウン (dropdown)**, có 4 option `D1..D4`<br>- Đã hard reload | 1. Mở item, xác nhận `表示方法` đang là dropdown<br>2. Edit nội dung `D1` → `D1_edit`<br>3. Kéo-thả đổi thứ tự thành `D4, D1_edit, D2, D3`<br>4. Bấm Lưu 「保存」<br>5. Hard reload, mở lại item<br>6. Mở form public → mở dropdown xem thứ tự hiển thị<br>7. Đổi `表示方法` sang ラジオボタン rồi Lưu lại → kiểm thứ tự có giữ nguyên | 4 option `D1..D4`; thứ tự đích `D4, D1_edit, D2, D3` | 1. Sau reload trong builder: thứ tự đúng `D4, D1_edit, D2, D3`.<br>2. Dropdown ở **form public** hiển thị đúng thứ tự đó.<br>3. Sau khi đổi `表示方法` sang radio và Lưu lại, thứ tự **vẫn** giữ nguyên, không reset. | | Lấp GAP-6 (`[MAJOR-07]`) / cover impact `T1` · Trả lời trực tiếp nghi vấn tự nêu trong `note` của `TC-REGSHARED001-04` · dẫn từ `TC-FORM-137` · Đánh giá spec: Spec ghi rõ (feature-spec §2 SCR-FA11-03) · Evidence: screenshot builder sau F5 + screenshot dropdown ở form public · regression |
| TC-FUNCSEQ001-07 | UI | FUNC-SEQ-001 | Item radio — lựa chọn 「その他」 | Abnormal | manual | staging | Bật `その他項目を選択肢に自動追加` — kéo sort không đẩy được 「その他」 khỏi vị trí cuối | - Admin, đã chọn bot<br>- Item radio 4 option `A, B, C, D`, đã **bật** `その他項目を選択肢に自動追加` → xuất hiện option `その他` ở cuối<br>- Đã hard reload | 1. Thử kéo option `その他` lên vị trí đầu danh sách<br>2. Kéo `D` lên đầu (thao tác hợp lệ)<br>3. Bấm Lưu 「保存」<br>4. Hard reload, mở lại item<br>5. Mở form public kiểm thứ tự hiển thị<br>6. Tắt rồi bật lại `その他項目...`, Lưu, reload lại | 4 option + `その他`; thử kéo `その他` lên đầu | 1. Không kéo được `その他` (bị chặn) **hoặc** kéo được nhưng sau Lưu nó **tự về cuối** — ghi lại hành vi thực tế để chốt spec.<br>2. Thứ tự 4 option còn lại sau reload là `D, A, B, C`, `その他` **luôn ở cuối cùng**.<br>3. Form public hiển thị `その他` cuối danh sách.<br>4. Sau khi tắt/bật lại `その他項目...`, thứ tự 4 option kia không bị xáo. | | Lấp GAP-8 (`[MAJOR-13]`) · Kiểm nhánh `checkHaveOther` + `arrNotInSort` trong `sortOptionItemForm` (impact `F1`) · dẫn từ `TC-FORM-144` · Đánh giá spec: **Spec không ghi** hành vi khi cố kéo `その他` (đã hỏi Dev) · Evidence: video thao tác kéo + screenshot sau F5 |
| TC-COMPATLEGACY001-01 | Data | COMPAT-LEGACY-001 | Form đời cũ ⇄ form mới | Normal | manual | staging | Form tạo **trước fix** (thứ tự đã sai) và form **UI cũ** — mở, sửa, lưu lại đều đúng | - Chuẩn bị **2 form**: (a) form tạo trước ngày deploy fix, có item radio đang lưu **sai thứ tự**; (b) form có `using_old_version = 1` (UI cũ)<br>- Admin, đã chọn bot, đã hard reload bản JS mới | 1. Mở form (a), mở item radio — **chưa thao tác gì** → ghi lại thứ tự hiển thị<br>2. Kéo lại đúng thứ tự mong muốn, bấm Lưu, hard reload, đối chiếu<br>3. Mở form (b) UI cũ → xác nhận mở được, không lỗi JS ở Console<br>4. Với form (b): thử sửa 1 option rồi Lưu (hoặc xác nhận hệ thống chặn edit theo spec)<br>5. Mở link form public **cũ** của form (a) → xác nhận vẫn truy cập được | Form (a) tạo trước fix, thứ tự sai; form (b) `using_old_version=1` | 1. Form (a) khi mở lần đầu **vẫn giữ thứ tự cũ sai** — hệ thống **KHÔNG tự migrate** (đúng khai báo `D2` của Dev).<br>2. Sau khi kéo lại + Lưu, thứ tự đúng và bền qua reload.<br>3. Form (b) UI cũ mở được, **không lỗi JS trên Console**, hành vi edit đúng như spec BR-09.<br>4. Link form public cũ vẫn truy cập được, hiển thị đúng thứ tự đã lưu. | | Lấp GAP-10 + `[MAJOR-15]` / cover impact `D2` · RULE-09 (test song song nhánh cũ ⇄ mới) · Nguồn spec: **BR-09** `using_old_version` · dẫn từ `TC-FORM-118`, `TC-FORM-176` · Đánh giá spec: Spec ghi rõ (BR-09) · Evidence: screenshot **cả 2 nhánh** cũ/mới + ảnh Console không lỗi |
| TC-REGSHARED001-10 | UI | REG-SHARED-001 | Màn quản lý thẻ (FA-012) — sort tag | Normal | manual | staging | Regression màn **quản lý tag** (mẫu fix cùng lớp lỗi) — kéo sort tag rồi Lưu vẫn đúng | - Admin, đã chọn bot<br>- Màn `タグ管理` (FA-012) có ≥4 tag trong 1 folder<br>- Đã hard reload | 1. Mở màn quản lý tag<br>2. Edit tên 1 tag<br>3. Kéo-thả đổi thứ tự tag<br>4. Bấm Lưu<br>5. Hard reload, đối chiếu thứ tự và tên tag<br>6. Kiểm tag hiển thị đúng thứ tự ở 1 nơi tham chiếu khác (VD dropdown chọn tag trong điều kiện gửi tin) | ≥4 tag; đổi tên 1 tag + đổi thứ tự | 1. Thứ tự tag sau reload đúng như đã kéo, tên đã sửa giữ nguyên.<br>2. Thứ tự tag hiển thị nhất quán ở nơi tham chiếu khác.<br>3. Không phát sinh lỗi JS trên Console. | | Lấp GAP-11 (`[MAJOR-14]`) · Mục 6 VERIFY của Dev nêu `public/js/tag/index_v2.js` là **mẫu fix cùng lớp lỗi** → `REG-SHARED-001` yêu cầu rà chức năng B có logic tương tự · Đánh giá spec: Spec ghi rõ (LME-SYSTEM-SPEC §3.9 FA-012) · Evidence: screenshot sau F5 + screenshot nơi tham chiếu · regression |
| TC-OUTTRUTH001-02 | API | OUT-TRUTH-001 | Item radio — lưu thất bại | Abnormal | manual | staging | Lưu **thất bại** (ngắt mạng) — báo lỗi đúng nguyên nhân, KHÔNG lưu nửa vời | - Admin, đã chọn bot<br>- Item radio 4 label `A, B, C, D` đã lưu đúng thứ tự này<br>- DevTools mở sẵn tab Network<br>- Đã hard reload | 1. Edit label `A` → `A_edit`, kéo đổi thứ tự thành `D, A_edit, B, C`<br>2. Trong DevTools bật **Offline** (hoặc chặn request `saveV3`)<br>3. Bấm Lưu 「保存」<br>4. Quan sát thông báo trên UI + response ở tab Network<br>5. Bật lại mạng, **hard reload**, mở lại item → đối chiếu thứ tự | Thứ tự đã lưu trước đó `A, B, C, D`; thao tác chưa lưu được `D, A_edit, B, C` | 1. UI hiển thị **thông báo lỗi đúng nguyên nhân** (lỗi kết nối / lưu thất bại), **KHÔNG** hiện thông báo lưu thành công.<br>2. Không màn trắng, không loading vô hạn.<br>3. Sau khi reload: thứ tự **vẫn là `A, B, C, D`** và label `A` **chưa** đổi tên — không lưu nửa vời (thứ tự mới mà tên cũ, hoặc ngược lại).<br>4. Thao tác lại khi có mạng thì Lưu thành công bình thường. | | Lấp `[MAJOR-03]` (RULE-01 cho OUT-TRUTH-001) + `UI-003` false success · Đây là mặt trái trực tiếp của fix: thứ tự được ghi vào data **ngay lúc thả**, phải chứng minh khi Save fail thì dữ liệu đã lưu không bị chạm · Đánh giá spec: **Spec không ghi** (đã hỏi Dev) · Evidence: screenshot thông báo lỗi + screenshot tab Network + screenshot sau reload |

**GAP dùng lại TC kho (không viết mới)**

> **GAP-7** → dùng lại **`TC-FORM-142`** (kho FA-011, `FUNC-SORT-001`, `Item radio & dropdown`, Normal) — *"Kéo thả sắp xếp option: lưu thì giữ thứ tự mới, **không lưu thì giữ thứ tự cũ**"*.
> **Cần chỉnh cho hợp bug #34227**: thêm bước **edit nội dung label trước khi kéo**, và test cả 2 cách rời màn không lưu (bấm Hủy / reload trực tiếp). Lý do bắt buộc chạy lại TC này sau fix: fix **đổi thời điểm ghi** thứ tự (từ lúc bấm Lưu → lúc thả chuột), nên nhánh "không lưu" là nhánh **có khả năng hồi quy cao nhất** và hiện **không TC nào** trong bộ 16 TC chạm tới.

---

## 6. Spec update needed

| # | Vấn đề | Nguồn | Cần ai chốt |
|---|---|---|---|
| 1 | **Hành vi khi kéo sort rồi KHÔNG lưu**: sau fix, thứ tự được ghi vào data ngay lúc thả chuột. Nếu user rời màn / bấm Hủy thì thứ tự đã lưu trong DB có bị chạm không? Spec FA-011 không định nghĩa. Kho `TC-FORM-142` khẳng định *"không lưu thì giữ thứ tự cũ"* → cần Dev xác nhận fix không phá ràng buộc này | `03-dev-impact.md` mục 2 · kho `TC-FORM-142` | **Dev + Leader** |
| 2 | **BR-12 — hành vi khi ĐỔI TÊN option đang liên kết friend info**: spec chỉ ghi *"Nếu options thay đổi → xóa `FriendInformationValue` và `FriendInfoOptionSelects` không còn dùng"*, không nói rõ "thay đổi" gồm **đổi tên** hay chỉ **thêm/xóa**. Đây là ranh giới giữa "hành vi đúng" và "mất dữ liệu khách hàng" | `spec-features/admin/form-answer/feature-spec.md` BR-12 | **Dev + PM** |
| 3 | **BR-10 — khoá phân nhánh bằng chuỗi label**: `next_page_setting` map `{value: "label"}`. Đổi tên label ⇒ nhánh khoá theo tên cũ có được rebuild đúng không? Spec ghi *"rebuild từ danh sách option hiện tại"* nhưng không nói rebuild theo **tên** hay theo **index** | `feature-spec.md` BR-10 | **Dev** |
| 4 | **Giới hạn số option** của item radio/checkbox — `FUNC-004` yêu cầu TC **ghi rõ nguồn của giới hạn**, hiện không tra được trong spec FA-011 | `feature-spec.md` (không có) | **Dev** |
| 5 | **`その他` có kéo được không** — kho `TC-FORM-144` nói *"không sửa/sort/xóa được"*, nhưng code có nhánh `checkHaveOther` xử lý `arrNotInSort` ⇒ hàm ý là **có thể kéo nhưng bị đẩy về cuối**. 2 mô tả không khớp nhau | kho `TC-FORM-144` vs `03-dev-impact.md` mục 3 | **Dev + Leader** |
| 6 | **Expected result của bug gốc trống** — Redmine #34227 không phát biểu kết quả mong đợi; mọi Expected trong 16 TC là do AI suy ra | `01-bug-task.md` | **Leader** (hoặc hỏi lại KH qua PM) |

---

> Report là **draft cho Leader verify**. TC Studio là read-only — mọi đề xuất sửa/xóa/đổi mã quan điểm phải thực hiện trên Studio (`testcase_update` / `testcase_delete`) rồi fetch lại.
