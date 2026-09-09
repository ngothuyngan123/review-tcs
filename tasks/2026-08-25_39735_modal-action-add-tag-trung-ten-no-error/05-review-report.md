# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | `#39735 — [Modal multi action] Add tag bị trùng name thì đang không hiển thị msg lỗi` |
| Reviewer (Leader) | `<Leader ký tên>` — draft sinh bởi `/review-tc` |
| Tester được review | **AI** (7/8 TC, job #497) + `cucdtk@mcp` (1/8 TC) — *không có TC nào do member người viết từ đầu* |
| Ngày review | `2026-08-25` |
| Version TCs | Studio round 1 · 7 TC `version 2`, 1 TC `version 1` · toàn bộ `status = draft` |
| Vòng review | `Round 1` |

---

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn | **MCP LME TEST STUDIO task #173** (fetch trực tiếp, nguồn sự thật) |
| Ticket · task_id · round · branch | `39735` · `#173` · round `1` · `ai_fixbug_39735` |
| Thời điểm fetch | `2026-08-25` (task_list xác nhận metadata không đổi so với lần fetch của `/new-task` cùng ngày) |
| Tổng số TC review | **8** |
| File 04 trong repo vs Studio | **Khớp** — `04-tc-list.md` sinh từ đúng payload Studio task #173 (8 TC, cùng tập `temp_id` NEW-5/6/7/9/10/11/12/13). Không có `[MAJOR] STALE-INPUT`. |
| Trạng thái Studio | `status = done-ai` · `reviewed = false` · `reviewState = leader` · `openBugs = 0` · `aiResult = null` · `submittedWithoutMcp = false` |

**Cảnh báo bắt buộc từ metadata Studio:**

| # | Chiều | Kết quả | Flag |
|---|---|---|---|
| 1 | Kết quả thực thi thật | **7/8 pass (87,5%)** · 0 fail · 0 error · **1 chưa chạy** | `OK` (≥ 80%) — nhưng xem #4 về giá trị của kết luận "Đạt" |
| 2 | TC `fail`/`error` + TC gắn ticket bug | **Không có TC fail/error.** `bug_tickets` rỗng ở cả 8 TC | `OK` — không có TC fail chưa raise ticket |
| 3 | Môi trường đã chạy | **PROD 0 · STAGING 0 · DEV 0 · LOCAL 8 (2 run)** | **`[MAJOR]` RULE-08 / ENV-003** — xem §4.2 |
| 4 | Ai chạy | **100% `last_exec.source = ai`**, `by = admin-lme-studio`, runId 439, 2026-08-24 10:02. **0 lượt QA người chạy** | **`[MAJOR]`** — 5 quan điểm ưu tiên **Cao** chỉ có bằng chứng từ pipeline AI |
| 5 | Tác giả TC | **7/8 (87,5%) `provenance.source = ai`** (job #497) · 1/8 người (`cucdtk@mcp`). `reviewState = leader` (chưa `done`) | **`[MAJOR]`** — ≥ 50% TC do AI sinh + review chưa đóng |
| 6 | Mã quan điểm Studio không có trong `checklist-lme.md` | **0 mã / 0 lượt TC** — cả 5 mã (`FUNC-001`, `FUNC-002`, `OUT-TRUTH-001`, `REG-SHARED-001`, `DEPLOY-ASSET-001`) đều có trong khung | `OK` — toàn bộ 8 TC map được coverage |

> **Ghi chú #1 vs #4**: 87,5% pass nhìn thì đẹp, nhưng **7/7 kết quả Đạt đều do AI tự chạy trên `local`, không có evidence đính kèm** (cột `Evidence thực tế` trống toàn bộ). Theo **RULE-02**, tick Đạt không kèm đúng loại bằng chứng thì **không được nghiệm thu**. Con số 87,5% vì vậy **chưa phải kết luận test hợp lệ**.

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — có issue BLOCKER, cần bổ sung TC và chạy lại

**Lý do ngắn gọn**: Bộ TC bám sát **đúng 2 nhánh lỗi mà API trả về** (rỗng / trùng tên) và có TC tái hiện bug gốc — phần lõi làm tốt. Nhưng **chưa cover nhánh request thất bại ở tầng HTTP** (500 / timeout / session hết hạn) — đúng nhánh mà triệu chứng gốc "bấm lưu không hiện gì cả" **vẫn còn nguyên**; **0/8 TC loại Boundary** trong khi 5 quan điểm ưu tiên Cao đều bị kích hoạt (RULE-01); và **Dev chưa cung cấp danh sách nơi ảnh hưởng** cho một modal dùng chung ở ~30 màn / 55 file blade (REG-SHARED-001).

---

## 2. Tóm tắt cho member

Bộ TC này làm tốt phần khó nhất: có TC **tái hiện đúng nguyên văn steps của ticket** (`TC-OUTTRUTH001-02`), expected ghi **đúng nguyên văn câu lỗi tiếng Nhật** thay vì "hiển thị đúng", và biết mở rộng smoke sang màn thứ hai dùng chung modal (`アクションスケジュール`). TC do người bổ sung (`TC-OUTTRUTH001-03`) đúng trọng tâm "multi action" của ticket — đây là TC giá trị nhất trong bộ.

Ba thứ phải bổ sung trước khi chốt: (1) **nhánh lỗi tầng HTTP** — fix hiện chỉ hiển thị lỗi khi API trả về HTTP 200 kèm `status=false`; nếu request 500 / timeout / session hết hạn thì màn hình **vẫn im lặng y như bug cũ**, chưa TC nào chạm tới; (2) **không có TC nào loại Boundary** — ô 「追加するタグ名」 có bộ đếm `/50` nên biên 50/51 ký tự và "chỉ nhập space" là bắt buộc theo RULE-01; (3) **kết quả Đạt chưa có evidence** và toàn bộ chạy trên `local` — riêng TC cache asset (`TC-DEPLOYASSET001-01`) thì chạy local **không kết luận được gì**, phải chạy lại ở STAGING/PRODUCTION.

---

## 3. Coverage Matrix

| Impact | Loại | Priority | TCs map | # TC | Exec | Status |
|---|---|---|---|---|---|---|
| **BUG** — popup 「タグ新規追加」 nuốt lỗi API (gán `error_message` nhưng không ai render) | Fix | — | `TC-OUTTRUTH001-02` (tái hiện), `TC-OUTTRUTH001-01`, `TC-OUTTRUTH001-03`, `TC-REGSHARED001-02` | 4 | 3/4 | **RISK** — cover đủ 2 nhánh `status=false` mà API trả về, **thiếu nhánh request thất bại tầng HTTP** (xem §3.5 + GAP-1) |
| **F1** — `saveAddTag` nhánh `.done()`, `public/js/select_action.js` (2 dòng 258/273) | Function | Direct | `TC-FUNC001-01`, `TC-FUNC002-01`, `TC-OUTTRUTH001-01/02/03`, `TC-REGSHARED001-01/02` | 7 | 6/7 | **RISK** — có Normal + Abnormal, **0 Boundary** (RULE-01) |
| **F2** — asset version `config/sns-line.php:62` → `202608190316` | Function | Direct | `TC-DEPLOYASSET001-01` | 1 | 1/1 | **RISK** — 1 TC, **chạy `local`** nên không kết luận được về cache/CDN; chỉ đi qua màn Chat 1:1, không đi luồng critical |
| **D1** — *(Dev ghi: không có data bị chạm)* | Data | — | — | — | — | **N/A** — không phát sinh yêu cầu TC data (đã đối chiếu: diff không đụng bảng `tags`) |
| **T1** — Action Settings (SC-004), modal dùng chung **~30 màn / 55 file blade** | Feature | *Dev không ghi* | `TC-REGSHARED001-01/02` (màn `アクションスケジュール`) + 5 TC màn Chat 1:1 | 7 | 6/7 | **RISK** — mới smoke **2/~30 màn**, và **Dev chưa cung cấp danh sách nơi ảnh hưởng** (REG-SHARED-001) |
| **T2** — Tag Management (FA-012) | Feature | *Dev không ghi* | `TC-FUNC001-01` (tạo tag qua popup) | 1 | 1/1 | **RISK** — cover đường tạo tag **trong popup**, nhưng **0 TC regression cho màn 「タグ管理」** (Studio REQ-010: màn này dùng endpoint + JS riêng, ngoài diff) |
| **T3** — 1-on-1 Chat (FA-001) — màn phát hiện bug | Feature | *Dev không ghi* | `TC-FUNC001-01`, `TC-FUNC002-01`, `TC-OUTTRUTH001-01/02/03`, `TC-DEPLOYASSET001-01` | 6 | 5/6 | **OK** — đủ Normal + Abnormal, có TC tái hiện, đã pass |
| **T4** — mọi màn admin nạp lại js/css sau khi tăng asset version (suy từ F2) | Feature | *Leader đánh giá* | `TC-DEPLOYASSET001-01` (chỉ màn Chat 1:1) | 1 | 1/1 | **RISK** — `DEPLOY-ASSET-001` yêu cầu chạy lại **luồng critical** (mua plan / hủy hợp đồng / gửi tin) sau F5 thường; không TC nào chạm |

### ORPHAN TCs

| TC No. | Tiêu đề | Lý do orphan | Hành động đề xuất |
|---|---|---|---|
| — | — | **Không có TC orphan.** Cả 8 TC đều trace được về BUG / F1 / F2 / T1–T4. | Giữ nguyên |

> **Đối chiếu ngược — 4/10 requirement Studio khai báo mà 0 TC gắn**: `REQ-006` (phạm vi kiểm trùng theo bot, không theo folder) · `REQ-007` (contract endpoint từng nhánh) · `REQ-009` (emoji / full-width / đúng 50 ký tự) · `REQ-010` (regression màn 「タグ管理」). Xem §4.

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| **Fix shape** | **Generic display của thông điệp lỗi do server trả về** — mục 2 dev-impact: *"nay bật thẳng hộp thoại cảnh báo (alert) với đúng nội dung lỗi API trả về"*, tức `alert(b.msg)` trong nhánh `.done()`. Không phải specific code-check (không có `if (code === X)`), nhưng **cũng không phải catch-all thật**: chỉ chạy khi request **thành công ở tầng HTTP**. |
| **Trigger space cần cover** | Đối chiếu spec endpoint [`action-settings/web/api-spec.md`](../../spec-features/admin/action-settings/web/api-spec.md) EP-10 `POST /ajax/save-add-tag-in-modal-action` + [`logic-spec.md`](../../spec-features/admin/action-settings/web/logic-spec.md) §8 — backend chỉ có **2 nhánh lỗi**: ① `tag_name` rỗng → `新しいタグ名を入力してください`; ② trùng tên trong bot → `そのタグ名はすでに利用されています`. Ngoài ra còn **③ nhánh request KHÔNG trả về HTTP 200**: exception 500 / timeout mạng / session hết hạn (redirect login) / CSRF token hết hạn (419). |
| **Số trigger TCs hiện cover** | **2/3** — ① `TC-FUNC002-01` · ② `TC-OUTTRUTH001-01/02/03`, `TC-REGSHARED001-02`. **③ = 0 TC.** |
| **KH report dạng** | **Có root cause cụ thể** — file 01 ghi rõ *"API trả về lỗi nhưng GUI không hiển thị msg lỗi gì cả"* + expected là **đúng nguyên văn** `そのタグ名はすでに利用されています`. → **AP-2 (symptom-only) KHÔNG áp dụng**, không cần bắt cover thêm root cause thay thế. |
| **Alternative root causes cần verify** | N/A (đã xác định chính xác root cause) |
| **Anti-patterns dính** | **AP-1 (biến thể)** — không phải "single-trigger" (2/2 nhánh `status=false` đã cover đủ), nhưng **thiếu hoàn toàn nhánh fallback khi request thất bại**, tức đúng tinh thần "chưa có TC trigger condition CHƯA BIẾT" của review-checklist §A.6. · **AP-3 (happy-path-only regression)** — T1 liệt kê modal dùng chung ~30 màn nhưng mỗi màn chỉ 1 TC ở trạng thái sạch. · **AP-5 KHÔNG dính** — không có TC nào test dư sang layer backend chưa bị chạm. · **AP-6 KHÔNG dính** — mục 3 có 4 dòng, không trống (nhưng chưa đủ, xem BLOCK-3). · **AP-4 một phần** — không có link PR, chỉ có branch `ai_fixbug_39735` + commit `497e386f64` + mô tả diff (2 dòng, +3/-3); đủ để suy fix shape nên chỉ ghi ở mức NIT. |

> **Kết luận §3.5**: trigger space cover **2/3** → flag **`[BLOCKER] FIX-SHAPE`** ở §4.1 (BLOCK-1).

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- **`[BLOCKER] FIX-SHAPE` GAP-1 — Nhánh request thất bại ở tầng HTTP vẫn im lặng đúng như bug cũ**: fix chỉ đặt `alert(b.msg)` trong nhánh `.done()`, tức **chỉ chạy khi API trả HTTP 200**. Khi request 500 / timeout mạng / session hết hạn (redirect login) / CSRF 419 thì `.done()` không chạy → **màn hình không hiện gì**, đúng triệu chứng nguyên văn ticket *"khi click save thì GUI không hiển thị msg lỗi gì cả"*. Báo cáo Dev **chỉ nhắc tới nhánh `.done()`**, không nói có `.fail()` handler hay không. — **Đề xuất**: hỏi Dev xác nhận `saveAddTag()` có `.fail()`/`.always()` không; bổ sung **`TC-OUTTRUTH001-04`** (chặn request bằng DevTools → offline) và **`TC-OUTTRUTH001-05`** (session hết hạn) ở §5. Nếu Dev xác nhận **không có** `.fail()` → đây là **bug còn sót của chính ticket này**, raise ticket riêng, không đóng #39735.

- **`[BLOCKER] RULE-01` GAP-2 — 0/8 TC loại `Boundary`, trong khi `FUNC-004` (ưu tiên **Cao**) bị kích hoạt rõ ràng**: ô 「追加するタグ名」 có bộ đếm hiển thị `/50` (Studio `REQ-009`; spec [`logic-spec.md`](../../spec-features/admin/action-settings/web/logic-spec.md) §8.1 ghi *"max 50 chars — watch ở Vue, không validate server"*). `FUNC-004` yêu cầu **5 pattern**: đúng biên / biên+1 / biên−1 / 0 / rỗng — hiện **chỉ có "rỗng"** (`TC-FUNC002-01`). Cả bộ TC không có **một TC Boundary nào**, nên **cả 5 quan điểm ưu tiên Cao** đều vi phạm RULE-01 mà không TC nào ghi lý do miễn trừ. — **Đề xuất**: thêm `TC-FUNC004-01/-02/-03` ở §5 (trùng tên dài đúng 50 ký tự full-width → câu lỗi vẫn hiện đủ, popup không vỡ layout; chỉ nhập space; 50 ký tự hợp lệ lưu được).

- **`[BLOCKER] FIX-SHAPE` GAP-3 — `REG-SHARED-001`: Dev chưa cung cấp danh sách nơi ảnh hưởng cho modal dùng chung**: mục 1 dev-impact ghi *"modal chọn hành động dùng chung cho khoảng 30 màn"*, Studio `REQ-005` ghi *"include ở 55 file blade"*, nhưng mục 3 chỉ liệt kê **4 function/file** và **không có danh sách màn**. AI chỉ `grep modalAddTagModalAction` (tên popup) rồi kết luận "không sót chỗ nào" — điều đó chứng minh **popup là duy nhất**, chứ **không** chứng minh 55 màn include nó đều hoạt động. TC hiện smoke **2/~30 màn**. `REG-SHARED-001` (**Cao**) yêu cầu *"dev cung cấp danh sách nơi ảnh hưởng → test lại từng mục"*. — **Đề xuất**: yêu cầu Dev xuất danh sách 55 blade include `modal_select_action`; Leader chọn tập con theo rủi ro (ưu tiên màn thuộc luồng **thanh toán / hủy hợp đồng / gửi tin** — `DEPLOY-ASSET-001` xếp các luồng này là "Cao tuyệt đối"); thêm `TC-REGSHARED001-03` ở §5.

### 4.2 Major (nên fix)

- **`[MAJOR] RULE-08 / ENV-003` — `TC-DEPLOYASSET001-01` chạy trên `local` là không kết luận được**: TC này verify **cache trình duyệt + tham số version asset sau deploy**, tức đúng chiều `domain / loadbalance` mà Catalog D cấm kết luận từ môi trường thấp. Trên `local` thường không đi qua CDN / loadbalance / cache header của môi trường thật. Studio ghi `env_tag = local-only` cho chính TC này. — **Đề xuất**: chạy lại ở `STAGING`, smoke `PRODUCTION` sau deploy; thêm `TC-DEPLOYASSET001-02` (§5).

- **`[MAJOR]` Metadata #4 — toàn bộ 7 kết quả Đạt do pipeline AI tự chạy, 0 lượt QA người**: `last_exec.source = ai`, `by = admin-lme-studio` ở cả 7 TC pass. Trong đó có 5 quan điểm ưu tiên **Cao**. Riêng bản chất fix là hiện **hộp thoại `alert()` gốc của trình duyệt** — công cụ tự động thường bắt dialog qua handler và tự đóng, nên "pass" của AI **không chứng minh người dùng thật nhìn thấy câu lỗi trên màn hình**. — **Đề xuất**: QA người chạy lại tối thiểu `TC-OUTTRUTH001-02` (tái hiện bug) + `TC-REGSHARED001-02`, kèm screenshot alert thật.

- **`[MAJOR] RULE-02` — 7 TC tick Đạt nhưng cột `Evidence thực tế` trống toàn bộ**: `testcase_list` không trả evidence và Studio cũng không có link evidence trong payload. RULE-02: *"chỉ tick Đạt khi đã đính kèm đúng loại bằng chứng"*, không chấp nhận "đã xem, OK". — **Đề xuất**: lấy artifact của Studio run #439 gắn vào từng TC, hoặc chạy lại tay và đính screenshot.

- **`[MAJOR]` — `Trạng thái đánh giá spec` = trống ở cả 8 TC**, trong khi có ít nhất 1 hành vi **spec không định nghĩa**: chính `TC-OUTTRUTH001-02` ghi trong note *"nhập 'tc39735_dup_a' (khác hoa/thường) và ' TC39735_DUP_A ' (thừa khoảng trắng) — hành vi đúng chưa được spec quy định"*. Bỏ trống cột này là nguy cơ **tự suy diễn rồi cho Đạt**. — **Đề xuất**: điền `Spec ghi rõ` cho các TC bám EP-10 (spec `api-spec.md` có đủ 3 response), điền `Spec không ghi` + tên người đã hỏi cho nhánh hoa/thường & space; kết quả chốt đưa vào §6.

- **`[MAJOR]` Metadata #5 — 87,5% TC do AI sinh, `reviewState` chưa `done`**: 7/8 TC `provenance.source = ai` (job #497), chỉ 1 TC do người (`cucdtk@mcp`). Task chưa `reviewed`. — **Đề xuất**: QA người phải ký xác nhận từng TC (đọc + đồng ý) trước khi bộ TC được tính là "member đã viết".

- **`[MAJOR]` GAP-4 — `REQ-006` (phạm vi kiểm trùng theo bot, không theo folder) có requirement nhưng **0 TC**: Studio khai báo *"tag trùng tên nằm ở thư mục khác trong cùng bot vẫn phải bị báo trùng; cùng tên tag ở bot khác thì được phép tạo"*. Đây chính là chiều `WHERE` scope của câu kiểm trùng — nếu scope sai thì **câu lỗi mới thêm sẽ bắn nhầm** (chặn user tạo tag hợp lệ) hoặc **không bắn** (im lặng trở lại). — **Đề xuất**: `TC-FUNCUNIQ001-02` (khác folder cùng bot) + `TC-FUNCUNIQ001-03` (cùng tên ở bot khác) ở §5.

- **`[MAJOR] FUNC-UNIQ-001` GAP-5 — hoa/thường và space đầu/cuối chưa có TC**: `FUNC-UNIQ-001` yêu cầu *"kiểm thêm hoa/thường (case-insensitive), space đầu/cuối"*; Catalog `DI-01` Abnormal yêu cầu *"chỉ nhập space → sau trim thành rỗng, xử lý như bỏ trống"*. Studio đã tự nhận diện đúng biến thể này nhưng xếp *"đáng thử thêm khi có thời gian"* → **không thành TC**. — **Đề xuất**: `TC-FUNCUNIQ001-01` ở §5, và đưa hành vi mong đợi vào §6 (spec chưa định nghĩa).

- **`[MAJOR] CONC-001` GAP-6 — double-click nút 「保存してアクションに設定に戻る」 nay sinh rủi ro MỚI do chính fix**: trước fix, click đúp thì lần 2 trả lỗi trùng và bị **nuốt im lặng** nên user không thấy gì. Sau fix, lần 2 sẽ **bật alert "そのタグ名はすでに利用されています"** dù thao tác của user đã **thành công** → user hiểu nhầm là thất bại. `CONC-001` (Cao) yêu cầu kiểm double-click. — **Đề xuất**: `TC-CONC001-01` ở §5; nếu tái hiện được → hỏi Dev có disable nút trong lúc request chạy không.

- **`[MAJOR] AP-3` GAP-7 — `REQ-010` regression màn 「タグ管理」 có requirement nhưng **0 TC**: Studio ghi màn này dùng **endpoint + file JS riêng** (`public/js/tag/index_v2.js:504-536`), nằm ngoài diff → rủi ro thấp nhưng T2 trong dev-impact có nêu Tag Management. — **Đề xuất**: 1 TC smoke regression (`TC-REGSHARED001-04`, ghi "regression" ở Ghi chú).

- **`[MAJOR] UI-INPUT-001` GAP-8 — paste bằng chuột phải chưa có TC**: `UI-INPUT-001` là **BẮT BUỘC với mọi màn có ô nhập text**; Catalog `UIC-04` cảnh báo đúng bẫy *"paste chuột phải xong nút Lưu vẫn disable (JS chỉ nghe keyboard event)"*. Popup này có ô text + bộ đếm ký tự chạy bằng Vue watcher, và fix vừa đụng đúng file JS của popup. — **Đề xuất**: `TC-UIINPUT001-01` ở §5 (Ctrl+V và chuột phải, Windows + Mac).

- **`[MAJOR] UI-003 / UIC-05` GAP-9 — chưa TC nào kiểm main modal mở lại sau khi popup báo lỗi**: [`logic-spec.md`](../../spec-features/admin/action-settings/web/logic-spec.md) §8.1 ghi rõ *"sub-modal `#modalAddTagModalAction` mở → main modal `#settingActionUrlModal` **đóng**"*, và chỉ mở lại ở nhánh **success**. Sau fix, nhánh lỗi dừng lại ở sub-modal → nếu user đóng sub-modal bằng **X / Esc / click ra ngoài** thì main modal 「アクション設定」 có mở lại không, hay user rơi về màn trắng/mất toàn bộ action đang cấu hình? `TC-OUTTRUTH001-03` chỉ kiểm khi user bấm **OK** trên alert. — **Đề xuất**: `TC-UI003-01` ở §5.

- **`[MAJOR]` — `TC-OUTTRUTH001-03` (Studio `priority = High`, TC người viết, đúng trọng tâm "multi action" của ticket) **chưa chạy lần nào**: `last_exec = null` vì được thêm lúc 2026-08-24 10:11, sau run #439 (10:02). Đây là TC duy nhất kiểm state của các action khác trong modal. — **Đề xuất**: chạy lại run mới bao gồm TC này **trước** khi kết luận task; không tính task là "đã test xong" khi TC High duy nhất chưa chạy.

### 4.3 Minor (có thể fix sau)

- **`[MINOR] RULE-02` — không TC nào ghi *loại* evidence bắt buộc ở cột `Ghi chú`**: các quan điểm liên quan yêu cầu evidence cụ thể (`OUT-TRUTH-001`: đối chiếu thông báo UI với dữ liệu thật; `DEPLOY-ASSET-001`: screenshot DevTools Network kèm query version + màn sau F5 thường). Ghi chú hiện chỉ có metadata Studio.
- **`[MINOR]`** — cột `Môi trường test` của `TC-OUTTRUTH001-03` đang là `ALL (dự kiến)` vì `env_scope = ["all"]` và chưa chạy. Nên chốt `STAGING` cho lần chạy đầu.
- **`[MINOR]`** — `TC-DEPLOYASSET001-01` gộp **2 mục đích** trong 1 TC (kiểm version asset + kiểm câu lỗi trùng tên) → vi phạm B.2 "atomic". Chấp nhận được vì bước 1–3 là tiền đề của bước 4–7, nhưng nếu fail thì khó quy trách nhiệm. Cân nhắc tách.

### 4.4 Nit (gợi ý)

- **`[NIT] AP-4`** — mục "Commit / Pull Request" của `03-dev-impact.md` **không có link PR**, chỉ có branch + commit hash + mô tả diff. Đủ để suy fix shape trong lần này, nhưng nếu có PR link thì reviewer verify được ngay có `.fail()` handler hay không (chính là BLOCK-1) mà không phải hỏi Dev.
- **`[NIT]`** — `TC-REGSHARED001-01/02` nên ghi thêm chữ **"regression"** ở `Ghi chú` cho khớp quy ước repo (TC verify màn ngoài phạm vi phát hiện bug).
- **`[NIT] RULE-11`** — không dùng §4 "Quan điểm chưa đủ bằng chứng" của `checklist-lme.md` (`CHAT-01`, `ADM-01/03/04`…) để flag trong report này, dù task chạm màn Chat 1:1. Chỉ ghi nhận để Leader biết đã cân nhắc.

---

## 5. TCs đề xuất bổ sung

> Member copy thẳng vào `04-tc-list.md` round tiếp theo. **16 cột canonical**, `TC No.` không trùng 8 TC đã có.
> ⚠️ TC Studio là read-only — các TC dưới đây phải tạo trên Studio bằng `testcase_create` rồi fetch lại, **không sửa tay** file 04.

| TC No. | Mã quan điểm liên kết | Loại case | Tiêu đề test case | Điều kiện tiền đề | Các bước thực hiện | Dữ liệu test/input | Kết quả mong đợi | Kết quả thực thi | Evidence thực tế | Môi trường test | Người thực hiện | Ngày thực hiện | Số ticket bug | Trạng thái đánh giá spec | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-OUTTRUTH001-04 | OUT-TRUTH-001 | Abnormal | Mất mạng khi lưu tag trong popup modal action: màn hình phải báo lỗi, không im lặng | - Đã đăng nhập admin, đã chọn bot test, dùng nhánh `ai_fixbug_39735`<br>- Bot có ít nhất 1 thư mục tag<br>- Biết mở DevTools của trình duyệt | 1. Mở màn Chat 1:1, chọn một người bạn<br>2. Bấm 「アクション」 để mở modal 「アクション設定」<br>3. Thêm một hành động, chọn loại 「タグ」, bấm 「タグ新規追加」<br>4. Mở DevTools, tab Network, chuyển chế độ mạng sang **Offline**<br>5. Nhập một tên tag chưa tồn tại<br>6. Bấm 「保存してアクションに設定に戻る」<br>7. Quan sát màn hình trong 10 giây: có thông báo nào hiện ra không, lớp phủ loading có tắt không<br>8. Bật lại mạng, bấm lưu lần nữa | Tên tag: `TC39735_OFFLINE_<yyyymmddHHMMSS>`; chế độ mạng: Offline | Bước 7: màn hình **phải hiện một thông báo lỗi đọc được** (không cần đúng câu tiếng Nhật nào cụ thể, nhưng không được im lặng) và lớp phủ loading phải tắt — đây đúng là triệu chứng gốc của ticket. Bước 8: sau khi có mạng lại, lưu thành công, popup đóng, tag mới có trong danh sách action. | Chưa test | | STAGING | | | | Đã hỏi leader | **Lấp GAP-1 / BLOCK-1** — cover impact BUG + F1. Nhánh request không trả HTTP 200 (`.done()` không chạy). Evidence bắt buộc: **video quay màn hình lúc bấm lưu ở chế độ Offline** + screenshot tab Network thể hiện request failed. Nếu màn hình im lặng → **bug còn sót**, raise ticket riêng, không đóng #39735. |
| TC-OUTTRUTH001-05 | OUT-TRUTH-001 | Abnormal | Session hết hạn khi lưu tag trong popup modal action: phải báo lỗi hoặc đưa về đăng nhập, không im lặng | - Đã đăng nhập admin, đã chọn bot test, dùng nhánh `ai_fixbug_39735`<br>- Có thể xoá cookie phiên đăng nhập từ DevTools > Application | 1. Mở màn Chat 1:1, chọn một người bạn<br>2. Bấm 「アクション」 → thêm hành động loại 「タグ」 → bấm 「タグ新規追加」<br>3. Nhập tên tag chưa tồn tại nhưng **chưa bấm lưu**<br>4. Mở DevTools > Application > Cookies, xoá cookie phiên đăng nhập của site<br>5. Quay lại popup, bấm 「保存してアクションに設定に戻る」<br>6. Quan sát: có thông báo gì hiện ra không, hay bị điều hướng về màn đăng nhập | Tên tag: `TC39735_SESSION_<yyyymmddHHMMSS>` | Hệ thống **phải phản hồi rõ ràng**: hiện thông báo lỗi hoặc điều hướng về màn đăng nhập. **Không được** đứng im không hiện gì như bug cũ. Không tạo tag mới. | Chưa test | | STAGING | | | | Spec không ghi | **Lấp GAP-1 / BLOCK-1** — cover impact BUG + F1. Evidence bắt buộc: **video thao tác** + screenshot tab Network (mã trạng thái của request). Hành vi mong đợi chưa có trong spec → xem §6. |
| TC-FUNC004-01 | FUNC-004 | Boundary | Tên tag trùng dài đúng 50 ký tự full-width: câu lỗi vẫn hiện đủ, popup không vỡ layout | - Đã đăng nhập admin, đã chọn bot test, dùng nhánh `ai_fixbug_39735`<br>- Đã tạo sẵn ở màn 「タグ管理」 một tag tên gồm **đúng 50 ký tự full-width tiếng Nhật**<br>- Ghi lại tên tag đó để nhập lại y hệt | 1. Mở màn Chat 1:1 → 「アクション」 → thêm hành động loại 「タグ」 → 「タグ新規追加」<br>2. Nhập lại **đúng** tên tag 50 ký tự đã tạo ở tiền đề<br>3. Quan sát bộ đếm ký tự dưới ô nhập<br>4. Bấm 「保存してアクションに設定に戻る」<br>5. Quan sát thông báo lỗi và bố cục popup | 50 ký tự full-width, VD: `テスト用タグ名テスト用タグ名テスト用タグ名テスト用タグ名テスト用タグ名テスト用タグ名テスト用タグ名テスト用タグ名テスト用タグ名テスト用タグ名` (đếm đủ 50) | Bước 3: bộ đếm hiển thị **50/50**, ô nhập không tràn ra ngoài khung. Bước 5: hiện đúng 「そのタグ名はすでに利用されています」, **chữ trong hộp thoại không bị cắt**, popup 「タグ新規追加」 vẫn mở, không tạo tag mới. | Chưa test | | STAGING | | | | Spec ghi rõ | **Lấp GAP-2 / BLOCK-2** (RULE-01 — quan điểm Cao thiếu Boundary) — cover impact F1. Nguồn limit: bộ đếm `/50` trên UI + `api-spec.md` EP-10 (`max 50 ký tự`). Evidence bắt buộc: **screenshot bộ đếm 50/50** + screenshot hộp thoại lỗi. |
| TC-FUNC004-02 | FUNC-004 | Abnormal | Chỉ nhập toàn dấu cách vào ô tên tag rồi lưu | - Đã đăng nhập admin, đã chọn bot test, dùng nhánh `ai_fixbug_39735`<br>- Bot có ít nhất 1 thư mục tag | 1. Mở màn Chat 1:1 → 「アクション」 → thêm hành động loại 「タグ」 → 「タグ新規追加」<br>2. Nhập **5 dấu cách** vào ô 「追加するタグ名」, không nhập ký tự nào khác<br>3. Quan sát bộ đếm ký tự<br>4. Bấm 「保存してアクションに設定に戻る」<br>5. Nếu lưu được → vào màn 「タグ管理」 xem tag vừa tạo hiển thị thế nào | Tên tag: `"     "` (5 dấu cách half-width) | Hệ thống xử lý như **bỏ trống**: hiện 「新しいタグ名を入力してください」, không tạo tag. **Không được** tạo ra một tag tên rỗng/trắng trong danh sách 「タグ管理」. | Chưa test | | STAGING | | | | Spec không ghi | **Lấp GAP-2 / BLOCK-2** — cover impact F1. Theo Catalog `DI-01` Abnormal: *"chỉ nhập space → sau trim thành rỗng, xử lý như bỏ trống"*. Evidence bắt buộc: screenshot thông báo + screenshot màn 「タグ管理」 sau thao tác. Hành vi trim chưa có trong spec → xem §6. |
| TC-FUNC004-03 | FUNC-004 | Normal | Tên tag hợp lệ dài đúng 50 ký tự lưu được và hiện đúng trong danh sách action | - Đã đăng nhập admin, đã chọn bot test, dùng nhánh `ai_fixbug_39735`<br>- Bot chưa có tag nào trùng tên với dữ liệu test | 1. Mở màn Chat 1:1 → 「アクション」 → thêm hành động loại 「タグ」 → 「タグ新規追加」<br>2. Chọn một thư mục cụ thể ở 「追加するフォルダ選択」<br>3. Nhập tên tag mới dài **đúng 50 ký tự**<br>4. Bấm 「保存してアクションに設定に戻る」<br>5. Xem danh sách tag trong action vừa quay lại<br>6. Mở màn 「タグ管理」 kiểm tra tag mới nằm đúng thư mục đã chọn | 50 ký tự, trộn latinh + full-width, VD `TC39735B50_あいうえおかきくけこ...` (đếm đủ 50) | Không có thông báo lỗi. Popup đóng, modal 「アクション設定」 mở lại, danh sách tag của action có tag vừa tạo, **tên hiển thị đủ 50 ký tự không bị cắt cụt**. Ở màn 「タグ管理」 tag nằm đúng thư mục đã chọn. | Chưa test | | STAGING | | | | Spec ghi rõ | **Lấp GAP-2 / BLOCK-2** (bổ sung Normal cho `FUNC-004` để đủ 3 loại case) — cover impact F1 + T2. Evidence bắt buộc: screenshot danh sách tag trong action + screenshot màn 「タグ管理」. |
| TC-FUNC004-04 | FUNC-004 | Boundary | Dán tên tag 51 ký tự (vượt biên) vào ô có bộ đếm tối đa 50 | - Đã đăng nhập admin, đã chọn bot test, dùng nhánh `ai_fixbug_39735`<br>- Đã copy sẵn vào clipboard một chuỗi **đúng 51 ký tự**<br>- Ghi lại số lượng tag hiện tại ở màn 「タグ管理」 | 1. Mở màn Chat 1:1 → 「アクション」 → thêm hành động loại 「タグ」 → 「タグ新規追加」<br>2. Dán chuỗi 51 ký tự vào ô 「追加するタグ名」 (dán, không gõ tay — bộ đếm Vue có thể chặn gõ nhưng không chặn dán)<br>3. Quan sát bộ đếm ký tự hiển thị bao nhiêu, ô nhập giữ lại bao nhiêu ký tự<br>4. Bấm 「保存してアクションに設定に戻る」<br>5. Vào màn 「タグ管理」 xem tag vừa tạo (nếu có) tên dài bao nhiêu ký tự | Chuỗi dán: đúng **51 ký tự** latinh, VD `TC39735_B51_AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA` (đếm đủ 51) | Hệ thống xử lý **nhất quán**: hoặc cắt còn đúng 50 ký tự và bộ đếm hiển thị 50/50, hoặc chặn lưu kèm thông báo rõ ràng. **Không được** lưu vào hệ thống một tag dài 51 ký tự, và **không được** im lặng không phản hồi. | Chưa test | | STAGING | | | | Spec không ghi | **Lấp GAP-2 / BLOCK-2** (pattern biên+1 của `FUNC-004`) — cover impact F1. ⚠️ Spec [`logic-spec.md`](../../spec-features/admin/action-settings/web/logic-spec.md) §8.1 ghi rõ *"max 50 chars — watch ở Vue, **không validate server**"* → nếu tag 51 ký tự lưu được thì đây là **rủi ro riêng nằm ngoài phạm vi fix #39735**, ghi nhận và raise ticket riêng (xem §6 mục 3). Evidence bắt buộc: screenshot bộ đếm sau khi dán + screenshot tên tag trong 「タグ管理」 (kèm số ký tự đếm được). |
| TC-FUNCUNIQ001-01 | FUNC-UNIQ-001 | Abnormal | Tên tag khác hoa/thường và thừa dấu cách so với tag đã tồn tại | - Đã đăng nhập admin, đã chọn bot test, dùng nhánh `ai_fixbug_39735`<br>- Trong bot đã có sẵn tag tên `TC39735_DUP_A`<br>- Ghi lại số lượng tag hiện tại ở màn 「タグ管理」 | 1. Mở màn Chat 1:1 → 「アクション」 → thêm hành động loại 「タグ」 → 「タグ新規追加」<br>2. Nhập `tc39735_dup_a` (toàn chữ thường) → bấm 「保存してアクションに設定に戻る」 → ghi nhận màn hình hiện gì<br>3. Mở lại popup, nhập ` TC39735_DUP_A ` (có 1 dấu cách ở đầu và cuối) → bấm lưu → ghi nhận màn hình hiện gì<br>4. Vào màn 「タグ管理」 đếm lại số tag và xem có tag nào mới trông "giống hệt" tag cũ không | Lần 1: `tc39735_dup_a` · Lần 2: ` TC39735_DUP_A ` (space đầu + cuối) | **Ghi nhận kết quả quan sát được, chưa kết luận Đạt/Không đạt** cho tới khi leader chốt spec. Điều **chắc chắn phải đúng**: hệ thống phản hồi rõ ràng ở cả 2 lần (báo trùng **hoặc** tạo thành công), **không được im lặng**; và nếu tạo thành công thì màn 「タグ管理」 **không được** xuất hiện 2 tag trông y hệt nhau khiến user không phân biệt được. | Chưa test | | STAGING | | | | Spec không ghi | **Lấp GAP-5** — cover impact F1 + BUG. Chính Studio đã nêu biến thể này trong note của `TC-OUTTRUTH001-02` nhưng không thành TC. Evidence bắt buộc: screenshot màn hình sau **mỗi** lần bấm lưu + screenshot danh sách 「タグ管理」 trước/sau. **Bắt buộc hỏi leader chốt spec trước khi cho Đạt** — xem §6. |
| TC-FUNCUNIQ001-02 | FUNC-UNIQ-001 | Abnormal | Tag trùng tên nằm ở thư mục khác trong cùng bot vẫn phải bị báo trùng | - Đã đăng nhập admin, đã chọn bot test, dùng nhánh `ai_fixbug_39735`<br>- Bot có **2 thư mục tag** khác nhau, VD `FolderA` và `FolderB`<br>- Đã tạo sẵn tag `TC39735_FOLDER_X` nằm trong `FolderA` | 1. Mở màn Chat 1:1 → 「アクション」 → thêm hành động loại 「タグ」 → 「タグ新規追加」<br>2. Ở 「追加するフォルダ選択」 chọn **`FolderB`** (khác thư mục chứa tag đã có)<br>3. Nhập tên `TC39735_FOLDER_X`<br>4. Bấm 「保存してアクションに設定に戻る」<br>5. Vào màn 「タグ管理」 kiểm tra `FolderB` có phát sinh tag mới không | Tên tag: `TC39735_FOLDER_X`; thư mục chọn: `FolderB` (tag gốc nằm ở `FolderA`) | Hiện đúng 「そのタグ名はすでに利用されています」. `FolderB` **không** phát sinh tag mới. Phạm vi kiểm trùng là **theo bot**, không theo thư mục. | Chưa test | | STAGING | | | | Spec ghi rõ | **Lấp GAP-4** (Studio `REQ-006` — 0 TC) — cover impact F1 + BUG. Nếu kiểm trùng bị bó theo thư mục thì câu lỗi mới thêm sẽ **không bắn** → bug im lặng quay lại ở tình huống này. Evidence bắt buộc: screenshot thông báo + screenshot 2 thư mục ở màn 「タグ管理」. |
| TC-FUNCUNIQ001-03 | FUNC-UNIQ-001 | Normal | Cùng tên tag ở bot khác thì vẫn tạo được, không bị báo trùng nhầm | - Có quyền truy cập **2 bot** khác nhau (bot A và bot B)<br>- Bot A đã có tag tên `TC39735_CROSSBOT`<br>- Bot B chưa có tag nào tên đó<br>- Dùng nhánh `ai_fixbug_39735` | 1. Chuyển sang **bot B**<br>2. Mở màn Chat 1:1 → 「アクション」 → thêm hành động loại 「タグ」 → 「タグ新規追加」<br>3. Nhập tên `TC39735_CROSSBOT`<br>4. Bấm 「保存してアクションに設定に戻る」<br>5. Vào màn 「タグ管理」 của bot B kiểm tra tag mới<br>6. Chuyển về bot A, vào 「タグ管理」 kiểm tra tag của bot A không bị đổi | Tên tag: `TC39735_CROSSBOT` (đã tồn tại ở bot A, chưa có ở bot B) | Bot B **tạo thành công**, không hiện thông báo lỗi, popup đóng và tag mới có trong danh sách action. Bot A giữ nguyên tag cũ, không bị sửa hay mất. | Chưa test | | STAGING | | | | Spec ghi rõ | **Lấp GAP-4** (Studio `REQ-006`) — cover impact F1. Đây là chiều **cách ly dữ liệu giữa 2 bot** (`PERM-003` / `DATA-DB-001`): câu lỗi bắn nhầm sẽ chặn user tạo tag hợp lệ. Evidence bắt buộc: screenshot 「タグ管理」 của **cả 2 bot** sau thao tác. |
| TC-REGSHARED001-03 | REG-SHARED-001 | Abnormal | Smoke báo lỗi trùng tag ở màn thuộc luồng critical dùng chung modal action | - Đã có **danh sách màn include `modal_select_action` do Dev cung cấp** (yêu cầu ở BLOCK-3)<br>- Leader đã chọn 3 màn rủi ro cao trong danh sách (ưu tiên màn thuộc luồng thanh toán / hủy hợp đồng / gửi tin)<br>- Bot có sẵn tag `TC39735_DUP_A`<br>- Dùng nhánh `ai_fixbug_39735` | 1. Mở **màn thứ nhất** trong danh sách leader chọn<br>2. Mở modal 「アクション設定」 từ màn đó<br>3. Thêm hành động loại 「タグ」 → bấm 「タグ新規追加」<br>4. Nhập `TC39735_DUP_A` → bấm 「保存してアクションに設定に戻る」<br>5. Ghi nhận màn hình hiện gì<br>6. Lặp lại bước 1–5 cho **màn thứ hai** và **màn thứ ba** | Tên tag: `TC39735_DUP_A` (đã tồn tại). Số màn test: 3 màn do leader chọn từ danh sách Dev | **Cả 3 màn** đều hiện đúng 「そのタグ名はすでに利用されています」, popup vẫn mở, không tạo tag mới, và **các cấu hình đang dở trên màn gốc không bị mất**. | Chưa test | | STAGING | | | | Spec ghi rõ | **Lấp GAP-3 / BLOCK-3** — cover impact T1 (modal dùng chung ~30 màn / 55 blade). **Chặn**: chưa có danh sách Dev thì chưa chạy được TC này. Ghi rõ tên 3 màn đã test vào Ghi chú khi chạy. Evidence bắt buộc: screenshot thông báo lỗi ở **từng màn** (3 ảnh). `regression` |
| TC-REGSHARED001-04 | REG-SHARED-001 | Normal | Regression màn 「タグ管理」: luồng thêm tag riêng của màn này không đổi hành vi | - Đã đăng nhập admin, đã chọn bot test, dùng nhánh `ai_fixbug_39735`<br>- Bot có sẵn tag `TC39735_DUP_A` | 1. Mở màn 「タグ管理」 (không đi qua modal action)<br>2. Dùng chức năng thêm tag **của chính màn này**, nhập tên `TC39735_DUP_A`<br>3. Bấm lưu, ghi nhận thông báo<br>4. Thêm tiếp một tag tên chưa tồn tại, bấm lưu<br>5. Kiểm tra danh sách tag sau mỗi thao tác | Lần 1: `TC39735_DUP_A` (trùng) · Lần 2: `TC39735_TAGMGR_<yyyymmddHHMMSS>` | Bước 3: màn 「タグ管理」 báo trùng **y như trước fix** (không đổi hành vi, không mất thông báo). Bước 4: tạo tag mới thành công, xuất hiện trong danh sách. | Chưa test | | STAGING | | | | Spec ghi rõ | **Lấp GAP-7** (Studio `REQ-010` — 0 TC) — cover impact T2. Màn này dùng endpoint + file JS **riêng** (`public/js/tag/index_v2.js`), ngoài diff → mục đích là chứng minh fix **không lan sang**. Evidence bắt buộc: screenshot thông báo trùng + danh sách tag. `regression` |
| TC-DEPLOYASSET001-02 | DEPLOY-ASSET-001 | Normal | Sau deploy production, chỉ F5 thường vẫn nhận JS mới và luồng critical không hỏng | - Bản fix **đã deploy lên PRODUCTION**<br>- Trước khi deploy đã mở sẵn màn admin trên trình duyệt để cache asset bản cũ<br>- Không xoá cache, không dùng Ctrl+F5<br>- Có tài khoản đủ quyền vào luồng thanh toán / hủy hợp đồng | 1. Trên trình duyệt còn cache bản cũ, bấm **F5 thường** ở màn admin<br>2. Mở DevTools > Network, lọc `js` và `css`, kiểm tra mã trạng thái và tham số version của các file<br>3. Kiểm tra console có lỗi JavaScript không<br>4. Chạy luồng critical: mở màn **thanh toán / gói cước** và màn **hủy hợp đồng**, thao tác tới bước xác nhận (không hoàn tất giao dịch thật)<br>5. Mở màn Chat 1:1 → modal action → 「タグ新規追加」 → nhập tên tag đã tồn tại → bấm lưu | Không xoá cache trước khi F5. Tag trùng: một tag có thật trên bot production | Bước 2: toàn bộ js/css trả **HTTP 200 kèm tham số version mới**, **không có file 404**. Bước 3: console không có lỗi JS. Bước 4: 2 màn critical hiển thị và thao tác được bình thường, không vỡ layout, không mất icon/font. Bước 5: hiện đúng 「そのタグ名はすでに利用されています」 mà không cần Ctrl+F5. | Chưa test | | **PRODUCTION** | | | | Spec ghi rõ | **Lấp GAP-6 / `[MAJOR]` RULE-08** — cover impact F2 + T4. `DEPLOY-ASSET-001` xếp **"Cao tuyệt đối"** khi asset bị đổi nằm trong luồng thanh toán/hủy hợp đồng — bump version ở `config/sns-line.php` làm **toàn bộ** js/css nạp lại nên 2 màn này bắt buộc smoke. **RULE-08**: không kết luận từ local/staging. ⚠️ Tránh tạo/xoá dữ liệu thật trên production. Evidence bắt buộc: **screenshot DevTools Network** (version + 200) + screenshot 2 màn critical sau F5 thường. |
| TC-DEPLOYASSET001-03 | DEPLOY-ASSET-001 | Abnormal | Trình duyệt vẫn giữ JS bản cũ thì popup thêm tag hành xử ra sao | - Có 1 trình duyệt/profile đã cache `select_action.js` **bản trước fix**<br>- Môi trường đã lên bản fix<br>- Bot có sẵn tag `TC39735_DUP_A` | 1. Trên trình duyệt còn cache bản cũ, **không** F5, mở lại tab màn Chat 1:1 đang có sẵn<br>2. Mở modal action → 「タグ新規追加」<br>3. Nhập `TC39735_DUP_A` → bấm 「保存してアクションに設定に戻る」<br>4. Ghi nhận màn hình hiện gì<br>5. Bấm F5 thường rồi lặp lại bước 2–4 | Tên tag: `TC39735_DUP_A` | Bước 4: **được phép** không hiện thông báo (vì JS cũ) — ghi nhận làm mốc so sánh, **không tạo tag mới**. Bước 5: sau F5 thường, cùng thao tác **phải** hiện 「そのタグ名はすでに利用されています」 → chứng minh tham số version đã ép nạp lại JS mới. | Chưa test | | STAGING | | | | Spec ghi rõ | **Lấp GAP-6** (bổ sung Abnormal cho `DEPLOY-ASSET-001` — RULE-01) — cover impact F2. Đây là TC chứng minh **giá trị thật** của việc bump asset version. Evidence bắt buộc: screenshot Network **trước và sau** F5 (2 ảnh, thấy rõ 2 tham số version khác nhau). |
| TC-CONC001-01 | CONC-001 | Abnormal | Click đúp nút lưu tag: không tạo tag trùng và không bắn thông báo lỗi gây hiểu nhầm | - Đã đăng nhập admin, đã chọn bot test, dùng nhánh `ai_fixbug_39735`<br>- Bot có ít nhất 1 thư mục tag<br>- Ghi lại số lượng tag hiện tại ở màn 「タグ管理」 | 1. Mở màn Chat 1:1 → 「アクション」 → thêm hành động loại 「タグ」 → 「タグ新規追加」<br>2. Nhập một tên tag **chưa tồn tại**<br>3. **Click đúp thật nhanh** vào 「保存してアクションに設定に戻る」<br>4. Quan sát: nút có bị khoá trong lúc chờ không, có hộp thoại lỗi nào bật lên không<br>5. Vào màn 「タグ管理」 đếm lại số tag và tìm tên vừa nhập | Tên tag: `TC39735_DBLCLICK_<yyyymmddHHMMSS>`; thao tác: click đúp nhanh | Chỉ tạo **đúng 1 tag** (số tag tăng đúng 1, không có 2 dòng cùng tên). **Không** bật hộp thoại 「そのタグ名はすでに利用されています」 — thao tác của user đã thành công, báo lỗi ở đây sẽ khiến user hiểu nhầm là thất bại. | Chưa test | | STAGING | | | | Spec không ghi | **Lấp GAP-6 (`[MAJOR] CONC-001`)** — cover impact F1 + BUG. **Rủi ro MỚI do chính fix sinh ra**: trước fix lần click thứ 2 bị nuốt im lặng nên vô hại; sau fix nó bật alert. Evidence bắt buộc: **video click đúp** + screenshot danh sách 「タグ管理」 trước/sau (đếm số tag). |
| TC-UIINPUT001-01 | UI-INPUT-001 | Normal | Dán tên tag bằng chuột phải và bằng Ctrl+V đều chạy đúng bộ đếm và nút lưu | - Đã đăng nhập admin, đã chọn bot test, dùng nhánh `ai_fixbug_39735`<br>- Có sẵn chuỗi tên tag trong clipboard<br>- Test trên **cả Windows và Mac** (Chrome + Safari trên Mac) | 1. Mở màn Chat 1:1 → 「アクション」 → thêm hành động loại 「タグ」 → 「タグ新規追加」<br>2. Đặt con trỏ vào ô 「追加するタグ名」, dán bằng **chuột phải > Paste**<br>3. Quan sát bộ đếm ký tự và trạng thái nút 「保存してアクションに設定に戻る」<br>4. Bấm lưu, ghi nhận kết quả<br>5. Xoá ô nhập, lặp lại bước 2–4 nhưng dán bằng **Ctrl+V** (Mac: Cmd+V)<br>6. Lặp lại toàn bộ trên máy còn lại (Windows ⇄ Mac) | Chuỗi dán: `TC39735_PASTE_あいうえお` (trộn latinh + full-width) | Cả 2 cách dán đều cho **kết quả giống nhau**: bộ đếm ký tự cập nhật đúng số ký tự đã dán, nút lưu ở trạng thái bấm được, và bấm lưu tạo tag thành công. Dán bằng chuột phải **không** được để bộ đếm đứng ở 0 hay nút lưu kẹt disable. | Chưa test | | STAGING | | | | Spec không ghi | **Lấp GAP-8** — cover impact F1. Catalog `UIC-04` cảnh báo đúng bẫy này (*JS chỉ nghe keyboard event*), và ô nhập này dùng watcher Vue để chạy bộ đếm `/50`. Evidence bắt buộc: **screenshot bộ đếm + trạng thái nút sau khi dán bằng chuột phải**, trên **cả Windows và Mac**. |
| TC-UI003-01 | UI-003 | Abnormal | Đóng popup bằng X / Esc sau khi bị báo trùng tag: modal action phải mở lại, cấu hình không mất | - Đã đăng nhập admin, đã chọn bot test, dùng nhánh `ai_fixbug_39735`<br>- Bot có sẵn tag `TC39735_DUP_A`<br>- Biết trước: mở popup 「タグ新規追加」 sẽ **đóng** modal 「アクション設定」 phía sau | 1. Mở màn Chat 1:1 → 「アクション」 để mở modal 「アクション設定」<br>2. Cấu hình trước 1 hành động khác (VD gửi tin) và giữ nguyên<br>3. Thêm hành động loại 「タグ」 → bấm 「タグ新規追加」<br>4. Nhập `TC39735_DUP_A` → bấm 「保存してアクションに設定に戻る」 → đóng thông báo lỗi<br>5. Đóng popup 「タグ新規追加」 bằng **nút X**<br>6. Quan sát: modal 「アクション設定」 có mở lại không, hành động cấu hình ở bước 2 còn không<br>7. Lặp lại bước 3–6 nhưng đóng popup bằng phím **Esc**, rồi lần nữa bằng **click ra vùng ngoài popup** | Tên tag trùng: `TC39735_DUP_A`; 3 cách đóng: nút X · phím Esc · click ra ngoài | Với **cả 3 cách đóng**: modal 「アクション設定」 mở lại được (không rơi về màn trắng, không phải tải lại trang), và hành động đã cấu hình ở bước 2 **còn nguyên**, không bị reset hay mất. | Chưa test | | STAGING | | | | Spec không ghi | **Lấp GAP-9** — cover impact BUG + T1 + T3. Theo `logic-spec.md` §8.1, popup mở thì modal cha **đóng** và chỉ mở lại ở nhánh **success** — nhánh lỗi mới thêm chưa rõ ai mở lại modal cha. `TC-OUTTRUTH001-03` chỉ kiểm khi bấm OK trên alert, chưa kiểm 3 cách đóng này. Evidence bắt buộc: **video** thao tác đủ 3 cách đóng. |

> **Tổng: 16 TC bổ sung** (Normal 5 · Abnormal 9 · Boundary 2) — lấp **9 GAP** (3 BLOCKER + 6 MAJOR).
> Phân bố loại case của cả bộ sau khi bổ sung: **Normal 9 · Abnormal 13 · Boundary 2** (trước đó 4 / 4 / **0**).
> `FUNC-004` (ưu tiên **Cao**) sau bổ sung có đủ 3 loại case theo RULE-01: Normal `-03` · Abnormal `-02` · Boundary `-01`, `-04`.

---

## 6. Spec update needed

- [ ] Không cần update spec
- [x] **Cần update spec** — 3 điểm:

**(1) Hành vi so trùng tên tag khi khác hoa/thường hoặc thừa dấu cách**
  - Section: [`spec-features/admin/action-settings/web/api-spec.md`](../../spec-features/admin/action-settings/web/api-spec.md) EP-10 · [`tag-management/feature-spec.md`](../../spec-features/admin/tag-management/feature-spec.md) §validation
  - Nội dung cần update: spec hiện chỉ ghi *"check duplicate name trong bot"*, **không** định nghĩa so trùng có phân biệt hoa/thường không, và có trim dấu cách đầu/cuối trước khi so không. Chính Studio đã ghi đây là **câu hỏi mở**. Cần chốt để `TC-FUNCUNIQ001-01` và `TC-FUNC004-02` có oracle rõ ràng.
  - Người chịu trách nhiệm: `<PM / Dev owner tag-management>`

**(2) Hành vi khi request lưu tag thất bại ở tầng HTTP**
  - Section: [`action-settings/web/logic-spec.md`](../../spec-features/admin/action-settings/web/logic-spec.md) §8 "Tag Creation Inline"
  - Nội dung cần update: flow hiện chỉ mô tả nhánh **success** (đóng sub-modal → mở lại main modal → `initDataTag`) và 2 nhánh `status=false`. **Không** định nghĩa hành vi khi request 500 / timeout / session hết hạn / CSRF 419. Đây chính là lỗ hổng ở BLOCK-1.
  - Người chịu trách nhiệm: `<Dev owner action-settings>`

**(3) Ràng buộc độ dài tên tag chỉ tồn tại ở frontend**
  - Section: [`action-settings/web/logic-spec.md`](../../spec-features/admin/action-settings/web/logic-spec.md) §8.1 — spec đã ghi nguyên văn *"max 50 chars — watch ở Vue, **không validate server**"*
  - Nội dung cần update: cần ghi rõ đây là **quyết định có chủ đích** hay **thiếu sót**. Nếu là thiếu sót thì gọi thẳng API với tên > 50 ký tự sẽ ghi được vào bảng `tags` — **rủi ro riêng, nằm ngoài phạm vi fix #39735** (fix chỉ đụng 2 dòng JS hiển thị lỗi, không đụng backend). → **Không** flag BLOCKER cho ticket này, nhưng **đề nghị Leader raise ticket riêng** để Dev đánh giá.
  - Người chịu trách nhiệm: `<Dev owner action-settings>`

---

## 7. Checklist đã chạy

- [x] **A. Coverage** — A.1 ✅ (có TC tái hiện đúng steps ticket) · A.2 ⚠️ (F1 thiếu Boundary, F2 chỉ 1 TC chạy local) · A.3 N/A (không có data impact) · A.4 ⚠️ (T1/T2/T4 RISK) · A.5 ✅ (0 orphan) · **A.6 ❌ FAIL** (trigger space 2/3 — xem §3.5)
- [x] **B. Chất lượng từng TC** — B.1 ✅ tốt (expected ghi **đúng nguyên văn câu lỗi tiếng Nhật**, không dùng "hiển thị đúng"; precondition đầy đủ, dựng được env) · B.2 ⚠️ (`TC-DEPLOYASSET001-01` gộp 2 mục đích) · B.3 ✅ (mỗi TC tự tạo/kiểm tiền đề, dùng dấu thời gian tránh đụng dữ liệu lần chạy trước) · B.4 ✅ (data test realistic, có quy ước đặt tên)
- [ ] **C. Chất lượng bộ TC tổng thể** — ❌ **FAIL**: phân bố loại case **Normal 4 / Abnormal 4 / Boundary 0** (khuyến nghị ~40/35/25) · **0 TC Boundary** · phân bố quan điểm lệch (3/8 TC dồn vào `OUT-TRUTH-001`) · không có TC role/permission (chấp nhận được — fix không chạm phân quyền) · **không có TC multi-device/browser** dù là fix UI (`UI-002`)
- [x] **D. Spec alignment** — ✅ TC **không mâu thuẫn** spec: expected 「そのタグ名はすでに利用されています」 và 「新しいタグ名を入力してください」 khớp đúng `api-spec.md` EP-10. ⚠️ 3 điểm spec chưa định nghĩa → §6. Folder **không có** `02-spec-reference.md` → đã fallback sang `spec-features/admin/action-settings/` + `tag-management/` (chi tiết hơn `LME-SYSTEM-SPEC.md`)
- [x] **E. Hành chính** — ✅ `TC No.` đúng format `TC-<mã quan điểm bỏ gạch>-<nn>` · file lưu đúng folder review · ⚠️ **`Người thực hiện` / `Ngày thực hiện` chỉ có của pipeline AI**, chưa có QA người ký
- [x] **F. Base quan điểm test LME**
  - [x] F.1 Quan điểm (tầng 1) — bảng dưới
  - [x] F.2 Catalog (tầng 2) — đã mở **A** (`DI-01` Text 1 dòng: Normal/Abnormal/Boundary) · **B** (`UIC-04` ô nhập, `UIC-05` modal/dialog, `UIC-11` loading/rỗng/lỗi, `UIC-15` icon/font/asset) · **C** (`MAP-TAG-01/03`: modal multi action nằm trong cả nhóm *hiển thị* lẫn *cập nhật* tag) · **D** (`ENV-PATH` / khác biệt production cho asset) · **E** N/A (không chạm media/file)
  - [ ] F.3 RULE quy trình — **RULE-01 ❌ FAIL** (0 Boundary cho 5 quan điểm Cao, không TC nào ghi lý do miễn trừ) · **RULE-02 ❌ FAIL** (7 TC Đạt không evidence) · RULE-03 N/A (chưa ai lập bảng ◯/×) · RULE-06 ✅ N/A (không có output ra LINE/mail/file — bug nằm ở màn admin) · RULE-07 ⚠️ (TC có kiểm "số lượng tag không tăng" = chạm tầng dữ liệu ở mức quan sát UI, chấp nhận được vì fix không đụng backend) · **RULE-08 ❌ FAIL** (0 TC ngoài `local`) · RULE-09 ✅ N/A (không chạm đối tượng đã version-up)

### F.1 — Bảng quan điểm đối chiếu

| Mã quan điểm | Ưu tiên | Trigger khớp task? | TC cover (suy luận) | Exec | Kết luận |
|---|---|---|---|---|---|
| `FUNC-001` — luồng chính đúng đặc tả | **Cao** | ◯ — mọi chức năng | `TC-FUNC001-01` (Normal) | 1/1 | **RISK** — chỉ 1 TC Normal, thiếu Boundary (RULE-01) |
| `FUNC-002` — bỏ trống trường bắt buộc | **Cao** | ◯ — popup có form nhập | `TC-FUNC002-01` (Abnormal) | 1/1 | **RISK** — chỉ 1 luồng vào (popup). `FUNC-002` yêu cầu test **đủ luồng**: tạo/sửa/copy/import/gọi thẳng API. Các luồng khác **không tồn tại** ở popup này → chấp nhận, nhưng thiếu Normal + Boundary |
| `FUNC-003` — nhập sai định dạng | Trung bình | ◯ — ô text tự do | — | — | **GAP** → gộp vào GAP-2/GAP-5 (`TC-FUNC004-01/02`, `TC-FUNCUNIQ001-01`) |
| `FUNC-004` — giới hạn ký tự / số lượng | **Cao** | ◯ — ô 「追加するタグ名」 có bộ đếm `/50` | — | — | **GAP** → **`[BLOCKER]` BLOCK-2**. Bổ sung `TC-FUNC004-01/-02/-03` |
| `FUNC-UNIQ-001` — unique check | Trung bình | ◯ — tên tag bắt buộc duy nhất trong bot | *(gián tiếp qua các TC trùng tên, nhưng không kiểm hoa/thường, space, scope folder/bot)* | — | **GAP** → **`[MAJOR]`**. Bổ sung `TC-FUNCUNIQ001-01/-02/-03` |
| `FUNC-MULTI-001` — đa phần tử cùng loại | Trung bình | ◯ — ticket nằm ở **modal multi action** | `TC-OUTTRUTH001-03` | **0/1 (chưa chạy)** | **RISK** — TC duy nhất cover và **chưa chạy lần nào** |
| `FUNC-SEQ-001` — thao tác liên tiếp & reload | Trung bình | × | — | — | × — popup 1 thao tác đơn, không có sort/nhiều tab. *(Lý do theo RULE-03)* |
| `CONC-001` — 1 hành động chỉ xử lý 1 lần | **Cao** | ◯ — có nút lưu, fix làm lần click thứ 2 **bật alert** thay vì im lặng | — | — | **GAP** → **`[MAJOR]`**. Bổ sung `TC-CONC001-01` |
| `CONC-003` — race tầng giao diện | Trung bình | × | — | — | × — popup chỉ 1 request, không loadmore/phân trang/nhiều tab |
| `DATA-001` — cập nhật phản ánh ở mọi màn | **Cao** | × | `TC-FUNC001-01` (chỉ danh sách tag trong action) | 1/1 | × **có chủ đích** — `MAP-TAG-01` liệt kê 8 nơi hiển thị tag, nhưng diff **không chạm** đường INSERT backend (chỉ 2 dòng JS hiển thị lỗi + 1 dòng config). Test lan sang 8 nơi = **AP-5 over-coverage**. *(Lý do theo RULE-03)* |
| `DATA-TEXT-001` — emoji & ký tự đặc biệt | Trung bình | ◯ — Studio `REQ-009`; tên tag có export CSV | — | — | **RISK** → đã gộp full-width vào `TC-FUNC004-01/-03`; emoji để mức `[NIT]` (không thuộc đường code bị sửa) |
| `DATA-DB-001` — WHERE scope + khóa mồ côi | **Cao** | × (một phần) | — | — | × — flow này **chỉ CREATE**, không UPDATE/DELETE nên trigger chính không khớp. Chiều `WHERE` scope của câu **kiểm trùng** đã chuyển sang `TC-FUNCUNIQ001-02/-03`. *(Lý do theo RULE-03)* |
| `DATA-AUDIT-001` — audit log | **Cao** | × | — | — | × — tag là dữ liệu nhạy cảm theo trigger, **nhưng** fix không đổi đường ghi tag (không thêm/sửa/xóa bản ghi nào so với trước). Nếu Leader muốn chắc → 1 TC smoke lịch sử thao tác, mức `[NIT]` |
| `PERM-001/002/003/004` | **Cao** | × | — | — | × — fix không chạm phân quyền/route. Riêng cách ly 2 bot đã cover bằng `TC-FUNCUNIQ001-03` |
| `MSG-*` (gửi tin) | **Cao** | × | — | — | × — không có đường gửi tin nào bị chạm |
| `OUT-PREVIEW-001` | **Cao** | × | — | — | × — popup không có chế độ preview/test-send |
| `OUT-TRUTH-001` — UI/message khớp trạng thái THẬT | **Cao** | ◯ — **đây là quan điểm lõi của ticket** | `TC-OUTTRUTH001-01` (Normal), `-02` (Abnormal, tái hiện), `-03` (Abnormal, chưa chạy), `TC-REGSHARED001-02` | 3/4 | **RISK** — cover tốt 2 nhánh `status=false` nhưng **thiếu nhánh HTTP thất bại** → **`[BLOCKER]` BLOCK-1**; thiếu Boundary (RULE-01) |
| `UI-001` — responsive theo surface | Trung bình | ◯ — có UI | — | — | **GAP** mức `[NIT]` — popup chỉ có ở admin web (PC); nên bổ sung kiểm ở **1366×768** khi chạy `TC-FUNC004-01` (chữ lỗi dài không vỡ layout) |
| `UI-002` — khác biệt trình duyệt / thiết bị | Trung bình | ◯ — fix là JS + `alert()` gốc trình duyệt | — | — | **GAP** → đã gộp vào `TC-UIINPUT001-01` (Windows + Mac, Chrome + Safari) |
| `UI-003` — loading / rỗng / lỗi | Trung bình → **Cao** | ◯ — **nâng Cao**: bug này chính là rủi ro *false success* (bấm lưu, không phản hồi, user tưởng đã lưu) | `TC-OUTTRUTH001-01`, `-03` (kiểm "không kẹt loading") | 1/2 | **RISK** → thiếu nhánh đóng popup bằng X/Esc/click ngoài. Bổ sung `TC-UI003-01` |
| `UI-FIELD-001` — field con theo field cha | Trung bình | ◯ nhẹ — chọn loại action 「タグ」 làm hiện khối tag | *(gián tiếp qua bước 3 của mọi TC)* | — | **OK (gián tiếp)** — mọi TC đều đi qua bước chọn loại action; không cần TC riêng |
| `UI-INPUT-001` — hành vi ô nhập liệu | Trung bình | ◯ — **BẮT BUỘC** với mọi màn có ô nhập text | — | — | **GAP** → **`[MAJOR]`**. Bổ sung `TC-UIINPUT001-01` |
| `PAY-*` (thanh toán & gói cước) | **Cao** | × (trực tiếp) | — | — | × cho luồng nghiệp vụ. **Nhưng** bump asset version làm màn thanh toán nạp lại js/css → đã chuyển thành bước 4 của `TC-DEPLOYASSET001-02` |
| `STATE-*` (trạng thái & lifecycle) | **Cao** | × | — | — | × — không có quy trình nhiều bước nào bị gián đoạn bởi fix |
| `REG-SHARED-001` — shared code / logic | **Cao** | ◯ — **modal dùng chung ~30 màn / 55 blade** | `TC-REGSHARED001-01` (Normal), `-02` (Abnormal) | 2/2 | **RISK** → **`[BLOCKER]` BLOCK-3**: mới 2/~30 màn và **Dev chưa cung cấp danh sách nơi ảnh hưởng** (RULE-12). Bổ sung `TC-REGSHARED001-03/-04` |
| `REG-RUN-001` — job/dữ liệu chạy dở khi release | **Cao** | × | — | — | × — fix không chạm job nền, không có dữ liệu đang chạy dở |
| `REG-SPEC-001` — spec đổi giữa chừng | **Cao** | × | — | — | × — spec không đổi sau khi có TC (round 1) |
| `SEC-001/002/SEC-ISO-001` | **Cao** | × | — | — | × — `alert()` hiển thị **chuỗi hằng của server** (không phải input user) nên không có đường XSS mới; không lộ token |
| `PERF-LARGE-001` | Trung bình | × | — | — | × — thao tác đơn lẻ, không có dữ liệu lớn |
| `ENV-003` — khác biệt dev/staging/production | **Cao** | ◯ — asset version + cache trình duyệt | `TC-DEPLOYASSET001-01` (chạy `local`) | 1/1 | **RISK** → **`[MAJOR]` RULE-08**. Bổ sung `TC-DEPLOYASSET001-02` (PRODUCTION) |
| `JOB-001` — job nền / batch | **Cao** | × | — | — | × — không có job nền bị chạm |
| `LIST-001` / `BULK-001` | Trung bình / **Cao** | × | — | — | × — popup không có search/filter/phân trang/thao tác hàng loạt |
| `MEDIA-*` | Trung bình | × | — | — | × — không chạm file/ảnh |
| `FRIEND-001` | **Cao** | × | — | — | × — không chạm friend info |
| `DEPLOY-ASSET-001` — version asset JS/CSS | **Cao** | ◯ — **BẮT BUỘC**: diff có sửa file JS + bump version | `TC-DEPLOYASSET001-01` (Normal) | 1/1 | **RISK** — 1 TC, chạy `local`, chỉ đi màn Chat 1:1, thiếu Abnormal + luồng critical. Bổ sung `TC-DEPLOYASSET001-02/-03` |
| `DEPLOY-LIVE-001` — release không lock maintain | **Cao** | × | — | — | × — diff **không đổi payload API / field form / cấu trúc request** (chỉ 2 dòng JS hiển thị). Client cũ vẫn gọi được server mới. *(Lý do theo RULE-03)* |
| `COMPAT-LEGACY-001` — cũ & mới song song | **Cao** | × | — | — | × — không chạm template/form/remind/richmenu/spread hay bất kỳ đối tượng nào đã version-up |

**Tổng kết F.1**: 5 quan điểm ưu tiên **Cao** trigger khớp (`FUNC-001`, `FUNC-002`, `FUNC-004`, `OUT-TRUTH-001`, `REG-SHARED-001`, `DEPLOY-ASSET-001`, `CONC-001`, `ENV-003`) → **3 GAP mức BLOCKER** (`FUNC-004`, và 2 lỗ hổng chiều sâu ở `OUT-TRUTH-001` + `REG-SHARED-001`), **4 GAP mức MAJOR** (`FUNC-UNIQ-001`, `CONC-001`, `UI-INPUT-001`, `UI-003`), **1 RISK môi trường** (`ENV-003` / `DEPLOY-ASSET-001`). Không quan điểm nào bị đánh × mà thiếu lý do (RULE-03 pass).

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | | |
| Tester | (đã đọc & hiểu feedback) | |

<!-- Draft sinh bởi /review-tc ngày 2026-08-25. Nguồn TC: MCP LME TEST STUDIO task #173 (ticket 39735), 8 TC, contentTrust = untrusted (xử lý như data). TC là read-only — mọi chỉnh sửa/bổ sung phải thực hiện trên Studio (testcase_create / testcase_update) rồi fetch lại. Đây là DRAFT cho Leader verify, không phải kết luận cuối. -->
