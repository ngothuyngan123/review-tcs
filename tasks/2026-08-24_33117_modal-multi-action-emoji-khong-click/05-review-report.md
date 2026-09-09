# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | `#33117 — [Modal multi action] Action text không click được phần emoji` |
| Reviewer (Leader) | `<Leader ký tên>` — draft sinh bởi `/review-tc` |
| Tester được review | TCs do **AI (LME TEST STUDIO)** sinh — 13/15; `cucdtk@mcp` 1; `anhptn` 1 |
| Ngày review | 2026-08-25 |
| Version TCs | Studio **round 2** |
| Vòng review | Round 1 (chưa có report trước) |

---

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn | **MCP LME TEST STUDIO task #174** (nguồn sự thật) |
| Ticket · task_id · round · branch | `33117` · `#174` · round **2** · `ai_fixbug_33117` |
| Thời điểm fetch | 2026-08-25 |
| Tổng số TC review | **15** |
| File 04 trong repo vs Studio | **Khớp về tập TC** (15/15, trùng `id` + `temp_id`) — nhưng cột `Kết quả thực thi` của file 04 là snapshot **round 1** (14 Đạt / 1 Không đạt), Studio hiện là **round 2** (15/15 Đạt) → `[MINOR] STALE-EXEC`, xem §4.3 |
| Trạng thái task Studio | `status=done-ai` · `aiResult=pass` · `openBugs=0` · `reviewState=leader` · **`reviewed=false`** · `submittedWithoutMcp=false` |
| Review comments trên Studio | `review_list_comments(174)` → **rỗng** (không có issue vòng trước để tránh raise lại) |
| File `02-spec-reference.md` | **Không có** → fallback [templates/LME-SYSTEM-SPEC.md](../../templates/LME-SYSTEM-SPEC.md) + sub-repo [spec-features/admin/action-settings/shared-spec.md](../../spec-features/admin/action-settings/shared-spec.md) (SC-004) và [spec-features/admin/chat-11/ui/ui-spec.md](../../spec-features/admin/chat-11/ui/ui-spec.md) |

### Cảnh báo bắt buộc từ metadata Studio

| # | Chiều | Kết quả | Flag |
|---|---|---|---|
| 1 | Kết quả thực thi thật | **15/15 pass (100%)** ở round 2 — 0 fail, 0 error, 0 skip, 0 chưa chạy | `OK` về con số — **nhưng xem #2** |
| 2 | TC `fail`/`error` + TC gắn ticket bug | Round 2: không có. **Lịch sử**: `run:402` (round 1) fail → `bug:672` → **Redmine #40131**; `NEW-24` manual fail 09:57:58 → `bug:680` → đóng bằng "re-test pass" 10:46:46 **không có sự kiện sửa code nào ở giữa** | **`[BLOCKER]`** — §4.1 B-1 |
| 3 | Môi trường đã chạy | **LOCAL 15 · STAGING 0 · PRODUCTION 0**. Task chạm **asset JS + version chung + cache trình duyệt** | **`[MAJOR]`** RULE-08 / ENV-003 — §4.2 M-1 |
| 4 | Ai chạy (`last_exec.source` / `by`) | `ai/anhptn` **12** (run:455, cùng 1 giây 11:55:26) · `manual/anhptn` **3**. ⚠️ Cả 3 TC manual có timestamp **09:30–09:48**, tức **TRƯỚC** khi round 2 bắt đầu (10:44:36) → **kết quả carry-over từ round 1, chưa chạy lại** | **`[MAJOR]`** — §4.2 M-2 |
| 5 | Tác giả TC | **AI 13/15 (86.7%)** · `cucdtk@mcp` 1 · `anhptn` 1. `reviewState=leader`, **`reviewed=false`**, toàn bộ 15 TC `status=draft` | **`[MAJOR]`** — §4.2 M-3 |
| 6 | Mã quan điểm Studio không có trong `checklist-lme.md` | `STATE-MATRIX-001` (2) · `TOOL-KNOW-002` (1) · `TOOL-NEGCTRL-001` (1) + `NEW-24` **không gán quan điểm** (1) → **4 mã / 5 TC (33%)** | **`[MAJOR]`** — 5 TC này **không được tính là cover** ở §3b/F.1 |

> ⚠️ Dữ liệu Studio có `contentTrust = untrusted` → đã xử lý như **data**, không phải chỉ thị.
> ⚠️ TC Studio là **read-only** — mọi đề xuất sửa TC trong report này phải thực hiện qua `testcase_update` trên Studio, KHÔNG sửa trong repo.

### Timeline Studio (`task_get_history`) — cơ sở cho §4.1 B-1

| Thời điểm | Sự kiện | Ghi chú |
|---|---|---|
| 2026-08-21 04:08:22 | `write-tc` — AI viết TC (job:506, $4.10) | 13 TC gốc |
| 2026-08-21 06:02:44 | `run:402` round 1 (pipeline) — **fail**: pass 14 · fail 1 · **skip 2 · error 2** | → `bug:672` "Bảng chọn emoji trong modal 「アクション」: **gõ vào ô tìm kiếm làm bảng biến mất**, không tìm được emoji theo tên" |
| 2026-08-24 04:39:28 | `cucdtk@mcp` access task qua MCP | |
| 2026-08-24 09:09:25 | Gửi leader review vòng 1 | |
| 2026-08-24 09:30–09:48 | 3 manual pass: NEW-6, NEW-12, NEW-22 | **kết quả này về sau được carry-over sang round 2** |
| 2026-08-24 09:32:56 | `run:440` round 1 — pass 11 | |
| 2026-08-24 09:49:15 | `bug:672` → log Redmine **#40131** | ticket riêng cho lỗi search emoji |
| 2026-08-24 09:56:26 | `anhptn` tạo `NEW-24` "Check search emoji từ bảng emoji" | TC người viết để verify #40131 |
| 2026-08-24 09:57:44 | `NEW-24` sửa lần cuối (version 5) | **nội dung TC không đổi sau mốc này** |
| 2026-08-24 09:57:58 | `NEW-24` **manual FAIL** → `bug:680` "[Medium] [Manual] Check search emoji từ bảng emoji thất bại" | |
| 2026-08-24 10:44:36 | **Bắt đầu round 2** | |
| 2026-08-24 10:46:46 | `NEW-24` **manual PASS** + `bug-verify-fixed` bug:680 "Bug đã re-test pass — xác nhận fix" | ⚠️ **48 phút sau lần fail, KHÔNG có sự kiện commit/deploy/branch nào ở giữa** |
| 2026-08-24 11:55:26 | `run:455` round 2 — pass 12 | NEW-24 pass lần 2 (auto) |

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — có issue BLOCKER, cần fix và review lại

**Lý do ngắn gọn**: Bộ TC 15/15 Đạt nhưng con số đó **không phản ánh coverage thật**. Fix nằm ở **thư viện dùng chung** `fgEmojiPicker.js` + **nâng version asset chung toàn hệ thống**, trong khi TC chỉ chạm **2/9 tính năng** dùng modal SC-004, **1/3 variant** của modal, **0 TC** có ≥2 action text (đúng class lỗi "chèn nhầm chủ sở hữu"), **0 TC** chạy production, và có **1 TC lật fail→pass không kèm bằng chứng sửa code**.

---

## 2. Tóm tắt cho member

Bộ TC bám rất sát root cause: NEW-1 tái hiện đúng lỗi gốc, NEW-23 dựng được kịch bản chuyển giữa 2 picker, NEW-15/NEW-17/NEW-19 chủ động bắt **rủi ro đối xứng** (sau fix bảng có thể "đóng quá muộn / kẹt không đóng") — đây là tư duy adversarial tốt, không chỉ test happy path.

Điểm phải fix: (1) fix là **shared library + version asset chung**, nhưng phạm vi test mới dừng ở chat 1:1 + tự động trả lời — modal SC-004 còn được **7 tính năng khác** và **2 variant khác** dùng; (2) **chưa có TC nào mở ≥2 action text trong cùng modal**, trong khi REQ-002 (risk High) yêu cầu "chèn đúng dòng action" — đây chính là biến thể trong-modal của lỗi gốc; (3) `NEW-24` chuyển từ Không đạt sang Đạt mà không có mốc sửa code nào — phải bổ sung bằng chứng trước khi đóng.

---

## 3. Coverage Matrix

> Map **quan điểm** đọc từ cột `Mã quan điểm liên kết`; map **impact BUG/F/D/T** suy luận từ tiêu đề / tiền đề / steps / expected. Cột `Exec` = số `pass` / tổng TC cover (round 2).

| Impact | Loại | Priority | TCs map | # TC | Exec | Status |
|---|---|---|---|---|---|---|
| **BUG** — 2 `FgEmojiPicker` cùng gắn handler lên `body`; picker đăng ký sau xoá bảng của picker trước + cả 2 cùng chèn emoji | Fix | — | NEW-1, NEW-23, NEW-2, NEW-9 | 4 | 4/4 | **OK** |
| **F1** — `fgEmojiPicker.js` (`removeEmojiPicker` / `emitEmoji` / `openEmojiSelector` / `bindEvents`) | Function | **Direct** | NEW-1, NEW-2, NEW-4, NEW-5, NEW-9, NEW-15, NEW-17, NEW-19, NEW-23, NEW-24 | 10 | 10/10 | **RISK** — đủ Normal + Abnormal, **thiếu Boundary**; chỉ test cấu hình "1 modal picker + 1 chat picker", chưa test **≥2 picker trong cùng modal** (multi-action) |
| **F2** — `footer.blade.php` — thẻ nạp thư viện emoji đổi từ version cố định → version chung | Function | Direct | NEW-21, NEW-22 | 2 | 2/2 | **RISK** — chỉ verify **1 thẻ script**; không TC nào rà **các thẻ asset khác trong layout còn dùng version cố định** (đây chính là loại lỗi Dev vừa phát hiện) |
| **F3** — `config/sns-line.php` — **nâng version chung** → trình duyệt tải lại **toàn bộ js/css** một lần sau release | Function | Direct | NEW-21 (gián tiếp) | 1 | 1/1 | **GAP thực chất** — không TC nào chạy lại **luồng critical** (mua plan / hủy hợp đồng / gửi tin) sau F5 với version mới; không kiểm 404 / icon-font / glyph → xem §4.1 B-2 |
| **D1** — không có data bị thêm/sửa/xoá | Data | — | — | 0 | — | **N/A** (Dev khai báo "Không có") — ⚠️ nhưng emoji **được lưu xuống DB** khi save bản ghi, NEW-18 có verify save→mở lại; xem §4.3 |
| **T1** — Chat 1:1 (FA-001) | Feature | **High** | NEW-1, NEW-2, NEW-4, NEW-5, NEW-6, NEW-9, NEW-12, NEW-15, NEW-17, NEW-23, NEW-24 | 11 | 11/11 | **OK** |
| **T2** — Action Settings (**SC-004**) — modal multi action dùng chung ở nhiều màn | Feature | **High** | NEW-18, NEW-19 (chỉ 自動応答) | 2 | 2/2 | **GAP** — SC-004 được **9 tính năng** dùng và có **3 variants**; TC cover **2/9 tính năng, 1/3 variant** → §4.1 B-3 |
| **T3** — Auto Reply (FA-003) — verify không hồi quy | Feature | Medium | NEW-18 (Normal), NEW-19 (Abnormal) | 2 | 2/2 | **OK** |

### Chi tiết GAP của T2 — nguồn: [spec-features/admin/action-settings/shared-spec.md](../../spec-features/admin/action-settings/shared-spec.md)

**9 tính năng dùng SC-004** — TC hiện cover 2:

| FA code | Tính năng | TC cover |
|---|---|---|
| FA-001 | Chat 1:1 | ✅ NEW-1…NEW-24 |
| FA-003 | Auto Reply | ✅ NEW-18, NEW-19 |
| FA-004 | Broadcast / Step Message | ❌ **0 TC** |
| FA-009 | Scenario (step delivery) | ❌ **0 TC** |
| FA-010 | Rich Menu (action per button) | ❌ **0 TC** |
| FA-012 | URL Tracking (action khi click link) | ❌ **0 TC** |
| FA-013 | Form Answer (action khi submit) | ❌ **0 TC** |
| FA-014 | Bookmark | ❌ **0 TC** |
| FA-015 | Action Schedule | ❌ **0 TC** |

**3 variants của modal** — TC hiện cover 1:

| Variant | File Blade | TC cover |
|---|---|---|
| **V2** (Main) `modal_select_action.blade.php` — 「アクション」 | file Dev đã check | ✅ toàn bộ TC |
| **V1** (Legacy) `modal_setting_action.blade.php` — 「友だち一括操作」, mở từ Friend List, jQuery thuần | ❌ **0 TC** — Dev **không nhắc tới** trong mục 3 |
| **V3** (Pro Edit) `modal_select_action_pro.blade.php` — 「アクション編集」 | ❌ **0 TC** — Dev **không nhắc tới** trong mục 3 |

### ORPHAN TCs

| TC ID | Title | Lý do | Hành động đề xuất |
|---|---|---|---|
| — | — | Không phát hiện TC lạc chủ đề. `NEW-24` tuy không gán `viewpoint`/`requirement_keys` nhưng nội dung **nằm trong scope F1** (ô tìm kiếm của bảng emoji do `fgEmojiPicker.js` render) | Giữ — nhưng bổ sung metadata, xem §4.2 M-6 |

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| **Fix shape** (mục 2 dev-impact) | **Kết hợp 3 shape**: (1) **Sửa hàm dùng chung** — "Sửa **thư viện chọn emoji dùng chung** (`public/js/fgEmojiPicker.js`)" → `REG-SHARED-001`; (2) **Guard / specific state check** — "thêm **2 điều kiện bảo vệ**"; (3) **Asset / cache** — "cho thẻ nạp file thư viện dùng **số version chung** ... **và nâng version**" → `DEPLOY-ASSET-001`, `DATA-CACHE-001` |
| **Trigger space cần cover** | **(a)** Mọi nơi khởi tạo `FgEmojiPicker` — Dev khẳng định chỉ 2 nơi (`select_action.js:2388`, `chat-v2.js:5511`), **nhưng chưa xác nhận cho V1/V3 của SC-004**. **(b)** Mọi tổ hợp số picker trên 1 trang: **1 picker** (các màn khác) · **2 picker** (chat 1:1) · **≥2 picker trong CÙNG modal** (multi-action nhiều action text) — **tổ hợp thứ 3 chưa test**. **(c)** Mọi asset chịu ảnh hưởng version chung — không chỉ `fgEmojiPicker.js` |
| **Số trigger TCs hiện cover** | **(a)** 2/2 nơi Dev khai báo, 0/2 variant chưa khai báo · **(b) 2/3 tổ hợp** · **(c) 1 asset / toàn bộ js+css** |
| **KH report dạng** | ⚠️ **SYMPTOM-ONLY ở mức cực đoan** — `description` Redmine **TRỐNG HOÀN TOÀN**. Toàn bộ mô tả bug = **tiêu đề ticket** + 1 ảnh + journal `2026-08-19: Ngần check vẫn đang bug`. Không có error message / console log / video |
| **Alternative root causes cần verify** | Dev **không tái hiện được runtime** (`curl host.docker.internal:8000 → 000`), root cause **suy ra từ đọc code + lint**, chưa từng quan sát thực tế. Các nguyên nhân khác cùng tạo triệu chứng "bấm emoji không hiện gì": (1) **asset JS cũ trong cache** — NEW-22 có cover một phần; (2) `z-index` / `overflow` của modal che hoặc cắt bảng emoji; (3) `/full-emoji-list.json` (nguồn dữ liệu emoji, xem [chat-11/ui/ui-spec.md `EP-08`](../../spec-features/admin/chat-11/ui/ui-spec.md)) load lỗi/chậm → bảng render rỗng; (4) bảng render ngoài viewport khi modal đang scroll. **(2)(3)(4) hiện 0 TC** |
| **Anti-patterns dính** | **AP-2** (symptom-only KH report) · **AP-3** (happy-path-only regression — T2 High risk chỉ 1 màn, data sạch) · **AP-4 một phần** (mục "Commit / Pull Request" chỉ có commit hash `e982edc05e`, **không có link PR/diff** để reviewer verify fix shape thực tế). AP-1 / AP-5 / AP-6: **không dính** (fix không phải generic catch; không over-test layer downstream; mục 3 dev-impact đã liệt kê 10 mục) |

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

**[BLOCKER] B-1 — NEW-24: kết quả lật từ Không đạt → Đạt không kèm bằng chứng sửa code**

`NEW-24` "Check search emoji từ bảng emoji" **manual FAIL** lúc `2026-08-24 09:57:58` (sinh `bug:680`), rồi **manual PASS** lúc `10:46:46` và `bug:680` được đóng bằng nhãn `bug-verify-fixed` — "Bug đã re-test pass — xác nhận fix". Trong 48 phút đó:
- `task_get_history` **không có** sự kiện `commit` / `deploy` / `branch` nào;
- Redmine #33117 **không có journal nào** sau 2026-08-21;
- nội dung TC **không đổi** (`updated_at 09:57:44` < thời điểm fail).

Ngoài ra lỗi này đã có ticket riêng: `bug:672` (do runner phát hiện ở `run:402`) → **Redmine #40131** "gõ vào ô tìm kiếm làm bảng biến mất, không tìm được emoji theo tên" — **cùng triệu chứng với NEW-24**.

— **Đề xuất fix**: (1) Leader kiểm tra trạng thái **Redmine #40131** — nếu còn Open thì kết quả Đạt của NEW-24 mâu thuẫn và phải hạ về Không đạt; (2) yêu cầu `anhptn` bổ sung vào Studio evidence lần chạy pass (screenshot/video + commit đã deploy lên local + phiên bản asset trong Network tab); (3) nếu nguyên nhân lần fail là **cache JS bản cũ** thì đó **chính là bug DEPLOY-ASSET-001** đang được test, phải ghi lại chứ không đóng bằng "re-test pass"; (4) theo **RULE-12(3)**, mọi case đã từng Không đạt và được fix **bắt buộc** nằm trong phạm vi regression các release sau.

---

**[BLOCKER] B-2 — FIX-SHAPE: nâng version asset chung ảnh hưởng toàn hệ thống, chỉ verify đúng 1 file**

Mục 2 dev-impact: *"cho thẻ nạp file thư viện trong layout dùng **số version chung** thay vì version cố định cũ (**và nâng version**)"*; mục 7 tự review xác nhận: *"Nâng version chung làm trình duyệt **tải lại toàn bộ js/css một lần** sau khi release"*.

`DEPLOY-ASSET-001` (**Cao**, trigger BẮT BUỘC khi release sửa JS) yêu cầu: *"(3) chỉ F5 thường → **chạy lại luồng critical** (mua plan, hủy hợp đồng, gửi tin); (4) Network: JS/CSS/font trả 200 với query version mới, **không có 404**; (5) font **không fallback**, glyph kanji/kana + dấu tiếng Việt đủ; (6) icon-font sau merge: load lại nhiều lần, **không lúc có lúc mất**"*.

NEW-21 chỉ kiểm **1 request `/js/fgEmojiPicker.js`**; NEW-22 chỉ kiểm bảng emoji mở được. **0/4 yêu cầu còn lại được cover.**

Thêm một điểm cụ thể: bản thân bug này lộ ra rằng **có thẻ asset trong layout đang hard-code version cũ** (Dev sửa đúng 1 thẻ). **Không TC nào rà xem còn thẻ nào khác cùng tình trạng** — đúng loại lỗi vừa phát hiện, nguy cơ lặp lại nguyên vẹn.

— **Đề xuất fix**: bổ sung `TC-DEPLOYASSET001-02/03/04` và `TC-ENV003-01` ở §5.

---

**[BLOCKER] B-3 — REG-SHARED-001 / COMPAT-LEGACY-001: fix ở shared component nhưng chỉ test 2/9 tính năng và 1/3 variant**

`REG-SHARED-001` (**Cao**) yêu cầu *"dev cung cấp **danh sách** nơi ảnh hưởng → test lại **từng mục**"*. Danh sách Dev đưa ở mục 4.3 là **T2: "modal multi action dùng chung ở nhiều màn (tự động trả lời, kịch bản, tag, form, đặt lịch, bán hàng...)"** — kết thúc bằng `...`, tức **không phải danh sách đóng**.

Đối chiếu spec SC-004: modal được **9 tính năng** dùng (FA-001/003/004/009/010/012/013/014/015) và có **3 variants** (V1 legacy `modal_setting_action.blade.php` mở từ Friend List, V2 main, V3 pro `modal_select_action_pro.blade.php`). Mục 3 dev-impact **chỉ nhắc `modal_select_action.blade.php` (V2)** — **V1 và V3 không được nhắc tới ở bất kỳ đâu**.

Rủi ro cụ thể: Dev khẳng định *"chỉ có 2 nơi khởi tạo bộ chọn emoji"* dựa trên quét V2. Nếu **V3 (Pro Edit) cũng khởi tạo picker riêng**, hoặc V1 dùng jQuery truyền thống với binding khác, thì kết luận "các màn khác hành vi không đổi" **chưa được kiểm chứng**. Theo **RULE-09** / `COMPAT-LEGACY-001` (**Cao**), đối tượng đã version-up (V1→V2→V3) **bắt buộc test cả nhánh cũ và mới**.

— **Đề xuất fix**: (1) yêu cầu Dev trả lời dứt điểm — **liệt kê đầy đủ mọi nơi gọi `new FgEmojiPicker`**, bao gồm V1 và V3; (2) bổ sung TC ở §5 (`TC-REGSHARED001-04…06`, `TC-COMPATLEGACY001-01…03`).

---

**[BLOCKER] B-4 — Không có TC nào mở ≥2 action text trong cùng modal (biến thể trong-modal của chính lỗi gốc)**

`REQ-002` (risk **High**) ghi rõ: *"emoji được chèn vào ô nội dung của **đúng action đang thao tác**, **đúng dòng action**"*. Spec SC-004 xác nhận modal **hỗ trợ multi-action**, action type `text` **"Không giới hạn"** số lượng, mỗi action có counter riêng `count_text_content{indexAction}/5,000` và hàm chèn nhận index (`insertAtCursorAction`).

Rà cả 15 TC: **không TC nào thêm quá 1 action 「テキスト」**. Nghĩa là mệnh đề "đúng dòng action" của REQ-002 **chưa từng được verify**.

Đây không phải edge case xa xôi — root cause của ticket **chính là** "picker chèn nhầm sang ô của chủ sở hữu khác". Với 2-3 action text, trigger `.fa-smile-o` khớp **nhiều icon** trong cùng modal, tức là **đúng class lỗi** trong phạm vi hẹp hơn, và **2 điều kiện bảo vệ mới có thể xử lý sai** khi các bảng đều thuộc cùng một instance picker.

— **Đề xuất fix**: bổ sung `TC-FUNCMULTI001-01…03` ở §5. Đây là nhóm TC ưu tiên cao nhất trong report này.

---

### 4.2 Major (nên fix)

**[MAJOR] M-1 — RULE-08 / ENV-003: 15/15 TC chạy ở `env = local`, 0 TC production**

`ENV-003` (**Cao**) — *"Không được đánh × với lý do 'staging đã pass'"*; ở đây thậm chí chưa tới staging. Catalog D ghi rõ production khác biệt: media/asset qua **server riêng `p.lmes.jp` → sync B2**, **loadbalance 2 server**, và `UIC-15` cảnh báo *"Font 404 trên production (media server riêng)"*. Toàn bộ nhóm asset/cache (NEW-21, NEW-22) **không thể kết luận từ local**.

Riêng NEW-22 còn yêu cầu dựng bối cảnh *"đã cache bản cũ **TRƯỚC** khi deploy"* — trên local rất khó dựng thật; note của chính TC ghi *"Nếu không dựng được bối cảnh này, tester ghi **skip kèm lý do** thay vì suy luận từ code"*, nhưng kết quả lại là **pass**. Cần evidence chứng minh bối cảnh đã dựng đúng.

**[MAJOR] M-2 — 3/15 kết quả round 2 là carry-over từ round 1, chưa chạy lại**

Round 2 bắt đầu `10:44:36`. Nhưng NEW-6 (`09:30:26`), NEW-12 (`09:47:56`), NEW-22 (`09:48:08`) đều có `last_exec.at` **trước** mốc đó → 3 TC này **không được chạy lại trong round 2**, chỉ thừa hưởng kết quả cũ. Đây đúng là **3 TC manual rủi ro cao nhất**: output ra LINE app thật (NEW-6), cross-browser (NEW-12), cache trước deploy (NEW-22).

Vì round 2 được mở ra sau khi NEW-24 lật trạng thái (xem B-1), **cần chạy lại cả 3 TC này trong round 2** để loại trừ khả năng môi trường đã đổi giữa 2 vòng.

**[MAJOR] M-3 — 86.7% TC do AI sinh, `reviewed = false`, toàn bộ ở `status = draft`**

13/15 TC `author=AI` (`created_job_id=506`), `reviewState=leader` nhưng **`reviewed=false`** và **không TC nào được approve** (`status=draft` cho cả 15). Đồng thời 12/15 kết quả Đạt do **pipeline AI tự chạy** (`run:455`, tất cả cùng timestamp `11:55:26`). Nhóm rủi ro cao — đặc biệt `NEW-24` (chính là bug #40131) — được kết luận Đạt **bởi AI tự chạy**, không phải QA người bấm tay.

— **Đề xuất**: Leader duyệt và chuyển `status` sang `approved` trước khi coi bộ TC này là baseline; với NEW-24 yêu cầu **QA người chạy tay + evidence**, không nhận kết quả pipeline.

**[MAJOR] M-4 — RULE-01: 0/15 TC loại `Boundary`, trong khi có 3 requirement risk High**

Phân bố `case_type`: Normal 9 · Abnormal 5 · **Boundary 0** · trống 1. REQ-001/002/003 đều `risk = High`. RULE-01 yêu cầu quan điểm ưu tiên **Cao** phải đủ **Normal + Abnormal + Boundary**, thiếu thì **bắt buộc ghi lý do** — không TC nào ghi lý do.

Biên có thật, không phải hình thức: textarea action text **max 5.000 ký tự** kèm counter (spec SC-004 §3.4.3). Chèn emoji sát biên → cần kiểm counter và hành vi chặn. Xem `TC-FUNC004-01…03` ở §5.

**[MAJOR] M-5 — SYMPTOM-ONLY (AP-2): root cause chỉ được suy ra từ đọc code, chưa từng quan sát runtime**

`description` Redmine **trống hoàn toàn**; Dev tự khai *"Trình duyệt/web dev không truy cập được từ container nên **không chạy tái hiện runtime được**; đã kiểm chứng bằng **đọc code + lint**"*. Bug tồn tại ~8 tháng (2025-12-15 → 2026-08-19).

Toàn bộ 15 TC bám **một** root cause do AI suy ra. Cần ≥2 plausible root cause — xem danh sách ở §3.5. Tối thiểu bổ sung TC cho nhánh **`/full-emoji-list.json` lỗi/chậm** (`TC-UI003-01` §5), vì đây là nguồn dữ liệu của bảng emoji **và** của ô tìm kiếm đang lỗi ở #40131.

**[MAJOR] M-6 — NEW-24 thiếu metadata bắt buộc, 2 người chạy sẽ ra 2 kết quả khác nhau**

`NEW-24` không có `viewpoint`, `case_type`, `precondition`, `data_input`, `requirement_keys`, `spec_ids`, `tc_group`. Steps mở đầu bằng *"Bấm nút thêm action 「テキスト」"* — **không nói đang ở màn nào**, không nói modal đã mở chưa. Vi phạm review-checklist §B.1 (precondition đầy đủ) và §B.3 (chạy độc lập). Chính TC này đang gánh việc verify bug #40131.

— **Đề xuất**: `testcase_update` trên Studio, bổ sung đủ 6 field; hoặc thay bằng `TC-UIINPUT001-01…03` ở §5.

**[MAJOR] M-7 — 5/15 TC (33%) mang mã quan điểm không thuộc `checklist-lme.md` → không tính là cover**

| Mã Studio | Số TC | Mã tầng 1 đề xuất map lại |
|---|---|---|
| `TOOL-KNOW-002` (NEW-1 — TC tái hiện lỗi gốc) | 1 | `FUNC-001` (Cao) |
| `TOOL-NEGCTRL-001` (NEW-2) | 1 | `DATA-001` (Cao) hoặc `REG-SHARED-001` |
| `STATE-MATRIX-001` (NEW-5, NEW-15) | 2 | `FUNC-SEQ-001` (Trung bình) + `UI-001`/`UIC-05` |
| *(trống)* (NEW-24) | 1 | `UI-INPUT-001` (Trung bình) |

Nhóm `TOOL-*` là mã nội bộ Studio. Hệ quả: TC **tái hiện lỗi gốc** (NEW-1) hiện **không map được** vào quan điểm tầng 1 nào → bảng coverage quan điểm ở F.1 bị thủng ở chỗ quan trọng nhất.

**[MAJOR] M-8 — 15/15 TC bỏ trống `Trạng thái đánh giá spec`**

Không TC nào ghi `Spec ghi rõ` / `Spec không ghi` / `Đã hỏi leader`. Rủi ro tự suy diễn rồi cho Đạt — đặc biệt với NEW-21 (oracle là *"version hiện tại của release/config"*, một quy ước không nằm trong spec sản phẩm) và NEW-24 (hành vi ô tìm kiếm emoji **không có trong spec SC-004** — [ui-spec.md](../../spec-features/admin/action-settings/ui/ui-spec.md) chỉ mô tả `Emoji picker | Icon smile fal fa-smile-o | Chèn emoji vào textarea`, không mô tả ô search).

**[MAJOR] M-9 — Cả `01-bug-task.md` và `03-dev-impact.md` chưa được tester tick verify**

Cả 2 file có `Auto-filled: 2026-08-24 by /new-task` nhưng checkbox **"Tester verify auto-fill chính xác"** vẫn trống. F/D/T trong file 03 chép từ báo cáo AI Auto-fixbug, chưa có người đọc lại đối chiếu Redmine → coverage matrix ở §3 đang dựa trên input **chưa được xác nhận**.

**[MAJOR] M-10 — 9 TC bị xoá khỏi Studio sau lần chạy lỗi, không giữ vết**

`temp_id` chạy tới NEW-24 nhưng chỉ còn 15 TC; mất `NEW-3, 7, 8, 10, 11, 13, 14, 16, 20`. `run:402` (round 1) có **skip 2 · error 2** — 4 TC không có kết luận, nhiều khả năng nằm trong nhóm bị xoá. `REG-SPEC-001` yêu cầu case hết hiệu lực **đánh dấu, KHÔNG xoá (giữ vết)**.

Đáng chú ý: `REQ-004` ghi rõ *"click ra ngoài **hoặc nhấn ESC** phải đóng bảng đang mở mà không chèn ký tự"* — **không TC nào còn lại test phím ESC**, có thể coverage này nằm ở một TC đã bị xoá. `UIC-05` và `UIC-14` cũng yêu cầu Esc đóng modal.

**[MAJOR] M-11 — AP-4: không có link PR/diff để verify fix shape**

Mục "Commit / Pull Request" chỉ có commit hash `e982edc05e` + branch `ai_fixbug_33117`, **không có link PR**. Dev mô tả fix là "2 điều kiện bảo vệ" và tự khẳng định *"cả 2 điều kiện đều **vô hiệu** khi trang chỉ có 1 bộ chọn emoji"* — khẳng định này quyết định toàn bộ phạm vi regression (nếu sai thì **9 tính năng** dùng SC-004 đều bị chạm), nhưng reviewer **không có cách nào verify** nếu không đọc được diff.

**[MAJOR] M-12 — NEW-12 (cross-browser) ghi Đạt nhưng note của chính TC nói local không kết luận được**

Note NEW-12: *"Local runner hiện chỉ có Chromium nên kết quả skip của automation **không được dùng để kết luận pass/fail cross-browser**"*. Precondition yêu cầu *"mở lại bằng một trình duyệt khác (Edge hoặc Firefox)"*. Kết quả: `pass`, `source=manual`, `env=local`. `UI-002` yêu cầu tối thiểu **Mac Safari + Chrome**, Windows Chrome — Safari (khách chính là chủ salon/cửa hàng nhỏ) **không có trong precondition**.

— **Đề xuất**: yêu cầu evidence ghi rõ browser + OS thật đã dùng; bổ sung Mac Safari vào precondition qua `testcase_update`.

**[MAJOR] M-13 — NEW-6 (RULE-06 output cuối chuỗi) chạy ở `env=local`, `env_tag=local-only`**

NEW-6 verify emoji nhận **thật trên LINE app**. `RULE-06` bắt buộc verify tại output cuối trên **thiết bị thật**. Kết quả `pass` ở env `local` — cần evidence là ảnh chụp **màn hình LINE app thật**, không phải khung chat admin (chính expected của TC cũng ghi *"Không kết luận pass chỉ dựa trên khung chat admin"*).

**[MAJOR] M-14 — DATA-CACHE-001: thiếu nhánh "tab mở sẵn trước deploy, không refresh"**

`DATA-CACHE-001` kiểm tra (1): *"trước deploy mở sẵn 1 tab (**không refresh**) → sau deploy thao tác tiếp trên tab đó (JS cũ đọc data format mới)"*. NEW-22 làm việc khác — F5 **sau** deploy. Nhánh "client cũ chạy tiếp không reload" (`DEPLOY-LIVE-001`) **hoàn toàn chưa có TC**, dù đây là tình huống thật của user đang mở màn chat khi release chạy.

### 4.3 Minor (có thể fix sau)

- **[MINOR] STALE-EXEC** — `04-tc-list.md` trong repo là snapshot **round 1** (14 Đạt / 1 Không đạt, `runId 440`); Studio hiện ở **round 2** (15/15 Đạt, `runId 455`). Tập TC khớp 100% nên không phải `STALE-INPUT`, nhưng cột `Kết quả thực thi` / `Ngày thực hiện` / §1–§2 cảnh báo trong file 04 **đã cũ**. Chạy lại `/new-task` hoặc cập nhật thủ công cột exec trước khi dùng file 04 làm bằng chứng.
- **[MINOR] RULE-02** — không TC nào ghi **loại evidence bắt buộc** ở `Ghi chú`; cột `Evidence thực tế` trống toàn bộ (Studio `testcase_list` không trả về). Với 15/15 Đạt mà không có evidence nào truy ra được từ file 04, RULE-02 chưa được thoả.
- **[MINOR] TC No.** — Studio dùng `temp_id` dạng `NEW-n`, không theo format repo `TC-<mã quan điểm bỏ gạch>-<nn>`. Không chặn review, nhưng khiến `/sync-ai-tc` và đối chiếu coverage khó tự động hoá.
- **[MINOR] D1 "không có data"** — mục 4.2 dev-impact ghi "Không có". Đúng theo nghĩa fix không đụng schema, nhưng emoji **được lưu xuống DB** qua `t_actions_detail` khi save bản ghi (spec SC-004 §1). NEW-18 có verify save→mở lại ở 自動応答, chưa verify ở tầng DB (`RULE-07` verify 3 tầng). Mức Minor vì fix là front-end thuần.
- **[MINOR] NEW-24 `exec_mode = auto` nhưng không có precondition** — TC được pipeline chạy tự động dù thiếu điểm khởi đầu xác định; nên đổi `exec_mode = manual` cho tới khi bổ sung đủ metadata (M-6).

### 4.4 Nit (gợi ý)

- **[NIT]** `UI-INPUT-001` yêu cầu kiểm **paste bằng chuột phải** trên Windows và Mac. Fix không chạm luồng paste nên **không đề xuất TC bắt buộc** (tránh over-coverage ngoài bán kính fix — xem AP-5), nhưng nếu bổ sung TC cho ô tìm kiếm emoji (§5 `TC-UIINPUT001-03`) thì gộp luôn 1 bước paste chuột phải là hợp lý.
- **[NIT]** NEW-1 và NEW-23 trùng một phần mục đích (đều verify bảng emoji của modal mở được và không bị picker kia xoá). Có thể giữ cả hai vì NEW-23 thêm chiều transition, nhưng nên ghi rõ quan hệ ở `Ghi chú` để người chạy không bỏ qua NEW-23 vì tưởng trùng.
- **[NIT]** Đặt lại tên `NEW-24` cho cụ thể hơn — "Check search emoji từ bảng emoji" là dạng "check X", theo review-checklist §B.1 nên mô tả được mục đích + oracle.

---

## 5. TCs đề xuất bổ sung

> 16 cột canonical, member copy thẳng sang Studio (`testcase_create`) hoặc `04-tc-list.md` round sau. `Kết quả thực thi` = `Chưa test`, `Evidence thực tế` để trống, loại evidence bắt buộc ghi ở `Ghi chú` (RULE-02).

| TC No. | Mã quan điểm liên kết | Loại case | Tiêu đề test case | Điều kiện tiền đề | Các bước thực hiện | Dữ liệu test/input | Kết quả mong đợi | Kết quả thực thi | Evidence thực tế | Môi trường test | Người thực hiện | Ngày thực hiện | Số ticket bug | Trạng thái đánh giá spec | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-FUNCMULTI001-01 | FUNC-MULTI-001 | Normal | Modal có 3 action 「テキスト」: emoji chèn đúng vào action đang thao tác, 2 action còn lại không đổi | - Đã đăng nhập admin, chọn bot test<br>- Mở màn chat 1:1 của 1 bạn bè<br>- Modal 「アクション」 đã mở | 1. Thêm 3 action 「テキスト」 liên tiếp<br>2. Nhập lần lượt 'AAA' / 'BBB' / 'CCC' vào action 1 / 2 / 3<br>3. Đặt con trỏ cuối chuỗi 'BBB' của action 2<br>4. Bấm icon mặt cười **của action 2**<br>5. Chọn emoji 😀<br>6. Đọc nội dung và bộ đếm ký tự của cả 3 action | Action 1 = 'AAA' · Action 2 = 'BBB' · Action 3 = 'CCC' · Emoji: 😀 vào action 2 | Action 2 = 'BBB😀', counter action 2 tăng đúng số ký tự emoji. Action 1 vẫn đúng 'AAA' và action 3 vẫn đúng 'CCC', counter 2 action này **không đổi**. Emoji xuất hiện **đúng 1 lần**, không rơi sang action khác hay sang ô nhập tin chat | Chưa test | | STAGING | | | | | Lấp **GAP B-4** — cover REQ-002 mệnh đề "đúng dòng action". Evidence bắt buộc: screenshot toàn modal thấy đủ 3 ô nội dung + 3 counter |
| TC-FUNCMULTI001-02 | FUNC-MULTI-001 | Abnormal | Mở bảng emoji của action 1 rồi bấm thẳng icon emoji của action 3 — chỉ 1 bảng tồn tại, chèn đúng action 3 | - Như TC-FUNCMULTI001-01<br>- Đã thêm 3 action 「テキスト」, cả 3 để trống nội dung | 1. Bấm icon mặt cười của **action 1** để mở bảng emoji<br>2. Không chọn emoji, bấm thẳng icon mặt cười của **action 3**<br>3. Đếm số bảng emoji đang hiển thị trên màn hình<br>4. Chọn emoji 🎉<br>5. Đọc nội dung cả 3 action | 3 action text rỗng · Emoji: 🎉 | Trên màn hình **luôn chỉ có 1 bảng emoji** — bảng của action 1 bị đóng khi bảng của action 3 mở. Emoji 🎉 chỉ vào action 3; action 1 và action 2 vẫn rỗng | Chưa test | | STAGING | | | | | Lấp **GAP B-4**. Đây là biến thể trong-modal của root cause (2 bảng cùng instance picker). Evidence: video thao tác + screenshot sau khi chọn |
| TC-FUNCMULTI001-03 | FUNC-MULTI-001 | Boundary | Xoá action ở giữa rồi chèn emoji vào action còn lại — không chèn nhầm theo index cũ | - Như TC-FUNCMULTI001-01<br>- Đã thêm 3 action 「テキスト」 nội dung 'A1' / 'A2' / 'A3' | 1. Xoá **action 2** ('A2') khỏi modal<br>2. Không reload trang<br>3. Đặt con trỏ cuối chuỗi 'A3' của action còn lại phía dưới<br>4. Bấm icon mặt cười của action đó và chọn 😀<br>5. Đọc nội dung 2 action còn lại<br>6. Xác nhận modal, mở lại modal và đọc lại | 'A1' / 'A2' (xoá) / 'A3' · Emoji: 😀 | Sau khi xoá, emoji chèn vào **đúng action 'A3'** → 'A3😀'; action 'A1' không đổi. Sau khi lưu và mở lại modal, nội dung vẫn là 'A1' và 'A3😀' — không lệch index, không mất emoji | Chưa test | | STAGING | | | | | Lấp **GAP B-4** + **M-4** (loại Boundary). Liên kết `FUNC-SEQ-001` (thao tác liên tiếp không reload). Evidence: screenshot trước/sau xoá + sau khi mở lại modal |
| TC-REGSHARED001-04 | REG-SHARED-001 | Normal | Kịch bản (FA-009): emoji trong action 「テキスト」 của 1 step lưu và mở lại nguyên vẹn | - Đã đăng nhập admin, chọn bot test<br>- Màn 「シナリオ」 tạo mới được kịch bản<br>- Dùng tên kịch bản riêng có hậu tố nhận diện lượt test | 1. Tạo kịch bản mới tên 'TC33117-SC-001'<br>2. Thêm 1 step, mở modal 「アクション」<br>3. Thêm action 「テキスト」, nhập 'Buoc 1'<br>4. Bấm icon mặt cười, chọn 😀<br>5. Xác nhận modal, lưu kịch bản<br>6. Mở lại kịch bản theo tên vừa tạo và mở lại modal 「アクション」 | Tên kịch bản: 'TC33117-SC-001' · Nội dung action: 'Buoc 1😀' | Bảng emoji mở được và **giữ hiển thị**; emoji chèn đúng ô nội dung action. Lưu thành công. Mở lại thấy đúng 'Buoc 1😀' — emoji không mất, không thành `?` hay ô vuông | Chưa test | | STAGING | | | | | Lấp **GAP T2 / B-3** — FA-009 hiện 0 TC. Evidence: screenshot modal sau khi chèn + screenshot sau khi mở lại |
| TC-REGSHARED001-05 | REG-SHARED-001 | Normal | Rich Menu (FA-010): emoji trong action 「テキスト」 gán cho 1 nút vẫn chèn đúng | - Đã đăng nhập admin, chọn bot test<br>- Màn 「リッチメニュー」 tạo/sửa được rich menu có ít nhất 1 vùng nút | 1. Mở rich menu test, chọn 1 vùng nút<br>2. Mở modal 「アクション」 của nút đó<br>3. Thêm action 「テキスト」, nhập 'Menu'<br>4. Bấm icon mặt cười, chọn 🎉<br>5. Xác nhận modal, lưu rich menu<br>6. Mở lại nút đó và đọc nội dung action | Nội dung action: 'Menu🎉' | Bảng emoji mở được, không tự đóng trong cùng cú bấm; emoji chèn đúng vào ô nội dung action của nút. Sau lưu và mở lại, nội dung vẫn đúng 'Menu🎉' | Chưa test | | STAGING | | | | | Lấp **GAP T2 / B-3** — FA-010 hiện 0 TC. Evidence: screenshot modal + screenshot sau khi mở lại nút |
| TC-REGSHARED001-06 | REG-SHARED-001 | Abnormal | Form Answer (FA-013): mở bảng emoji rồi đóng modal bằng nút X — bảng không treo lại trên nền trang | - Đã đăng nhập admin, chọn bot test<br>- Màn 「フォーム」 có 1 form mở được cấu hình action khi submit | 1. Mở form test, vào cấu hình action khi submit<br>2. Thêm action 「テキスト」, nhập 'Cam on'<br>3. Bấm icon mặt cười để mở bảng emoji<br>4. **Không chọn emoji**, bấm nút X đóng modal<br>5. Quan sát nền trang trong 3 giây<br>6. Mở lại modal 「アクション」 và bấm lại icon mặt cười | Nội dung action: 'Cam on' | Bảng emoji **biến mất cùng modal**, không còn phần tử bảng emoji treo trên nền trang. Mở lại modal thì bảng emoji vẫn mở lại được bình thường (không bị "kẹt") và nội dung action vẫn là 'Cam on' | Chưa test | | STAGING | | | | | Lấp **GAP T2 / B-3** — FA-013 hiện 0 TC; đối xứng với NEW-5 nhưng ở màn chỉ có 1 picker. Evidence: video thao tác đóng modal + screenshot DOM sau khi đóng |
| TC-COMPATLEGACY001-01 | COMPAT-LEGACY-001 | Normal | Variant V1 legacy 「友だち一括操作」 mở từ Danh sách bạn bè: emoji của action text hoạt động như trước | - Đã đăng nhập admin, chọn bot test<br>- Màn 「友だちリスト」 có ≥1 bạn bè<br>- Đã deploy bản fix, đã F5 thường | 1. Mở màn danh sách bạn bè, chọn ≥1 bạn bè<br>2. Mở modal thao tác hàng loạt 「友だち一括操作」 (variant V1)<br>3. Vào tab có action gửi text, nhập 'V1 test'<br>4. Bấm icon emoji nếu variant này có<br>5. Chọn 1 emoji và đọc nội dung ô | Nội dung: 'V1 test😀' | Nếu V1 có icon emoji: bảng mở được và chèn đúng vào ô của V1. Nếu V1 **không có** icon emoji: ghi nhận rõ trong kết quả để Dev xác nhận phạm vi. Trong cả 2 trường hợp, thao tác hàng loạt của V1 **không bị lỗi JS** (Console không có exception) | Chưa test | | STAGING | | | | Spec không ghi | Lấp **GAP B-3** — V1 `modal_setting_action.blade.php` dùng jQuery thuần, **Dev không nhắc tới**. Evidence: screenshot modal V1 + ảnh chụp Console tab |
| TC-COMPATLEGACY001-02 | COMPAT-LEGACY-001 | Normal | Variant V3 「アクション編集」 (Pro Edit): sửa action text đã lưu, emoji chèn đúng ô đang sửa | - Đã đăng nhập admin, chọn bot test<br>- Đã có sẵn 1 bản ghi có action 「テキスト」 nội dung 'Goc'<br>- Đã deploy bản fix, đã F5 thường | 1. Mở bản ghi đã có action, chọn chức năng sửa action → modal 「アクション編集」 (variant V3)<br>2. Trong khối 「設定されたアクション」, chọn action text 'Goc'<br>3. Đặt con trỏ cuối chuỗi<br>4. Bấm icon mặt cười, chọn 😀<br>5. Lưu và mở lại bản ghi | Nội dung gốc: 'Goc' → sau sửa: 'Goc😀' | Bảng emoji của V3 mở được và giữ hiển thị; emoji chèn đúng vào ô đang sửa, không chèn sang ô khác trong khối 「設定されたアクション」. Lưu và mở lại thấy 'Goc😀' | Chưa test | | STAGING | | | | Spec không ghi | Lấp **GAP B-3** — V3 `modal_select_action_pro.blade.php`, **Dev không nhắc tới**. Evidence: screenshot V3 trước/sau chèn + sau khi mở lại |
| TC-COMPATLEGACY001-03 | COMPAT-LEGACY-001 | Abnormal | Variant V3 mở từ màn có sẵn ô nhập tin chat — kiểm tra có phát sinh cấu hình 2 picker như bug gốc không | - Đã đăng nhập admin, chọn bot test<br>- Mở màn chat 1:1 của 1 bạn bè (màn có ô nhập tin chat)<br>- Bạn bè đó đã có action được cấu hình từ trước | 1. Từ màn chat 1:1, mở chức năng sửa action đã cấu hình → modal V3 「アクション編集」<br>2. Bấm icon mặt cười của action text trong V3<br>3. Quan sát bảng emoji trong 2-3 giây<br>4. Chọn 1 emoji<br>5. Đóng modal, đọc lại ô nhập tin nhắn chat | Ô chat trước khi mở modal: 'chat-goc' · Emoji: 😀 | Bảng emoji của V3 **không bị đóng ngay trong cùng cú bấm** (đúng như V2 sau fix). Emoji chỉ vào ô nội dung action; ô nhập tin nhắn chat vẫn đúng 'chat-goc' | Chưa test | | STAGING | | | | Spec không ghi | Lấp **GAP B-3** — kịch bản 2 picker ở variant chưa được rà. Nếu V3 không mở được từ chat 1:1 thì ghi lý do và chuyển × |
| TC-DEPLOYASSET001-02 | DEPLOY-ASSET-001 | Normal | Sau F5 thường với version chung mới, luồng critical vẫn chạy đúng và không có asset 404 | - Trình duyệt đã mở hệ thống **TRƯỚC** khi deploy (đã cache js/css version cũ)<br>- Đã deploy bản fix lên môi trường test<br>- Mở sẵn tab Network, **KHÔNG** tick tắt cache | 1. Trên đúng trình duyệt đó, mở lại trang admin và nhấn **F5 thường** (không Ctrl+F5)<br>2. Chạy luồng **gửi tin** cơ bản tới 1 bạn bè<br>3. Mở màn gói cước / thanh toán và thao tác tới bước xác nhận (không hoàn tất)<br>4. Mở màn hủy hợp đồng tới bước xác nhận (không hoàn tất)<br>5. Lọc tab Network theo js / css / font, đọc status code và query version | Không nhập dữ liệu nghiệp vụ; chỉ đi qua các bước và quan sát Network | Tất cả js / css / font trả **HTTP 200** với **query version mới**, **không có request nào 404**. Cả 3 luồng critical thao tác được bình thường, không lỗi JS trên Console | Chưa test | | **PRODUCTION** | | | | | Lấp **GAP B-2** — mục (3)(4) của DEPLOY-ASSET-001. RULE-08: asset phải kết luận trên production. Evidence: screenshot tab Network (đầy đủ version + status) + screenshot từng luồng critical |
| TC-DEPLOYASSET001-03 | DEPLOY-ASSET-001 | Abnormal | Rà toàn bộ thẻ nạp asset trong layout — không còn thẻ nào giữ version cố định cũ | - Đã deploy bản fix<br>- Mở tab Network, tick **Disable cache = OFF** | 1. Mở lần lượt 5 màn đại diện: chat 1:1, tự động trả lời, kịch bản, gói cước, danh sách bạn bè<br>2. Ở mỗi màn, lọc Network theo js và css<br>3. Đối chiếu **query version** của từng request với version chung hiện tại của release<br>4. Ghi lại mọi request có version **khác** version chung | Không nhập dữ liệu; đối chiếu query string | **Không request js/css nào** dùng version khác version chung của release hiện tại. Nếu phát hiện thẻ còn hard-code version cũ → raise ticket riêng cho Dev | Chưa test | | **PRODUCTION** | | | | | Lấp **GAP B-2** — chính loại lỗi Dev vừa sửa cho `fgEmojiPicker.js`, chưa ai rà các thẻ còn lại. Evidence: bảng liệt kê request + version của cả 5 màn |
| TC-DEPLOYASSET001-04 | DEPLOY-ASSET-001 | Boundary | Icon-font và glyph sau khi nâng version chung: load lại nhiều lần không mất icon, không tofu | - Đã deploy bản fix trên production<br>- Chuẩn bị 1 bản ghi có nội dung chứa kanji, kana và dấu tiếng Việt | 1. Mở màn chat 1:1 và màn tự động trả lời<br>2. Nhấn F5 thường **5 lần liên tiếp**, mỗi lần chờ trang load xong<br>3. Sau mỗi lần, kiểm tra icon mặt cười và các icon thanh công cụ có hiển thị đủ không<br>4. Mở bản ghi có kanji + kana + dấu tiếng Việt, đọc kỹ từng ký tự<br>5. Lọc Network theo font, kiểm status code | Nội dung kiểm tra: chuỗi có kanji 「配信」, kana 「アクション」, dấu tiếng Việt 'Điều kiện lọc' | Qua cả 5 lần load, icon hiển thị **đầy đủ và ổn định**, không có lần nào mất icon. Font trả 200, **không 404**, không fallback về font hệ thống. Không ký tự nào hiện ô vuông (tofu) | Chưa test | | **PRODUCTION** | | | | | Lấp **GAP B-2** + **M-4** (loại Boundary). Theo `UIC-15` + DEPLOY-ASSET-001 mục (5)(6). Evidence: 5 screenshot sau mỗi lần load + screenshot Network tab font |
| TC-ENV003-01 | ENV-003 | Normal | Chạy lại nhóm asset/cache trên PRODUCTION — không kết luận từ local | - Bản fix đã release lên production<br>- Có tài khoản test trên production<br>- Trình duyệt đã từng mở production **trước** release | 1. Trên production, lặp lại đúng các bước của NEW-21 (F5 thường, kiểm request `/js/fgEmojiPicker.js`)<br>2. Lặp lại đúng các bước của NEW-22 (trình duyệt còn cache bản cũ, F5 thường, mở modal và bấm icon emoji)<br>3. Kiểm tra đường dẫn asset có redirect sang `p.lmes.jp` như quy ước production không<br>4. Ghi lại router id nếu hệ thống trả về, lặp bước 1-2 cho router còn lại | Không nhập dữ liệu; quan sát request và hành vi bảng emoji | Trên production, request asset trả 200 với version mới; bảng emoji mở được và giữ hiển thị mà **không cần hard-reload**. Kết quả **giống nhau trên cả 2 router** (production loadbalance 2 server) | Chưa test | | **PRODUCTION** | | | | | Lấp **M-1** — RULE-08 / Catalog D (media qua `p.lmes.jp`, loadbalance 2 server). Evidence: screenshot Network trên production cho từng router |
| TC-DATACACHE001-02 | DATA-CACHE-001 | Abnormal | Tab mở sẵn TRƯỚC deploy, không refresh — thao tác tiếp không lỗi và không báo thành công giả | - Mở màn chat 1:1 và modal 「アクション」 với 1 action text **TRƯỚC** khi release<br>- **Không đóng, không refresh** tab đó trong suốt quá trình release | 1. Thực hiện release bản fix trong khi tab vẫn đang mở<br>2. **Không reload**, quay lại tab cũ<br>3. Bấm icon mặt cười của action text và quan sát<br>4. Chọn 1 emoji, xác nhận modal và lưu bản ghi<br>5. Mở tab mới, F5, mở lại bản ghi vừa lưu và đối chiếu nội dung | Nội dung action trước release: 'Truoc deploy' · Emoji: 😀 | Thao tác trên tab cũ hoặc **chạy đúng như trước**, hoặc **báo lỗi rõ ràng** — tuyệt đối **không lưu nửa vời** và **không báo thành công giả**. Nếu lưu thành công thì bản ghi mở ở tab mới phải đúng 'Truoc deploy😀' | Chưa test | | **PRODUCTION** | | | | | Lấp **M-14** — DATA-CACHE-001 mục (1) + `DEPLOY-LIVE-001` (client cũ gọi server mới). Evidence: screenshot tab cũ trước/sau release + bản ghi đọc lại ở tab mới |
| TC-UI001-01 | UI-001 | Abnormal | Nhấn ESC khi bảng emoji đang mở — đóng bảng, modal vẫn mở, nội dung action không mất | - Đang ở màn chat 1:1 của 1 bạn bè<br>- Modal 「アクション」 đã mở, đã thêm 1 action 「テキスト」 nội dung 'ABC' | 1. Bấm icon mặt cười của action để mở bảng emoji<br>2. Nhấn phím **ESC** một lần<br>3. Quan sát bảng emoji, modal và nội dung ô action<br>4. Bấm lại icon mặt cười để xác nhận bảng còn mở lại được | Nội dung action: 'ABC' | Bảng emoji đóng lại; **modal 「アクション」 vẫn mở**; nội dung action vẫn đúng 'ABC', **không bị chèn thêm ký tự nào**. Bấm lại icon thì bảng mở lại bình thường | Chưa test | | STAGING | | | | | Lấp **M-10** — REQ-004 nêu rõ ESC nhưng 0 TC cover (nhiều khả năng nằm ở TC đã bị xoá). Theo `UIC-05` + `UIC-14`. Evidence: video thao tác ESC |
| TC-UI001-02 | UI-001 | Abnormal | Nhấn ESC lần thứ hai — đóng modal, hành vi với nội dung soạn dở phải nhất quán | - Tiếp nối TC-UI001-01: bảng emoji đã đóng bằng ESC, modal vẫn mở, action có nội dung 'ABC' | 1. Nhấn **ESC** lần thứ hai<br>2. Quan sát modal 「アクション」<br>3. Mở lại modal 「アクション」<br>4. Kiểm tra action text còn nội dung soạn dở hay đã bị xoá<br>5. Lặp lại toàn bộ ở màn tự động trả lời để so sánh | Nội dung action soạn dở: 'ABC' | Modal đóng lại. Hành vi với nội dung soạn dở phải **nhất quán và khớp spec** — hoặc giữ nguyên, hoặc xoá kèm hỏi xác nhận; **không được xoá âm thầm**. Hành vi ở chat 1:1 và ở tự động trả lời phải **giống nhau** | Chưa test | | STAGING | | | | Spec không ghi | Lấp **M-10** — `UIC-05` "Dữ liệu đang nhập dở khi đóng modal: giữ hay xóa, phải nhất quán"; liên kết `FUNC-DRAFT-001`. **Cần hỏi Leader/PM** hành vi mong đợi trước khi chấm Đạt |
| TC-UIINPUT001-01 | UI-INPUT-001 | Normal | Ô 「Search emoji」 lọc đúng theo từ khoá và khôi phục danh sách đầy đủ khi xoá trắng | - Đã đăng nhập admin, chọn bot test<br>- Mở màn chat 1:1 của 1 bạn bè<br>- Modal 「アクション」 đã mở, đã thêm 1 action 「テキスト」 nội dung rỗng<br>- Đã F5 thường sau khi deploy bản fix | 1. Bấm icon mặt cười để mở bảng emoji<br>2. Bấm vào ô 「Search emoji」<br>3. Gõ từ khoá 'smile', quan sát bảng ngay sau **ký tự đầu tiên**<br>4. Xoá trắng ô tìm kiếm<br>5. Gõ 'heart', chọn 1 emoji trong kết quả<br>6. Đọc nội dung ô action | Từ khoá: 'smile' rồi 'heart' · Chọn 1 emoji kết quả 'heart' | Ngay từ ký tự đầu tiên, **bảng emoji vẫn hiển thị** (không biến mất) và danh sách thu hẹp còn emoji khớp từ khoá. Xoá trắng → danh sách đầy đủ hiện lại. Chọn emoji từ kết quả 'heart' → emoji được chèn vào ô nội dung action | Chưa test | | STAGING | | | | Spec không ghi | Thay thế **NEW-24** (M-6) và verify **Redmine #40131**. Spec SC-004 không mô tả ô search → cần Leader xác nhận oracle. Evidence: video gõ từng ký tự + screenshot danh sách đã lọc |
| TC-UIINPUT001-02 | UI-INPUT-001 | Abnormal | Gõ từ khoá không khớp emoji nào — hiện trạng thái rỗng rõ ràng, bảng không biến mất | - Như TC-UIINPUT001-01, bảng emoji đang mở | 1. Bấm vào ô 「Search emoji」<br>2. Gõ chuỗi chắc chắn không khớp: 'zzzzzzzz'<br>3. Quan sát bảng emoji<br>4. Xoá bớt về 'z'<br>5. Xoá trắng hoàn toàn | Từ khoá: 'zzzzzzzz' → 'z' → rỗng | Bảng emoji **vẫn hiển thị**, vùng danh sách hiện thông báo rỗng hoặc danh sách trống rõ ràng — **không màn trắng, không bảng tự đóng**. Khi xoá bớt ký tự thì kết quả cập nhật lại, xoá trắng thì danh sách đầy đủ trở lại | Chưa test | | STAGING | | | | Spec không ghi | Lấp **M-6** + liên kết `UI-003` (trạng thái rỗng). Evidence: screenshot trạng thái rỗng của bảng emoji |
| TC-UIINPUT001-03 | UI-INPUT-001 | Boundary | Ô 「Search emoji」 với 1 ký tự, khoảng trắng và paste bằng chuột phải | - Như TC-UIINPUT001-01, bảng emoji đang mở<br>- Đã copy sẵn chuỗi 'heart' vào clipboard | 1. Gõ đúng **1 ký tự** 's' vào ô tìm kiếm, quan sát<br>2. Xoá, gõ **1 khoảng trắng**, quan sát<br>3. Xoá, **click chuột phải > Paste** chuỗi 'heart' từ clipboard<br>4. Quan sát danh sách kết quả<br>5. Chọn 1 emoji trong kết quả và đọc ô action | 's' · 1 khoảng trắng · paste 'heart' bằng chuột phải | Với 1 ký tự: bảng vẫn hiển thị, danh sách lọc theo 's'. Với khoảng trắng: bảng không biến mất, hành vi ổn định (không lỗi JS). Paste **bằng chuột phải** phải kích hoạt lọc **giống hệt gõ bằng bàn phím** — chọn emoji xong chèn đúng vào ô action | Chưa test | | STAGING | | | | Spec không ghi | Lấp **M-4** (Boundary) + **M-6**; gộp gợi ý ở §4.4 (paste chuột phải theo `UIC-04`). Evidence: screenshot sau mỗi input + trạng thái danh sách |
| TC-FUNC004-01 | FUNC-004 | Boundary | Chèn emoji khi nội dung action đã sát giới hạn 5.000 ký tự — bộ đếm đúng, không tràn | - Đang ở màn chat 1:1, modal 「アクション」 đã mở<br>- Đã thêm 1 action 「テキスト」<br>- Chuẩn bị sẵn chuỗi **4.999 ký tự** latinh để paste | 1. Paste chuỗi 4.999 ký tự vào ô nội dung action<br>2. Đọc bộ đếm, xác nhận hiển thị 4,999/5,000<br>3. Đặt con trỏ ở cuối chuỗi<br>4. Bấm icon mặt cười và chọn 😀<br>5. Đọc lại bộ đếm và nội dung ô<br>6. Xác nhận modal, lưu, mở lại và đối chiếu | Chuỗi 4.999 ký tự latinh · Emoji: 😀 | Bộ đếm sau khi chèn emoji phản ánh **đúng quy tắc đếm của hệ thống** và **không vượt 5.000** một cách âm thầm. Nếu emoji làm vượt giới hạn thì hệ thống **chặn rõ ràng** (không chèn hoặc báo lỗi), tuyệt đối không lưu nội dung dài hơn 5.000. Sau khi lưu và mở lại, nội dung khớp đúng cái đã lưu | Chưa test | | STAGING | | | | Spec ghi rõ | Lấp **M-4**. Nguồn limit: spec SC-004 §3.4.3 — textarea max 5.000, counter `count_text_content{indexAction}/5,000`. Evidence: screenshot bộ đếm trước/sau chèn + nội dung sau khi mở lại |
| TC-FUNC004-02 | FUNC-004 | Boundary | Nội dung action **đúng 5.000 ký tự** — bấm emoji không được làm vỡ giới hạn hoặc mất nội dung | - Như TC-FUNC004-01<br>- Chuẩn bị sẵn chuỗi **đúng 5.000 ký tự** | 1. Paste chuỗi 5.000 ký tự vào ô nội dung action<br>2. Xác nhận bộ đếm hiển thị 5,000/5,000<br>3. Bấm icon mặt cười và chọn 😀<br>4. Đọc bộ đếm và nội dung ô<br>5. Thử xác nhận modal và lưu | Chuỗi đúng 5.000 ký tự · Emoji: 😀 | Hệ thống **không cho chèn thêm** hoặc báo lỗi rõ ràng. Nội dung **không bị cắt mất phần đầu/cuối**, không lưu chuỗi > 5.000. Nếu chặn, thông báo phải dễ hiểu với người vận hành | Chưa test | | STAGING | | | | Spec ghi rõ | Lấp **M-4** — pattern "đúng biên" của FUNC-004. Evidence: screenshot bộ đếm + thông báo chặn |
| TC-UI003-01 | UI-003 | Abnormal | Nguồn dữ liệu emoji lỗi hoặc chậm — bảng emoji báo trạng thái rõ ràng, không im lặng | - Đang ở màn chat 1:1, modal 「アクション」 đã mở, đã thêm 1 action 「テキスト」<br>- Mở DevTools, dùng Network throttling **Slow 3G**; chuẩn bị thêm 1 lượt chặn request tới `/full-emoji-list.json` | 1. Bật Slow 3G, bấm icon mặt cười, quan sát trong lúc dữ liệu emoji đang tải<br>2. Ghi nhận có chỉ báo đang tải hay màn trống<br>3. Tắt throttling, chặn hẳn request `/full-emoji-list.json` (block request URL)<br>4. F5 thường, bấm lại icon mặt cười<br>5. Quan sát bảng emoji và Console | Không nhập dữ liệu; điều khiển mạng qua DevTools | Khi tải chậm: có chỉ báo đang tải hoặc bảng hiện khung, **không màn trắng**, không "bấm mà không có gì hiện ra". Khi nguồn dữ liệu lỗi: hiển thị trạng thái lỗi rõ ràng cho người dùng, **không im lặng như không bấm** — vì đây chính là triệu chứng của bug gốc | Chưa test | | STAGING | | | | Spec không ghi | Lấp **M-5** (AP-2) — alternative root cause. Nguồn: `EP-08 GET /full-emoji-list.json` trong [chat-11/ui/ui-spec.md](../../spec-features/admin/chat-11/ui/ui-spec.md). Evidence: video Slow 3G + screenshot khi block request |

### Đã push lên MCP LME TEST STUDIO — 2026-08-25

Toàn bộ 22 TC trên đã được tạo trên **Studio task #174** bằng `testcase_create` (actor `@mcp`, `status=draft`, `Kết quả thực thi` = chưa chạy). Task hiện có **37 TC** (15 cũ + 22 mới): `pass 15 · fail 0 · untested 22`.

| TC No. (report) | Studio `temp_id` | Studio `id` | `client_ref` |
|---|---|---|---|
| TC-FUNCMULTI001-01 | NEW-25 | 12642 | `qa33117-rv-funcmulti001-01` |
| TC-FUNCMULTI001-02 | NEW-26 | 12643 | `qa33117-rv-funcmulti001-02` |
| TC-FUNCMULTI001-03 | NEW-27 | 12644 | `qa33117-rv-funcmulti001-03` |
| TC-REGSHARED001-04 | NEW-28 | 12645 | `qa33117-rv-regshared001-04` |
| TC-REGSHARED001-05 | NEW-29 | 12646 | `qa33117-rv-regshared001-05` |
| TC-REGSHARED001-06 | NEW-30 | 12647 | `qa33117-rv-regshared001-06` |
| TC-COMPATLEGACY001-01 | NEW-31 | 12648 | `qa33117-rv-compatlegacy001-01` |
| TC-COMPATLEGACY001-02 | NEW-32 | 12649 | `qa33117-rv-compatlegacy001-02` |
| TC-COMPATLEGACY001-03 | NEW-33 | 12650 | `qa33117-rv-compatlegacy001-03` |
| TC-DEPLOYASSET001-02 | NEW-34 | 12651 | `qa33117-rv-deployasset001-02` |
| TC-DEPLOYASSET001-03 | NEW-35 | 12652 | `qa33117-rv-deployasset001-03` |
| TC-DEPLOYASSET001-04 | NEW-36 | 12653 | `qa33117-rv-deployasset001-04` |
| TC-ENV003-01 | NEW-37 | 12654 | `qa33117-rv-env003-01` |
| TC-DATACACHE001-02 | NEW-38 | 12655 | `qa33117-rv-datacache001-02` |
| TC-UI001-01 | NEW-39 | 12656 | `qa33117-rv-ui001-01` |
| TC-UI001-02 | NEW-40 | 12657 | `qa33117-rv-ui001-02` |
| TC-UIINPUT001-01 | NEW-41 | 12658 | `qa33117-rv-uiinput001-01` |
| TC-UIINPUT001-02 | NEW-42 | 12659 | `qa33117-rv-uiinput001-02` |
| TC-UIINPUT001-03 | NEW-43 | 12660 | `qa33117-rv-uiinput001-03` |
| TC-FUNC004-01 | NEW-44 | 12661 | `qa33117-rv-func004-01` |
| TC-FUNC004-02 | NEW-45 | 12662 | `qa33117-rv-func004-02` |
| TC-UI003-01 | NEW-46 | 12663 | `qa33117-rv-ui003-01` |

**Lưu ý khi chạy 22 TC này:**

- **5 TC bắt buộc chạy PRODUCTION** (`env_scope = ["prd"]`): NEW-34, NEW-35, NEW-36, NEW-37, NEW-38 — theo RULE-08, nhóm asset/cache/deploy không kết luận được từ local/staging.
- ⚠️ **NEW-34** đi qua màn thanh toán và hủy hợp đồng trên production: dùng **tài khoản test**, **DỪNG trước bước xác nhận cuối**, tuyệt đối không hoàn tất giao dịch thật.
- **NEW-40** (`TC-UI001-02`) cần **Leader/PM chốt hành vi mong đợi** với nội dung soạn dở khi đóng modal bằng ESC trước khi chấm Đạt — spec SC-004 chưa định nghĩa.
- **NEW-41** (`TC-UIINPUT001-01`) thay thế `NEW-24` và verify **Redmine #40131**; sau khi NEW-41 chạy đạt thì đề nghị `testcase_delete` hoặc đánh dấu NEW-24 hết hiệu lực.
- `client_ref` là **idempotent key** — chạy lại `testcase_create` với cùng `client_ref` sẽ trả `reused: true` thay vì tạo trùng.

---

## 6. Spec update needed

- [ ] Không cần update spec
- [x] **Cần update spec** — chi tiết:

**(1) Hành vi ô 「Search emoji」 chưa có trong spec**
- Section: [spec-features/admin/action-settings/ui/ui-spec.md](../../spec-features/admin/action-settings/ui/ui-spec.md) §3.4.3 テキスト — hiện chỉ ghi `Emoji picker | Icon smile fal fa-smile-o | Chèn emoji vào textarea`.
- Nội dung cần update: mô tả bảng emoji (nguồn dữ liệu `/full-emoji-list.json`, ô tìm kiếm, quy tắc lọc, trạng thái rỗng, cách đóng bằng click ra ngoài / ESC / mở picker khác).
- Lý do: bug **#40131** và `NEW-24` đều nằm ở hành vi này nhưng **không có oracle trong spec** → tester đang tự suy diễn. Đây là nguyên nhân M-8.
- Người chịu trách nhiệm: `<PM/BA điền>`

**(2) Quy tắc chỉ được có tối đa 1 bảng emoji trên trang**
- Section: [spec-features/admin/action-settings/shared-spec.md](../../spec-features/admin/action-settings/shared-spec.md) (SC-004) — bổ sung mục về emoji picker dùng chung.
- Nội dung cần update: ghi rõ ràng buộc "tại mọi thời điểm chỉ có tối đa 1 bảng emoji hiển thị", quy tắc chủ sở hữu bảng khi trang có **nhiều picker** hoặc modal có **nhiều action text**, và hành vi khi mở picker thứ hai.
- Lý do: đây là **hợp đồng hành vi** mà bản fix vừa thiết lập (REQ-004), nhưng chỉ tồn tại trong code + requirement Studio, không có trong spec sản phẩm → release sau rất dễ phá vỡ mà không ai phát hiện. Liên quan **RULE-10** (bug lọt production phải sinh dòng quan điểm/spec mới).
- Người chịu trách nhiệm: `<PM/BA điền>`

**(3) Danh sách nơi khởi tạo `FgEmojiPicker`**
- Section: SC-004 shared-spec — mục "Các tính năng sử dụng SC-004" + mục "Variants".
- Nội dung cần update: ghi rõ variant nào (V1/V2/V3) có emoji picker, khởi tạo ở file nào.
- Lý do: nền tảng cho `REG-SHARED-001` ở mọi lần sửa thư viện emoji về sau (xem B-3).

---

## 7. Checklist đã chạy

- [x] **A. Coverage** — A.1 ✅ pass · A.2 ⚠️ RISK (F1 thiếu Boundary + tổ hợp multi-action; F2/F3 thiếu phạm vi) · A.3 N/A (không data) · A.4 ❌ **fail** (T2 High chỉ 2/9 tính năng) · A.5 ✅ không có orphan · A.6 ❌ **fail** (xem §3.5)
- [x] **B. Chất lượng từng TC** — B.1 ⚠️ NEW-24 thiếu precondition (M-6) · B.2 ✅ các TC atomic · B.3 ⚠️ NEW-24 không chạy độc lập được · B.4 ✅ data sample hợp lý (dùng keyword riêng theo lượt test — điểm tốt)
- [x] **C. Chất lượng bộ TC** — ❌ **fail**: Normal 9 / Abnormal 5 / **Boundary 0** (gợi ý 40/35/25) · không trùng lặp ✅ · phân bố quan điểm dồn vào `REG-SHARED-001` + `STATE-MATRIX-001` ⚠️ · không có TC phân quyền (không áp dụng) · multi-device chỉ NEW-12 ⚠️
- [x] **D. Spec alignment** — ⚠️ 2 hành vi chưa có spec (xem §6); không TC nào mâu thuẫn spec hiện có
- [x] **E. Hành chính** — ⚠️ TC No. không theo format repo (MINOR) · file 04 đúng folder ✅ · 15/15 TC còn `status=draft`, `reviewed=false` ❌
- [x] **F. Base quan điểm test LME**
  - [x] F.1 Quan điểm (tầng 1) — bảng dưới
  - [x] F.2 Catalog (tầng 2) — **A** ⚠️ ô nhập text (action textarea + ô search emoji) chưa bê đủ 3 cột Normal/Abnormal/Boundary · **B** ⚠️ đã chạm UIC-04/05/11/13/15 nhưng thiếu ESC (UIC-05, UIC-14) và icon-font ổn định (UIC-15) · **C** ⚠️ chưa duyệt hết khối SC-004 (2/9 tính năng) · **D/D2** ❌ 0 TC production (RULE-08) · **E** N/A (không chạm media/file)
  - [x] F.3 RULE — RULE-01 ❌ (M-4) · RULE-02 ⚠️ (§4.3) · RULE-03 N/A · RULE-06 ⚠️ (M-13) · RULE-07 ⚠️ (§4.3 D1) · RULE-08 ❌ (M-1) · RULE-09 ❌ (B-3, variants V1/V3) · RULE-12 ⚠️ (M-2 carry-over, B-1 case từng Không đạt)

### F.1 — Bảng quan điểm đối chiếu

> TC mang mã Studio lạ (`TOOL-*`, `STATE-MATRIX-001`) hoặc không gán mã **không được tính là cover** — ghi trong ngoặc để Leader thấy nguồn.

| Mã quan điểm | Ưu tiên | Trigger khớp task? | TC cover (suy luận) | Kết luận |
|---|---|---|---|---|
| `REG-SHARED-001` | **Cao** | ✅ **BẮT BUỘC** — mục 2 ghi rõ "sửa **thư viện dùng chung**" | NEW-9, NEW-18, NEW-19 | **RISK → nâng BLOCKER** — chỉ 2/9 tính năng SC-004, thiếu `Boundary` (RULE-01). §4.1 B-3 |
| `COMPAT-LEGACY-001` | **Cao** | ✅ SC-004 có 3 variants (V1 legacy / V2 / V3 pro) — đối tượng đã version-up | *(không có)* | **GAP** → **[BLOCKER]** §4.1 B-3 · RULE-09 |
| `DEPLOY-ASSET-001` | **Cao** | ✅ **BẮT BUỘC** — release sửa file JS + **nâng version chung** | NEW-21 (Normal), NEW-22 (Abnormal) | **RISK → nâng BLOCKER** — thiếu luồng critical, 404, glyph, icon-font; thiếu `Boundary`. §4.1 B-2 |
| `ENV-003` | **Cao** | ✅ asset/cache/domain — Catalog D (`p.lmes.jp`, B2, loadbalance 2 server) | *(0 TC production)* | **GAP** → **[MAJOR]** M-1 · RULE-08 |
| `FUNC-004` | **Cao** | ✅ textarea action text max **5.000** + counter, fix chạm luồng chèn ký tự | *(không có)* | **GAP** → **[MAJOR]** M-4 |
| `FUNC-001` | **Cao** | ✅ luồng chính "mở bảng emoji → chèn vào đúng ô" | NEW-1 *(đang gắn `TOOL-KNOW-002` — không tính)*, NEW-2 *(đang gắn `TOOL-NEGCTRL-001` — không tính)* | **RISK** — nội dung có cover nhưng **mã quan điểm không map được** → M-7, đề nghị `testcase_update` gắn lại `FUNC-001` |
| `DATA-TEXT-001` | **Trung bình → Cao** (text gửi qua LINE) | ✅ emoji là ký tự đặc biệt, được gửi ra LINE | NEW-6 | **RISK** — chỉ 1 TC Normal, chạy `env=local` (M-13). Thiếu ký tự đặc biệt khác (①②③, ㈱) |
| `DATA-CACHE-001` | **Trung bình → Cao** (output user-facing) | ✅ release đổi JS/asset | NEW-22 | **RISK** — thiếu nhánh "tab mở sẵn trước deploy, không refresh" (M-14) |
| `DEPLOY-LIVE-001` | **Cao** | ✅ release lên production không lock maintain, version chung đổi | *(không có)* | **GAP** → **[MAJOR]** M-14 |
| `FUNC-MULTI-001` | **Trung bình** | ✅ modal cho phép **nhiều action 「テキスト」** (spec SC-004: "Không giới hạn") | *(không có)* | **GAP** → **[BLOCKER]** §4.1 B-4 — nâng severity vì trùng class với root cause + REQ-002 risk High |
| `FUNC-SEQ-001` | **Trung bình** | ✅ chuỗi thao tác mở/đóng/chèn liên tiếp không reload | NEW-4, NEW-23 | **RISK** — có chuỗi thao tác nhưng **không TC nào F5 sau chuỗi** rồi đối chiếu (yêu cầu cốt lõi của quan điểm) |
| `CONC-003` | **Trung bình** | ✅ nhiều picker cùng gắn handler, race ở tầng client | NEW-17 | **RISK** — chỉ 1 Abnormal; thiếu nhánh Network throttling / delay response (mục 3-4 của quan điểm) |
| `UI-002` | **Trung bình** | ✅ mọi chức năng có UI user-facing | NEW-12 | **RISK** — thiếu **Mac Safari** trong precondition, kết quả ghi ở `env=local` (M-12) |
| `UI-003` | **Trung bình → Cao** (rủi ro false success) | ✅ bảng emoji tải dữ liệu bất đồng bộ từ `/full-emoji-list.json` | *(không có)* | **GAP** → **[MAJOR]** M-5 — alternative root cause |
| `UI-001` | **Trung bình** | ✅ modal — `UIC-05` yêu cầu đóng bằng X / **ESC** / click ra ngoài | NEW-5, NEW-15 *(đang gắn `STATE-MATRIX-001` — không tính)* | **GAP về ESC** → **[MAJOR]** M-10. Nhánh click-ra-ngoài và đóng-modal có cover nhưng sai mã quan điểm |
| `UI-INPUT-001` | **Trung bình** | ✅ ô nhập text (action textarea) + ô 「Search emoji」 | NEW-24 *(không gán mã — không tính)* | **GAP** → **[MAJOR]** M-6 |
| `FUNC-DRAFT-001` | **Trung bình** | ✅ modal soạn nội dung action, đóng modal giữa chừng | *(không có)* | **GAP** → **[MINOR]** — gộp vào `TC-UI001-02` |
| `DATA-001` | **Cao** | ✅ emoji lưu rồi hiển thị lại ở list/detail/preview | NEW-18 | **RISK** — chỉ verify ở 自動応答, chưa verify tầng DB (RULE-07) |
| `LIST-001` | **Trung bình** | ⚠️ một phần — bảng emoji có search + danh sách, nhưng không phải màn danh sách nghiệp vụ | NEW-24 *(không tính)* | **RISK** — đã gộp vào `TC-UIINPUT001-01…03`, không tách riêng |
| `REG-SPEC-001` | **Cao** | ✅ 9 TC bị xoá giữa vòng test | *(không áp dụng)* | **[MAJOR]** M-10 — case hết hiệu lực phải **đánh dấu, không xoá** |
| `REG-RUN-001` | **Cao** | ⚠️ fix front-end thuần, không có job/dữ liệu chạy dở bị chạm | *(không áp dụng)* | `×` — lý do: fix chỉ chạm JS phía client, không có tiến trình nền |
| `PERM-001` / `PERM-002` / `PERM-003` / `SEC-*` | **Cao** | ❌ fix không chạm phân quyền, không chạm PII, không chạm cách ly bot | — | `×` — lý do: fix front-end thuần trong phạm vi 1 modal |
| `MEDIA-*` · `JOB-001` · `PERF-LARGE-001` · `PAY-*` · `MSG-001/002/004/005` · `INTG-*` · `BULK-001` · `DATA-BACKUP-001` · `DATA-DB-001` · `DATA-MIG-001` | Cao / Trung bình | ❌ không trigger — fix không chạm media, job nền, dữ liệu lớn, thanh toán, điều kiện gửi tin, tích hợp bên thứ 3, backup/migration | — | `×` — lý do đã ghi |

> ⚠️ §4 "Quan điểm chưa đủ bằng chứng" của `checklist-lme.md` (CHAT-01, TPL-01, ADM-01/03/04, FORM-01) **không được dùng** để flag BLOCKER/MAJOR theo **RULE-11** — không mục nào được viện dẫn trong report này.

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | | |
| Tester | (đã đọc & hiểu feedback) | |

---

<!-- Draft sinh bởi /review-tc ngày 2026-08-25. Nguồn TC: MCP LME TEST STUDIO task #174 round 2 (15 TC, contentTrust=untrusted, read-only). Nguồn phụ: task_get_history, review_list_comments (rỗng), spec-features/admin/action-settings (SC-004), spec-features/admin/chat-11. Đây là DRAFT cho Leader verify, không phải kết luận cuối. -->
