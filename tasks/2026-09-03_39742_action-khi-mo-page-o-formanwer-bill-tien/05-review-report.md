# 05 — Review Report

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| **Nguồn đã dùng** | **(1) MCP LME TEST STUDIO** — task `#171`, ticket `39742` |
| Vì sao không dùng nguồn dưới | Nguồn 1 trả về 41 TC → **dừng ngay**, KHÔNG fetch Google Sheet, KHÔNG đối chiếu chéo với file 04 cũ (đúng quy tắc "dừng ở nguồn đầu tiên có TC") |
| Thời điểm fetch | `2026-09-03` (fetch lại trong phiên review — xem cảnh báo **stale** bên dưới) |
| Tổng TC | **41** |
| Snapshot đã ghi | `04-tc-list.md` — **refresh ghi đè** bản do `/new-task` sinh sáng nay (bản cũ có header `<!-- source: MCP LME TEST STUDIO ... -->` → được phép đè theo 0.2b) |
| Metadata task | `status=done-ai` · `round=3` · `branch=ai_fixbug_39742` · `aiResult=pass` · `reviewState=leader` · **`reviewed=false`** · `openBugs=0` · `submittedWithoutMcp=false` |
| **Nguồn spec đã dùng** | `spec-features/admin/bill-item/feature-spec.md` (§7.3, dòng 366) · `spec-features/admin/bill-item/web/logic-spec.md:143,467` · `spec-features/admin/bill-item/db/db-mapping.md:454,1356` · `spec-features/admin/form-answer/feature-spec.md:134,145,627` (EP-38 `action_open_id`/`action_open_type`) · kho TCs `fa011` + `fa026` |

### ⚠️ 0.a — Snapshot bị stale trong vòng 1 giờ (bằng chứng bộ TC đang chuyển động)

| Lần fetch | pass | fail | other | staging | local |
|---|---|---|---|---|---|
| `/new-task` (~19:11) | 41 | 0 | 0 | 8 TC | 33 TC |
| `/review-tc` (~19:40) | **40** | 0 | **1 (`skip`)** | **24 TC** | 17 TC |

→ QA `thanhntp` đang **chạy manual trên staging ngay trong lúc review** (16 TC chuyển từ local → staging trong ~30 phút, `NEW-14` và `NEW-33` được cập nhật lúc `10:39`–`10:40`). **Report này chốt trên bản `40 pass / 1 skip`.** Leader cần fetch lại trước khi ra quyết định cuối.

### 0.b — Cảnh báo bắt buộc về chất lượng nguồn (mục 0.6)

| # | Nội dung | Kết luận |
|---|---|---|
| 1 | **Kết quả thực thi thật** | `pass` **40/41 = 97,6%** → **trên ngưỡng 80%, KHÔNG flag** ở mục này. 1 TC `skip` (`NEW-33`) = **không có kết luận test** → xử lý riêng ở §4.2. |
| 2 | **TC fail / có ticket bug** | **0 TC fail.** 1 TC gắn ticket bug: `NEW-13` → Redmine **#40150** *"URL có fragment (#): cờ bị chèn sau # nên không gửi lên server, F5 gửi action lần 2"*, đã `closed`, verified `2026-08-27` (run 630). ✅ Bug đã raise đúng quy trình — **không có TC fail chưa raise ticket**. |
| 3 | **Môi trường** | `staging` 24 · `local` 17 · **`prd` 0** · `dev` 0. Task chạm **bill tiền** (`SalesManagementV2Controller::orderDetail`, `bot_line_user_item.count_action_view_page`) + **URL/domain** + **asset JS sau release** → **`[MAJOR]` RULE-08 / ENV-003** (§4.2). |
| 4 | **Ai chạy** | `manual/thanhntp` 24 · `ai/ngavt` 17. Nhóm rủi ro cao (LINE app thật, bill tiền) **đã có QA người chạy** (NEW-38/43/44 manual staging) → **KHÔNG flag** mục này. `submittedWithoutMcp=false`. |
| 5 | **Tác giả TC** | `AI` **38/41 (92,7%)** · `thanhntp@mcp` 2 · `thanhntp` 1. ≥50% do AI sinh **và** `reviewed=false`, `reviewState=leader` → **`[MAJOR]`** (§4.2). |
| 6 | **Mã quan điểm lạ** | **10 mã / 21 TC** không có trong `framework/checklist-lme.md`: `TOOL-NEGCTRL-001`(6) · `TOOL-KNOW-002`(4) · `TOOL-AXIS-001`(3) · `API-CONTRACT-001`(2) · `RULE-06`(1) · `TOOL-OLDREC-001`(1) · `SEC-INJECT-001`(1) · `API-001`(1) · `TOOL-ERRHYG-001`(1) · `(trống)`(1). **21/41 TC không map được coverage** → §4.2. |

> **Diễn giải mục 6 — nêu rõ để Leader không hiểu nhầm**: quy tắc gốc bảo "coi như chưa cover". Tôi áp dụng **có phân biệt**: nơi nội dung TC **thực sự** kiểm đúng quan điểm (vd `NEW-38` mã `RULE-06` nhưng nội dung đúng `MSG-004`), tôi ghi **`RISK` + issue "sai mã, cần re-tag"** thay vì `GAP`, vì báo GAP ở đó sẽ khiến member viết lại TC đã có. Nơi **không** có TC nào kiểm nội dung → ghi `GAP` thật. Mọi chỗ áp dụng ngoại lệ đều ghi rõ trong §3.6.

### 0.c — Lịch sử run (`task_get_report`) — `last_exec` che mất

| Tổng auto toàn task | pass | fail | skip | **error** |
|---|---|---|---|---|
| | 102 | 1 | 5 | **42** |

| Run | Env | Status | Thời gian |
|---|---|---|---|
| 819 | staging | **queued** | chưa chạy |
| 792 | staging | **error** | 2026-09-03 06:29 → 08:54 |
| 780 | staging | **error** | 2026-09-03 04:38 → 05:18 |
| 630 | local | **pass** | 2026-08-27 02:01 → 02:21 |
| 539 / 536 / 423 | local | error | 2026-08-24 → 26 |
| 465 | local | **fail** | 2026-08-25 (sinh bug #40150) |

→ **Runner tự động chưa từng chạy xanh trên staging** (2 run `error`, 1 `queued`). Toàn bộ 24 kết quả staging hiện tại là **manual do QA bấm tay**, không phải runner. Không phải lỗi TC, nhưng Leader cần biết: **automation của task này chưa dùng được ngoài local**.

**Độ phủ spec theo Studio: `covered 0 / partial 48 / none 0`** — không mục spec nào được Studio tự đánh giá là phủ đủ.

---

## 1. Verdict

### ❌ REJECTED

3 `[BLOCKER]` — đều là **vùng bug lọt được ra production**, không phải vấn đề hình thức:
1. Không có TC kiểm phạm vi `WHERE` trên 2 bot (DATA-DB-001) dù fix có UPDATE bộ đếm.
2. Không có TC cache asset cho **trang bill tiền** — đúng loại file mà `DEPLOY-ASSET-001` xếp "Cao tuyệt đối".
3. Cơ chế chặn bằng param URL **không phủ các đường mở link khác** (richmenu / imagemap / QR / LIFF) mà kho TCs đã ghi là đường vào hợp lệ.

Cộng thêm **1 xung đột expected với kho TCs** (`TC-BIL-85`) chưa được ai chốt — xem §6.

---

## 2. Tóm tắt cho member

Bộ TC này **chất lượng cao hơn mặt bằng chung**: 41 TC bám sát 15 requirement, có TC negative-control cho từng nhánh không gửi action, có TC biên 10 biến thể giá trị cờ ở tầng API, và đã **tự tìm ra 1 bug thật (#40150 — URL có fragment)** rồi verify lại. Việc QA chạy tay trên staging cho các TC cần LINE app thật cũng đúng RULE-06.

Ba chỗ phải bổ sung trước khi merge: (1) **chưa có TC nào kiểm dữ liệu bị giới hạn đúng theo bot** — fix có UPDATE bộ đếm nhưng không ai chứng minh nó không đụng bot khác; (2) **TC cache asset chỉ làm cho màn biểu mẫu, bỏ trống màn bill tiền** — trong khi file blade bị sửa nằm thẳng trong luồng thanh toán; (3) **chỉ test đường mở link trực tiếp và từ chat LINE**, chưa test richmenu / imagemap / QR / link LIFF — mà cơ chế chặn nằm ở URL nên mỗi đường vào cho ra một URL khác nhau.

Ngoài ra: `NEW-33` đang `skip` (màn đơn hàng bản cũ chưa có kết luận), `NEW-45` viết quá sơ sài để dùng làm bằng chứng, và **kho TCs `TC-BIL-85` đang nói ngược với hành vi sau fix** — cần Leader chốt chứ member không tự sửa được.

---

## 3. Coverage Matrix

| Impact | Loại | TC cover (suy luận) | # TC | Exec | Status |
|---|---|---|---|---|---|
| **BUG** — action gửi lại mỗi lần reload | Root cause | NEW-2, NEW-23, NEW-38 | 3 | 3/3 pass | `OK` |
| **F1** `FormAnswerController::userOpenFormanswer` | Direct | NEW-4, 5, 6, 15, 16, 17, 18, 19, 20, 21 | 10 | 10/10 pass | `OK` |
| **F2** `SalesManagementV2Controller::orderDetail` | Direct | NEW-22…31, NEW-44 | 11 | 11/11 pass | `OK` |
| **F3** `FormAnswerService::renderFormAnswer` | Direct | NEW-1, 2 (gián tiếp qua render form) | 2 | 2/2 pass | `RISK` — không TC nào nhắm thẳng service, chỉ đi xuyên qua |
| **F4** `config/sns-line.php` (version asset) | Direct | NEW-34, NEW-35 | 2 | 2/2 pass | `RISK` — **chỉ phủ asset màn biểu mẫu v3**, bỏ màn bill tiền v2 → GAP-2 |
| **F5** `form_render_v3.js` | Direct | NEW-1, 2, 4, 5, 6, 12, 13 | 7 | 7/7 pass | `OK` |
| **F6** `form_render.blade.php` v3 | Direct | NEW-10 | 1 | 1/1 pass | `RISK` — 1 TC, chỉ chiều injection |
| **F7** `order/detail.blade.php` v2 | Direct | NEW-22, 23, 31 | 3 | 3/3 pass | `RISK` — không có TC cache asset cho blade này |
| **F8** `sendAction` / `sendActionOrderItem` (dùng chung) | Indirect | NEW-25, NEW-36 (tĩnh), NEW-45 (mơ hồ) | 3 | 3/3 pass | `RISK` — chỉ 1 TC runtime thật (NEW-25); slot action khác chưa test → GAP-7 |
| **F9** `SalesManagementController::orderDetail` v1 | Indirect | NEW-33 | 1 | **0/1 — `skip`** | `RISK` — **có TC nhưng không có kết luận** |
| **F10** `form_render.js` / blade bản cũ | Indirect | NEW-32 | 1 | 1/1 pass | `OK` |
| **D1** `user_open_formanswer.count_click` | UPDATE | NEW-2, NEW-3 | 2 | 2/2 pass | `OK` |
| **D2** `bot_line_user_item.count_action_view_page` | UPDATE | NEW-22, 23, 24, 29, 30, 31 | 6 | 6/6 pass | `RISK` — chỉ đọc DB, **không TC nào verify màn admin hiển thị số này** → GAP-6 |
| **D3** `action_lineuser` | CREATE | NEW-1, 2, 7, 8, 14, 22, 23, 26–30 | 12 | 12/12 pass | `OK` |
| **D1–D3 · phạm vi `WHERE` theo bot** | UPDATE | **(không có)** | 0 | — | **`GAP`** → GAP-1 `[BLOCKER]` |
| **T1** Form Builder (FA-011) | Regression | NEW-1…14, 32, 38, 43 | 17 | 17/17 pass | `RISK` — thiếu ma trận đường mở link (richmenu/imagemap/QR/LIFF) → GAP-3 |
| **T2** Single Product / Sales (FA-026) | Regression | NEW-22…31, 33, 44 | 12 | 11/12 (1 skip) | `RISK` — GAP-2 + GAP-6 + xung đột kho `TC-BIL-85` |
| **T3** Action Settings (SC-004) | Regression | NEW-21, NEW-45 | 2 | 2/2 pass | `RISK` — **[AP-3]** chỉ happy-path; các slot `申込完了時` / `決済時` / `解約時` chưa test runtime → GAP-7 |

**Tổng kết**: `OK` 6 · `RISK` 9 · `GAP` 1.

### ORPHAN TCs

| TC | Vấn đề |
|---|---|
| `NEW-45` | **Không có `viewpoint`, `case_type`, `screen`; `precondition` rỗng.** Nội dung (`action submit form` + `action khi mua sản phẩm success`) nằm **ngoài phạm vi "action khi mở page"** của ticket. Đây thực chất là regression cho hàm dùng chung `sendAction` (F8) nhưng viết quá sơ sài → xem §4.2. **KHÔNG đề nghị xóa** — nó là TC *duy nhất* chạm 2 slot action đó; đề nghị **viết lại** (GAP-7). |
| `NEW-35`, `NEW-36` | Là **kiểm tra tĩnh trên source code** (`git diff` giữa 2 nhánh), không phải test case chạy được trên môi trường. Hợp lệ về nội dung nhưng sai tầng → `[MINOR]`, nên chuyển thành mục review code, không đếm vào coverage runtime. |

---

## 3.5 Fix-shape analysis (adversarial)

**Fix shape đọc từ `03-dev-impact.md` mục 2**: thêm cờ `hasAction`/`sendActionSuccess` vào 2 nhánh trả về sớm + đảo thứ tự ghi param vào URL trước khi redirect. Kèm bump version asset.

| Fix shape khớp | Câu hỏi adversarial | TCs trả lời được? | Kết luận |
|---|---|---|---|
| **"JS / asset / build"** (`config/sns-line.php`, `form_render_v3.js`) | F5 **thường** (không Ctrl+F5) trên browser còn cache bản cũ? Network tab có asset 404? | ⚠️ **Một nửa** — `NEW-34` làm đúng việc này nhưng **chỉ cho `form_render.blade.php` v3**. `order/detail.blade.php` v2 cũng bị sửa và cũng khai báo biến JS mới, **không có TC nào**. | **`[BLOCKER]`** — `DEPLOY-ASSET-001` ghi rõ *"Cao tuyệt đối nếu file bị sửa nằm trong luồng thanh toán / hủy hợp đồng"*. `order/detail.blade.php` **là** luồng thanh toán → GAP-2 |
| **"sửa hàm dùng chung / 共通"** (`sendAction`, `sendActionOrderItem`) | Có danh sách nơi ảnh hưởng do Dev cung cấp? TC test **từng nơi**? Chức năng tương tự đã rà? | ✅ Dev **có** list caller (mục 3, 9 dòng). ⚠️ Nhưng TC runtime chỉ có `NEW-25` (bước mua tiếp theo) + `NEW-45` (mơ hồ). `NEW-36` chỉ là diff tĩnh. Các slot `申込完了時` / `トライアル` / `決済時` / `解約時` (kho `TC-BIL-83` xác nhận 継続商品 có **7 slot**) **chưa có TC runtime**. | **`[MAJOR]`** → GAP-7 |
| **"số đếm / count"** (`count_click`, `count_action_view_page`) | Đối chiếu **4 nguồn** (summary / detail / CSV / API) + phép tính tay? | ⚠️ TCs có phép tính tay tốt (vd `NEW-2`: 3 lần F5 → `count_click = 4`, action = 1) nhưng **chỉ đọc DB**. Không TC nào mở **màn admin** xem thống kê lượt xem trang. Mà D2 làm con số này **giảm so với trước fix** → khách sẽ thấy số tụt. | **`[MAJOR]`** → GAP-6 |
| **"validate input / kiểm tra điều kiện"** (`!= 'true'`) | Cover bao nhiêu variant? Test **server-side** hay chỉ frontend? Đủ 5 pattern biên? | ✅ **Làm tốt** — `NEW-18` gọi thẳng endpoint với **10 biến thể** (`'true'`, `'TRUE'`, `'True'`, `' true '`, `'1'`, `'false'`, rỗng, không gửi, số `1`, `'yes'`), có bảng đối chiếu. Đây là TC mạnh nhất của bộ. | ✅ Đạt |
| **"concurrent / 2 tab"** (CONC-001 trigger) | Đủ 4 kịch bản CONC-001? Evidence có đếm số lần xử lý thực tế? | ⚠️ Chỉ `NEW-14` (2 tab). **Expected của nó không assert được**: *"có thể phát sinh 2 bản ghi action… chỉ báo bug nếu số action lớn hơn số tab"* → TC **không thể fail**. | **`[MAJOR]`** → §4.2 + §6 |

**Symptom-only KH report check**: **KHÔNG áp dụng** — ticket `39742` là tracker `Triển khai ngang`, không có khách báo triệu chứng, `01-bug-task.md` không có Actual/Expected. **Nhưng hệ quả ngược lại còn nặng hơn**: chuẩn "hành vi đúng" của bộ TC này **chỉ đến từ chính mô tả fix của Dev**, không có spec độc lập nào xác nhận — và chuẩn đó **đang mâu thuẫn với kho TCs** (§6).

### Anti-patterns

| AP | Dính? | Chi tiết |
|---|---|---|
| **AP-3** Happy-path-only regression | ✅ **Dính** | `T3` (Action Settings) chỉ có `NEW-21` + `NEW-45`, precondition đều là data sạch, không có edge state (action đã xóa giữa chừng, item hết hạn, bot hết hợp đồng). → `[MAJOR]` §4.2 |
| **AP-4** Specific code-check disguised as generic catch | ✅ **Dính (theo rule detect #1)** | Mục "Commit / Pull Request" của `03-dev-impact.md` = `<không có link PR>`. Chỉ có tên nhánh + commit hash, không có link review được. → `[MAJOR]` §4.2 |
| **AP-1** Single-trigger generic-fix | ❌ Không | Fix không phải generic catch; `NEW-18` đã phủ 10 trigger. |
| **AP-2** Symptom-only | ❌ Không | Không có KH report. |
| **AP-5** Layer-downstream over-coverage | ⚠️ Nhẹ | `NEW-35`, `NEW-36` test tầng source-diff thay vì code path chạy. → `[MINOR]` |
| **AP-6** Mục 3 dev-impact trống | ❌ Không | Dev đã list 9 caller, có phân biệt "sửa" / "chỉ đọc" / "đã rà không sửa". |

---

## 3.6 Bảng quan điểm đối chiếu

| Mã quan điểm | Ưu tiên | Trigger khớp? | TC cover | Exec | Kết luận |
|---|---|---|---|---|---|
| `FUNC-001` | Cao | ✅ mọi chức năng | NEW-4, 5, 6 (**cả 3 đều Normal**) | 3/3 | ⚠️ `[MAJOR]` **RULE-01** — thiếu Abnormal + Boundary, không ghi lý do |
| `FUNC-004` | Cao | ✅ có giới hạn số lần trả lời | NEW-18, NEW-31 (**cả 2 Boundary**) | 2/2 | ⚠️ `[MAJOR]` **RULE-01** — thiếu Normal + Abnormal |
| `CONC-001` | Cao | ✅ 2 tab cùng link, không có khoá server | NEW-14 (Boundary) | 1/1 | ⚠️ `[MAJOR]` — 1/4 kịch bản, **expected không assert được** |
| `DATA-DB-001` ★ | Cao (BẮT BUỘC — có UPDATE) | ✅ UPDATE `count_click`, `count_action_view_page` | **KHÔNG CÓ** | — | 🔴 **`[BLOCKER]`** → GAP-1 |
| `DATA-COUNT-001` | Cao (BẮT BUỘC — màn có số đếm) | ✅ 2 bộ đếm bị đổi hành vi | NEW-2, 3, 22, 23, 24, 29, 31 | 7/7 | ⚠️ `[MAJOR]` — chỉ tầng DB, thiếu màn admin + đối chiếu nguồn → GAP-6 |
| `DEPLOY-ASSET-001` ★ | **Cao tuyệt đối** (file trong luồng thanh toán) | ✅ bump version + sửa JS/blade | NEW-34, NEW-35 (**chỉ màn biểu mẫu**) | 2/2 | 🔴 **`[BLOCKER]`** — bỏ trống `order/detail.blade.php` v2 → GAP-2 |
| `LIFF-ENTRY-001` ★ | Cao (BẮT BUỘC — sinh URL cho LINE user) | ✅ link form + link đơn hàng | NEW-43, NEW-44 (**cả 2 Normal**) | 2/2 | 🔴 **`[BLOCKER]`** — thiếu ma trận đường vào; kho `TC-FORM-411` liệt kê **6 đường**, `TC-FORM-413` thêm dạng **LIFF** → GAP-3. Cộng `[MAJOR]` RULE-01 (thiếu Abnormal/Boundary) |
| `ENV-003` ★ | Cao (BẮT BUỘC — URL/domain + bill tiền) | ✅ | 0 TC chạy `prd` | 0 | ⚠️ `[MAJOR]` **RULE-08** → GAP-4 |
| `COMPAT-LEGACY-001` ★ | Cao (BẮT BUỘC — đối tượng đã version-up) | ✅ form v1/v2 + order v1 | NEW-32 (pass), **NEW-33 (`skip`)** | 1/2 | ⚠️ `[MAJOR]` **RULE-09** — nửa phạm vi legacy không có kết luận → GAP-5 |
| `REG-SHARED-001` | Cao | ✅ `sendAction` dùng chung | NEW-25, NEW-36 (tĩnh) | 2/2 | ⚠️ `[MAJOR]` — slot action khác chưa test runtime → GAP-7 |
| `MSG-004` | Cao | ✅ output user cuối trên LINE | **NEW-38** — nội dung ĐÚNG, nhưng gắn mã `RULE-06` (không phải mã quan điểm) | 1/1 | ⚠️ `[MAJOR]` **sai mã, không phải thiếu TC** — fix = re-tag `RULE-06` → `MSG-004`. `RISK`, không phải GAP |
| `MSG-USER-001` | Cao | ✅ tương tác friend LINE | NEW-8 (Abnormal) | 1/1 | `RISK` — 1 TC, chỉ nhánh chặn/chưa kết bạn |
| `OUT-TRUTH-001` | Cao | ✅ có thông báo kết quả gửi | NEW-21, NEW-29 (cả 2 Abnormal) | 2/2 | `RISK` — thiếu Normal |
| `STATE-001` | Cao | ✅ 2 bước ghi tuần tự (gửi action → ghi param) | NEW-11 (Abnormal) | 1/1 | `RISK` — 1 TC; đúng vùng REQ-015 |
| `REG-URL-001` ★ | Trung bình → **nâng Cao** (chạm luồng thanh toán) | ✅ thêm param vào URL | NEW-12 (Boundary) | 1/1 | ⚠️ `[MAJOR]` RULE-01 — nâng Cao thì cần đủ 3 loại case |
| `DEPLOY-LIVE-001` ★ | Cao | ✅ đổi payload API (+2 field), release không maintain | NEW-37 (Normal) | 1/1 | `RISK` — 1 TC |
| `INTG-LINE-001` | Cao | ✅ LIFF + LINE in-app browser | NEW-38, 43, 44 (in-app browser) | 3/3 | `RISK` — **nhánh `liff.init`** (khi URL không có `line_user_id`) Dev nêu ở mục 6 nhưng **không TC nào đi vào nhánh đó** → gộp GAP-3 |
| `FUNC-003` / `SEC-001` | Trung bình → Cao (field liên quan URL) | ✅ param trên URL | **NEW-10** — nội dung đúng, mã `SEC-INJECT-001` không tồn tại | 1/1 | `[MINOR]` re-tag → `FUNC-003` |
| `PAY-STATE-001` | Cao | ⚠️ chạm trang trong luồng mua, **không** đổi trạng thái giao dịch | NEW-25 (bước mua tiếp theo) | 1/1 | `RISK` — chấp nhận được, không flag riêng |
| `REG-SPEC-001` | Cao | ✅ hành vi thay đổi sau khi kho TCs đã tồn tại | **KHÔNG CÓ** | — | ⚠️ `[MAJOR]` — xung đột `TC-BIL-85` chưa ai xử lý → §6 |
| `PERM-*`, `PAY-PLAN/AMOUNT/BATCH`, `BULK-*`, `MEDIA-*`, `JOB-*`, `PERF-*`, `LIST-*`, `FRIEND-001` | — | ❌ không khớp trigger | — | — | × không áp dụng |

**Quan điểm thiếu hẳn TC**: `DATA-DB-001` (BLOCKER) · `REG-SPEC-001` (MAJOR).

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

**`[BLOCKER] GAP-1 · DATA-DB-001`** — Fix có UPDATE 2 cột bộ đếm (`user_open_formanswer.count_click`, `bot_line_user_item.count_action_view_page`) và INSERT `action_lineuser`, nhưng **không TC nào trong 41 TC kiểm phạm vi `WHERE`**. Đã grep toàn bộ file 04: **0 lần** nhắc "2 bot" / "2 tài khoản" / "bot khác" / "OA khác". Không ai chứng minh việc mở form của bot A không cộng/không chặn nhầm bộ đếm của bot B khi 2 bot có form hoặc sản phẩm trùng tên. — **Fix**: thêm GAP-1 (§5), dựng 2 bot cùng tên form/sản phẩm, đối chiếu bộ đếm từng bot trước/sau.

**`[BLOCKER] GAP-2 · DEPLOY-ASSET-001`** — `config/sns-line.php` (version asset) bị bump và **cả 2** blade đều khai báo biến JS mới, nhưng `NEW-34` (F5 thường trên cache cũ) và `NEW-35` (kiểm version ở thẻ script) **chỉ làm cho `form_render.blade.php` v3**. `resources/views/basic/sales/v2/order/detail.blade.php` — file **nằm trong luồng thanh toán** — không có TC cache asset nào. `DEPLOY-ASSET-001` quy định mức **"Cao tuyệt đối"** đúng cho trường hợp này. Rủi ro: khách còn cache blade/JS cũ mở trang mua → biến `sendActionSuccess` chưa khai báo → lỗi JS → **không mua được**. — **Fix**: GAP-2 (§5).

**`[BLOCKER] GAP-3 · LIFF-ENTRY-001 + INTG-LINE-001`** — Cơ chế chặn nằm **trong URL**, nên **mỗi đường mở link cho ra một URL khác nhau**. Bộ TC chỉ phủ 2 đường: dán link trực tiếp (NEW-1…14) và tap link trong chat LINE (NEW-43/44). Kho TCs đã ghi rõ các đường còn lại là hợp lệ: `TC-FORM-411` — *"mở form được từ đủ **6 đường**: link trực tiếp, template button, image map, rich menu, chat 1:1, quét QR"*; `TC-FORM-413` — link form dạng **LIFF** `https://liff.line.me/<liffId>?unique_key=<key>`. Dev cũng xác nhận ở mục 6 có nhánh `liff.init` khi URL **không có** `line_user_id` — **không TC nào đi vào nhánh này**. Rủi ro: trên LIFF, `history.replaceState` có thể không giữ được param → action gửi lại mỗi lần, tức **bug gốc vẫn còn nguyên trên đường vào phổ biến nhất**. — **Fix**: GAP-3 (§5).

### 4.2 Major (nên fix)

**`[MAJOR] RULE-08 / ENV-003` (GAP-4)** — 0/41 TC chạy `prd`. Task chạm **bill tiền** + **URL/domain** + **asset sau release** — cả 3 đều nằm trong danh mục RULE-08 cấm kết luận từ staging. — **Fix**: chạy tối thiểu bộ GAP-4 trên production.

**`[MAJOR] NEW-33 · COMPAT-LEGACY-001 / RULE-09` (GAP-5)** — TC màn chi tiết đơn hàng **bản cũ** đang `skip` (staging, `2026-09-03 10:40`), không ghi lý do skip. Màn cũ bị loại khỏi phạm vi sửa **có chủ đích**, nên đây đúng là chỗ phải chứng minh "không đổi gì" — mà lại là TC duy nhất không có kết luận. RULE-09 không cho đánh × chỉ vì nhánh mới chạy ổn. — **Fix**: chạy lại `NEW-33`, hoặc ghi lý do skip + Leader approve.

**`[MAJOR] Tác giả TC` (mục 0.6 #5)** — 38/41 TC (92,7%) do **AI sinh**, `reviewed=false`, `reviewState=leader`. Bộ TC chưa qua duyệt người. — **Fix**: Leader duyệt trên Studio rồi set `reviewed`.

**`[MAJOR] 21/41 TC mang mã quan điểm không tồn tại`** — 10 mã lạ (`TOOL-*`, `API-CONTRACT-001`, `API-001`, `SEC-INJECT-001`, `RULE-06`, 1 TC trống mã). Hơn nửa bộ TC **không map được coverage** bằng `framework/checklist-lme.md`. — **Fix**: re-tag trên Studio. Đề xuất ánh xạ: `RULE-06`→`MSG-004` · `SEC-INJECT-001`→`FUNC-003` · `API-CONTRACT-001`/`API-001`→`FUNC-001` · `TOOL-OLDREC-001`→`COMPAT-LEGACY-001` · `TOOL-AXIS-001`→`FUNC-001` · `TOOL-NEGCTRL-001`→`OUT-TRUTH-001` · `TOOL-KNOW-002`→`FUNC-001` · `TOOL-ERRHYG-001`→`FUNC-002`.

**`[MAJOR] NEW-14 · Expected không assert được`** — Kết quả mong đợi ghi *"có thể phát sinh 2 bản ghi action… Kết quả cần ghi số thực tế vào báo cáo; chỉ báo bug nếu số action lớn hơn số tab"* → TC **không thể fail**, và đang được tick `pass`. Vi phạm mục 4a #4 (expected phải đo lường được). — **Fix**: Leader chốt ngưỡng chấp nhận (§6), rồi viết lại expected thành số cụ thể.

**`[MAJOR] NEW-45 · TC không đủ chất lượng làm bằng chứng`** — Vi phạm **4/10** mục rà chất lượng: `Điều kiện tiền đề` **rỗng** (#2), `Các bước thực hiện` chỉ 2 dòng *"User trả lời form nhiều lần / User mua sản phẩm nhiều lần"* — không dựng lại được (#3), `Kết quả mong đợi` = *"Action được cho user theo đúng setting của form và item"* — không đo lường được (#4), thiếu `Mã quan điểm` + `Loại case` + `screen` (#1). Đang tick `pass` trên staging. — **Fix**: viết lại theo GAP-7. **Không xóa** — là TC duy nhất chạm 2 slot action đó.

**`[MAJOR] NEW-43 / NEW-44 · Expected 2 nhánh nên không thể fail`** — Cả 2 TC (do người viết) có expected dạng *"nếu setting 1 lần ⇒ không gửi lại; nếu setting nhiều lần ⇒ gửi lại"*. Đã bao trọn 2 kết quả đối nghịch → chạy kiểu gì cũng `pass`. — **Fix**: tách thành 2 TC, mỗi TC 1 setting + 1 expected xác định.

**`[MAJOR] GAP-6 · DATA-COUNT-001`** — Bộ đếm `count_action_view_page` **đổi hành vi** (D2: chỉ tăng khi action thật sự gửi → số thống kê **thấp hơn trước fix** với cùng lượng truy cập). Không TC nào mở **màn admin** để xem con số khách nhìn thấy; chỉ đọc DB. Spec xác nhận cột này là *"★ Bộ đếm slot 「商品ページ表示時」"* (`bill-item/db/db-mapping.md:454`) và tham gia logic `稼働回数`. — **Fix**: GAP-6 (§5). Song song: hỏi PM có cần thông báo khách về việc số liệu tụt.

**`[MAJOR] GAP-7 · REG-SHARED-001 + [AP-3]`** — `sendAction`/`sendActionOrderItem` là hàm **dùng chung**; kho `TC-BIL-83` xác nhận 継続商品 có **7 slot action** (`商品ページ表示時`, `申込完了時`, `トライアル`, `初回決済時`, `2回目以降決済時`, `決済エラー発生時`, `解約時`). Release này chỉ đụng slot đầu, nhưng chỉ có `NEW-25` test runtime 1 nhánh + `NEW-45` mơ hồ. Regression cho `T3` toàn happy-path, không có edge state (**AP-3**). — **Fix**: GAP-7 (§5).

**`[MAJOR] [AP-4] Không có link PR`** — `03-dev-impact.md` mục "Commit / Pull Request" = `<không có link PR>`, chỉ có nhánh `ai_fixbug_39742` + commit `afe26df872`. Không review được fix shape thực tế; đặc biệt **`config/sns-line.php` bị sửa mà mục 2 và 3 không giải thích**. — **Fix**: yêu cầu Dev đưa link diff.

**`[MAJOR] Auto-fill chưa được tester verify`** — `01-bug-task.md` và `03-dev-impact.md` đều có `Auto-filled: 2026-09-03 by /new-task` nhưng checkbox **"Tester verify auto-fill chính xác" CHƯA tick** ở cả 2 file. F/D/T có thể thiếu hoặc map sai → toàn bộ coverage matrix ở §3 dựa trên input chưa ai xác nhận. — **Fix**: tester đọc lại Redmine #39742 (journal 129308) và tick.

**`[MAJOR] RULE-01` — 4 quan điểm ưu tiên Cao thiếu loại case, không ghi lý do**: `FUNC-001` (3 TC đều Normal) · `FUNC-004` (2 TC đều Boundary) · `LIFF-ENTRY-001` (2 TC đều Normal) · `REG-URL-001` (1 Boundary, đã nâng Cao). — **Fix**: bổ sung theo §5, hoặc ghi lý do vào `Ghi chú`.

**`[MAJOR] REG-SPEC-001`** — Hành vi sau fix **mâu thuẫn kho TCs `TC-BIL-85`** (§6). Không TC nào trong bộ 41 xử lý việc TC cũ đã lỗi thời. — **Fix**: xem §6.

### 4.3 Minor (có thể fix sau)

- **`[MINOR]` `NEW-35`, `NEW-36` là kiểm tra tĩnh source code**, không phải TC chạy được trên môi trường (`[AP-5]` nhẹ). Nên chuyển sang mục code-review, không tính vào coverage runtime.
- **`[MINOR]` `NEW-10` gắn mã `SEC-INJECT-001`** (không tồn tại) → đổi sang `FUNC-003`.
- **`[MINOR]` `NEW-45` thiếu `TC No.` theo format** `TC-<mã quan điểm bỏ gạch>-<nn>` vì không có mã quan điểm.
- **`[MINOR] RULE-02`** — cột `Evidence thực tế` **rỗng ở toàn bộ 41 TC** (`testcase_list` không trả về). Không kiểm chứng được các kết quả `pass` có kèm bằng chứng đúng loại hay không. Riêng bug #40150 thì **có** evidence đầy đủ (`trace.zip` + `.webm`).

### 4.4 Nit (gợi ý)

- **`[NIT]`** `temp_id` nhảy cóc: có `NEW-1…38`, `NEW-43…45`, thiếu `NEW-39…42`. Nếu là TC bị xóa giữa chừng thì nên ghi lý do vào lịch sử task.
- **`[NIT]`** Nên gộp `NEW-35`/`NEW-36` thành 1 mục "pre-merge code check" thay vì 2 TC riêng.

---

## 4.5 TC trùng lặp nội dung

**Đã rà toàn bộ 41 TC theo 4 yếu tố** (`mã quan điểm` × `loại case` × `đối tượng + thao tác` × `tiền đề tương đương`). Kết quả: **không có `DUP-EXACT`, không có `DUP-INFLATE`, không có `DUP-CONFLICT`**. Phát hiện **1 cặp chồng lấn một phần**:

| Nhóm trùng | TC giữ lại | TC đề nghị xóa/gộp | Loại trùng | 4 yếu tố trùng nhau | Severity |
|---|---|---|---|---|---|
| Mở lại link gốc trang đơn hàng lần 2 | **`NEW-29`** (`OUT-TRUTH-001`, Abnormal) — expected xác định: sản phẩm `1度のみ` ⇒ không gửi action | `NEW-44` (`LIFF-ENTRY-001`, Normal, người viết) — **GỘP, KHÔNG XÓA** | `DUP-SUBSET` một phần | Cùng đối tượng (trang chi tiết đơn hàng v2) · cùng thao tác (đóng trang → mở lại **link gốc sạch**) · tiền đề tương đương (LINE user đã kết bạn, sản phẩm có action mở trang). **Khác**: `NEW-29` chỉ nhánh `1度のみ`; `NEW-44` gộp cả 2 nhánh vào 1 expected | `[MINOR]` |

**Gate trước khi đề nghị**: giả định xóa `NEW-44` → `LIFF-ENTRY-001` chỉ còn `NEW-43` (màn biểu mẫu), **mất hoàn toàn cover LIFF cho màn bill tiền** → theo quy tắc "không xóa TC duy nhất cover một quan điểm", đổi đề xuất từ **xóa** sang **gộp/tách**: giữ `NEW-44`, tách expected 2 nhánh của nó thành 2 TC xác định (trùng với issue `[MAJOR] NEW-43/NEW-44` ở §4.2), nhánh `1度のみ` dẫn chiếu `NEW-29` thay vì lặp lại.

> ⚠️ **Không tự xóa/sửa TC nào** — TC Studio là read-only. Thao tác thật do human thực hiện trên Studio (`testcase_update` / `testcase_delete`).

---

## 5. TCs đề xuất bổ sung

**Đã đối chiếu 41 TC ở BƯỚC 0 + `kho-tcs/fa011-taobieumau-フォーム作成.md` + `kho-tcs/fa026-billtienitem-商品販売.md` — không TC đề xuất nào trùng.**
Chi tiết đối chiếu kho: `TC-FORM-411` (6 đường mở form) và `TC-FORM-413` (link LIFF) → dùng làm **nguồn vùng regression** cho GAP-3, không copy lại. `TC-BIL-84`/`TC-BIL-85` (`稼働回数`) → **conflict expected**, đẩy sang §6, **không** viết TC theo bên nào. `TC-BIL-82`/`TC-BIL-83` (số slot action) → nguồn cho GAP-7.

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-DATADB001-01 | Data | DATA-DB-001 | Action khi mở page — phạm vi dữ liệu theo bot | Normal | manual | product | Mở form của bot A không làm đổi bộ đếm và bản ghi action của bot B khi 2 bot có form trùng tên | - Có 2 bot A và B cùng plan, cùng 1 tài khoản quản trị truy cập được cả 2<br>- Mỗi bot tạo 1 form v3 **trùng tên** `39742-FORM-SCOPE`, đều gắn action gửi tin ở mục khi mở page, kiểu gửi 「毎回」<br>- Mỗi bot có 1 LINE user test riêng đã kết bạn, chưa từng mở form này | 1. Ghi lại số bản ghi action và số lượt mở form hiện có của **cả 2 bot** (màn lịch sử action của từng bot)<br>2. LINE user của bot A mở link form của bot A, chờ hiển thị xong<br>3. F5 lại 3 lần trên chính tab đó<br>4. Mở màn lịch sử action của **bot A** — đếm bản ghi action mới<br>5. Mở màn lịch sử action của **bot B** — đếm bản ghi action mới<br>6. Đối chiếu số lượt mở form của cả 2 bot với số ghi ở bước 1 | 2 bot × 1 form trùng tên `39742-FORM-SCOPE` · 1 lần mở + 3 lần F5 | - Bot A: đúng **1** bản ghi action mới; số lượt mở form tăng thành **4**<br>- Bot B: **0** bản ghi action mới; số lượt mở form **không đổi** so với bước 1<br>- Không có bản ghi nào của bot A xuất hiện trong màn lịch sử của bot B và ngược lại |  | Lấp GAP-1 / cover impact D1, D2, D3 · Đánh giá spec: Spec không ghi (đã hỏi Dev qua điểm nghi vấn #2 file 03) · Evidence: ảnh chụp màn lịch sử action của **cả 2 bot** trước và sau · RULE-07 (verify DB + màn hình) |
| TC-DATADB001-02 | Data | DATA-DB-001 | Action khi mở page — phạm vi dữ liệu theo bot | Abnormal | manual | product | Đổi bot đang chọn giữa chừng rồi mở lại form không làm bộ đếm ghi nhầm sang bot vừa chuyển sang | - Như TC-DATADB001-01<br>- Tài khoản quản trị đang mở màn quản lý của bot A | 1. Ghi lại bộ đếm của cả 2 bot<br>2. LINE user của bot A mở link form bot A lần đầu<br>3. Trên màn quản trị, dùng chức năng đổi bot sang bot B<br>4. LINE user của bot A F5 lại trang form (link vẫn của bot A)<br>5. Đọc lại bộ đếm và lịch sử action của cả 2 bot | Đổi bot ở màn quản trị giữa 2 lần mở trang phía LINE user | - Bộ đếm và bản ghi action vẫn thuộc **bot A**, không bị ghi sang bot B<br>- Việc đổi bot ở màn quản trị không ảnh hưởng trang phía LINE user đang mở |  | Lấp GAP-1 / cover impact D2 · Đánh giá spec: Spec không ghi (đã hỏi Dev) · Evidence: ảnh 2 màn lịch sử action · regression |
| TC-DEPLOYASSET001-03 | API | DEPLOY-ASSET-001 | Nạp asset sau release — trang chi tiết đơn hàng v2 | Normal | manual | product | Browser còn cache bản trước release, chỉ F5 thường vẫn nạp đúng JS mới của trang bill tiền và không lỗi JS | - Sản phẩm bản mới `39742-ITEM-A` có cấu hình action ở slot 「商品ページ表示時」, 稼働回数 =「何度でも」<br>- Trước khi deploy: mở trang chi tiết đơn hàng của sản phẩm này bằng LINE user test để browser cache asset bản cũ<br>- Sau đó deploy bản có fix lên môi trường test | 1. Sau khi deploy xong, quay lại **đúng browser đã cache** ở tiền đề<br>2. Bấm **F5 thường** (KHÔNG Ctrl+F5, KHÔNG xoá cache)<br>3. Mở tab Network, lọc JS/CSS — đọc tham số version trên các asset của trang<br>4. Mở tab Console kiểm tra lỗi JavaScript<br>5. Đọc URL trên thanh địa chỉ<br>6. Bấm nút mua/đăng ký để xác nhận bước tiếp theo vẫn chạy | 1 lần F5 thường trên browser còn cache bản trước release | - Network: asset của trang chi tiết đơn hàng nạp đúng **version mới**, không có request nào 404<br>- Console: **không** có lỗi JavaScript (đặc biệt không có lỗi biến `sendActionSuccess` chưa khai báo)<br>- URL được thêm `sendActionSuccess=true` như bản mới<br>- Nút mua/đăng ký bấm được, sang đúng bước tiếp theo |  | Lấp GAP-2 / cover impact F4, F7 · Đánh giá spec: Spec ghi rõ — `bill-item/web/logic-spec.md:143` · Evidence: ảnh tab Network (cột version asset) + ảnh Console trống lỗi · **RULE-08 → bắt buộc product**: file blade nằm trong luồng thanh toán |
| TC-DEPLOYASSET001-04 | API | DEPLOY-ASSET-001 | Nạp asset sau release — trang chi tiết đơn hàng v2 | Abnormal | manual | product | Tab trang đơn hàng mở TRƯỚC release, thao tác mua sau khi release xong vẫn không lỗi | - Như TC-DEPLOYASSET001-03<br>- Có 1 tab trang chi tiết đơn hàng đã mở từ trước lúc deploy và **không** đóng, **không** reload | 1. Deploy bản có fix trong khi tab vẫn mở<br>2. Quay lại tab cũ (đang chạy JS bản trước release)<br>3. Bấm nút mua/đăng ký<br>4. Quan sát kết quả và Console<br>5. Kiểm tra lịch sử action của LINE user | Tab mở trước release, thao tác sau release | - Thao tác mua **không** lỗi 500, **không** lỗi JavaScript<br>- Hoặc chạy đúng, hoặc hiển thị thông báo yêu cầu tải lại trang — **không** được im lặng thất bại<br>- Không phát sinh bản ghi action trùng |  | Lấp GAP-2 / cover impact F4, F7 · Đánh giá spec: Spec không ghi (đã hỏi Dev) · Evidence: video thao tác + ảnh Console · dẫn từ quan điểm DEPLOY-LIVE-001 (release không maintain) |
| TC-LIFFENTRY001-03 | UI | LIFF-ENTRY-001 | Đường mở form — ma trận entry point | Normal | manual | product | Form mở từ đủ 6 đường vào: hành vi gửi action và ghi param trên URL được ghi nhận cho từng đường | - Form v3 `39742-FORM-ENTRY` có action gửi tin ở mục khi mở page, kiểu gửi 「毎回」<br>- Đã setting mở form này ở: template button, image map, rich menu<br>- Đã tạo mã QR trỏ tới form<br>- LINE user test đã kết bạn, chưa từng mở form này<br>- Chuẩn bị bảng ghi 6 dòng để điền kết quả từng đường | 1. Mở form bằng **link trực tiếp** dán vào browser → đọc URL sau khi trang hiển thị, đếm tin action nhận được<br>2. Đóng trang. Mở form bằng **template button** trong chat → lặp việc đọc URL + đếm tin<br>3. Lặp với **image map**<br>4. Lặp với **rich menu**<br>5. Lặp với **link gửi ở chat 1:1**<br>6. Lặp với **quét mã QR**<br>7. Với mỗi đường: sau khi trang hiển thị xong, bấm F5 **1 lần** rồi đếm lại số tin action<br>8. Điền bảng 6 dòng: đường vào → URL có param hay không → số tin lần đầu → số tin sau F5 | 6 đường mở × form `39742-FORM-ENTRY` | Với **cả 6 đường**: lần mở đầu nhận đúng **1** tin action; sau khi trang hiển thị xong URL **có** `sendActionSuccess=true`; bấm F5 **không** phát sinh tin thứ 2. Nếu có đường nào URL không nhận được param (⇒ F5 sinh thêm tin) thì ghi rõ đường đó vào bảng và **báo bug** — đó chính là bug gốc còn sót |  | Lấp GAP-3 / cover impact T1, F5 · Đánh giá spec: Spec ghi rõ — dẫn từ `TC-FORM-411` (kho FA-011, 6 đường mở form) · Evidence: bảng 6 dòng + ảnh URL của từng đường + ảnh chat đếm tin · **RULE-08 → product** (domain/URL) |
| TC-LIFFENTRY001-04 | UI | LIFF-ENTRY-001 | Đường mở form — link dạng LIFF | Abnormal | manual | product | Form mở bằng link LIFF (URL không có mã người dùng) — nhánh liff.init vẫn chặn được lần gửi thứ 2 | - Form v3 `39742-FORM-LIFF` có action gửi tin ở mục khi mở page, kiểu gửi 「毎回」<br>- Tạo template có chèn code form để hệ thống thay thành link LIFF `https://liff.line.me/<liffId>?unique_key=<key>`<br>- LINE user test đã kết bạn, chưa từng mở form này | 1. Gửi template chứa code form cho LINE user test<br>2. Trên LINE app thật, tap link LIFF trong tin nhắn → chờ form hiển thị xong<br>3. Đếm số tin action nhận được trong chat<br>4. Đọc URL hiện tại trong webview LIFF<br>5. Kéo xuống rồi kéo lên để trigger reload trong webview (hoặc bấm reload nếu webview có)<br>6. Đếm lại số tin action | Link LIFF dạng `https://liff.line.me/<liffId>?unique_key=<key>` — **không** có mã người dùng trên URL | - Lần mở đầu: form hiển thị, nhận đúng **1** tin action<br>- URL trong webview được ghi param `sendActionSuccess=true`<br>- Reload trong webview: **không** phát sinh tin action thứ 2<br>- Nếu param không ghi được vào URL LIFF ⇒ ghi rõ hiện trạng và **báo bug**: nhánh `liff.init` chưa được fix |  | Lấp GAP-3 / cover impact T1, F5 · Đánh giá spec: Spec không ghi (đã hỏi Dev — mục 6 file 03 nêu 2 điểm gọi `openFormanswer` loại trừ nhau nhưng chỉ verify tĩnh) · Evidence: video quay màn LINE app + ảnh URL webview · dẫn từ `TC-FORM-413` (kho FA-011) |
| TC-ENV003-01 | API | ENV-003 | Xác nhận trên production | Normal | manual | product | Bộ nghiệp vụ lõi của cả 2 màn chạy đúng trên production (không kết luận từ staging) | - Đã deploy bản fix lên production<br>- Trên production: 1 form v3 và 1 sản phẩm bản mới, đều có action gửi tin ở mục khi mở page, kiểu gửi 「毎回」<br>- 1 LINE user thật đã kết bạn với OA production | 1. Mở link form trên production bằng LINE app thật → đếm tin action, đọc URL<br>2. F5 3 lần → đếm lại tin action<br>3. Mở link trang chi tiết đơn hàng trên production → đếm tin action, đọc URL<br>4. F5 3 lần → đếm lại tin action<br>5. Đối chiếu bộ đếm lượt xem trang ở màn quản trị production trước/sau | 1 form + 1 sản phẩm trên production, mỗi màn 1 lần mở + 3 lần F5 | - Cả 2 màn: nhận đúng **1** tin action cho lần mở đầu, 3 lần F5 không sinh tin thêm<br>- URL cả 2 màn đều được thêm `sendActionSuccess=true`<br>- Bộ đếm lượt xem trang tăng đúng theo số lần action **thật sự** được gửi |  | Lấp GAP-4 / cover impact BUG, T1, T2 · Đánh giá spec: Spec ghi rõ · Evidence: ảnh chat LINE thật + ảnh URL + ảnh màn quản trị · **RULE-08** — bill tiền + domain, bắt buộc production |
| TC-COMPATLEGACY001-03 | Data | COMPAT-LEGACY-001 | Màn bản cũ — chi tiết đơn hàng v1 | Normal | manual | product | Trang chi tiết đơn hàng bản cũ giữ nguyên hành vi gửi action sau release (thay TC đang skip) | - Có 1 sản phẩm thuộc **bản cũ** (`is_product_new = 0`) `39742-ITEM-OLD` có cấu hình action khi mở trang<br>- LINE user test có mã người dùng hợp lệ<br>- Ghi lại số bản ghi action và bộ đếm lượt xem của user–sản phẩm này trước khi test | 1. Mở link chi tiết đơn hàng **bản cũ** kèm mã người dùng LINE test<br>2. Đọc URL trên thanh địa chỉ<br>3. Mở Console kiểm tra lỗi JavaScript<br>4. Bấm F5 **2 lần**<br>5. Đọc lại số bản ghi action và bộ đếm lượt xem ở màn quản trị<br>6. So với hành vi ghi nhận **trước release** (nếu chưa có, ghi nhận làm mốc và nêu rõ) | Sản phẩm bản cũ `39742-ITEM-OLD`, 1 lần mở + 2 lần F5 | - Trang mở bình thường, hiển thị đúng thông tin sản phẩm, **không** lỗi JavaScript<br>- URL **KHÔNG** bị thêm `sendActionSuccess`<br>- Hành vi gửi action **giữ nguyên như trước release** (mỗi lần mở vẫn gửi) — ghi số thực tế, **không** báo bug vì màn cũ gửi lại<br>- Bộ đếm lượt xem tăng theo đúng cách cũ |  | Lấp GAP-5 / cover impact F9, T2 · Thay cho `NEW-33` đang `skip` · Đánh giá spec: Spec ghi rõ — Dev loại màn cũ khỏi phạm vi có chủ đích (file 03 mục 3 dòng 8) · Evidence: ảnh URL + ảnh Console + ảnh màn quản trị · **RULE-09** · regression |
| TC-DATACOUNT001-01 | Data | DATA-COUNT-001 | Thống kê lượt xem trang sản phẩm — màn quản trị | Normal | manual | product | Số lượt xem trang trên màn quản trị khớp với số action thật sự được gửi sau fix | - Sản phẩm bản mới `39742-ITEM-COUNT`, slot 「商品ページ表示時」 có action gửi tin, 稼働回数 =「何度でも」<br>- LINE user test chưa từng mở trang này<br>- Ghi lại giá trị hiển thị ở màn quản trị: số lượt xem trang của user–sản phẩm này (mốc = N) | 1. LINE user mở trang chi tiết đơn hàng lần đầu, chờ hiển thị xong<br>2. F5 **4 lần** trên chính tab đó<br>3. Đóng tab, tap lại **link gốc sạch** từ tin nhắn 1 lần<br>4. Mở màn quản trị → đọc số lượt xem trang của user–sản phẩm<br>5. Mở màn lịch sử action → đếm bản ghi action của user–sản phẩm<br>6. Đếm số tin action user nhận được trong chat LINE<br>7. Đối chiếu 3 con số ở bước 4, 5, 6 với phép tính tay | 1 lần mở + 4 lần F5 + 1 lần mở lại link gốc. **Phép tính tay**: action thật sự gửi = 2 (lần mở đầu + lần mở link gốc sạch) ⇒ số lượt xem trang kỳ vọng = N + 2 | - Màn quản trị: số lượt xem trang = **N + 2** (KHÔNG phải N + 6)<br>- Màn lịch sử action: đúng **2** bản ghi mới<br>- Chat LINE: user nhận đúng **2** tin<br>- **3 nguồn khớp nhau** và khớp phép tính tay |  | Lấp GAP-6 / cover impact D2, T2 · Đánh giá spec: Spec ghi rõ — `bill-item/db/db-mapping.md:454` (cột là bộ đếm slot 商品ページ表示時) + `logic-spec.md:143` (chỉ +1 khi gửi thành công) · Evidence: ảnh 3 màn + bảng phép tính tay · ⚠️ Con số này **thấp hơn trước fix** — xác nhận với PM trước khi kết luận Đạt |
| TC-DATACOUNT001-02 | Data | DATA-COUNT-001 | Thống kê lượt xem trang sản phẩm — màn quản trị | Boundary | manual | staging | Sản phẩm cấu hình 稼働回数「1度のみ」: bộ đếm lượt xem có tăng ở lần mở thứ 2 trở đi hay không | - Sản phẩm bản mới `39742-ITEM-ONCE`, slot 「商品ページ表示時」 có action, 稼働回数 =「1度のみ」<br>- LINE user test chưa từng mở trang này<br>- Ghi mốc số lượt xem trang = N | 1. LINE user mở trang lần đầu → đếm tin action<br>2. Đóng tab, tap lại link gốc sạch **2 lần nữa**<br>3. Mỗi lần đọc lại số lượt xem trang ở màn quản trị<br>4. Đếm tổng tin action nhận được<br>5. Lập bảng: lần mở → có gửi action không → số lượt xem sau mỗi lần | Sản phẩm `1度のみ`, 3 lần mở từ link gốc sạch | - Chỉ lần mở đầu gửi action (1 tin)<br>- Lần 2 và 3: **không** gửi action<br>- Số lượt xem trang: ghi số thực tế cho từng lần. **Nếu bộ đếm vẫn tăng ở lần 2, 3 dù không gửi action** ⇒ trái với D2 trong `03-dev-impact.md` ("chỉ còn tăng khi action thật sự được gửi") ⇒ báo lên Leader, **không tự kết luận Đạt** |  | Lấp GAP-6 / cover impact D2 · Đánh giá spec: **Spec không ghi rõ** — `REQ-015` của Studio đã nêu đúng khoảng hở này nhưng chưa ai chốt · Evidence: bảng 3 dòng + ảnh màn quản trị từng lần · liên quan §6 mục 2 |
| TC-REGSHARED001-03 | UI | REG-SHARED-001 | Slot action khác của sản phẩm — regression hàm dùng chung | Normal | manual | product | 6 slot action còn lại của 継続商品 vẫn gửi bình thường sau khi thêm param vào URL | - 継続商品 `39742-ITEM-CONT` đã gắn action gửi tin **khác nhau, dễ phân biệt** ở đủ 6 slot còn lại: `申込完了時`, `トライアル`, `初回決済時`, `2回目以降決済時`, `決済エラー発生時`, `解約時`<br>- Bot đã liên kết cổng thanh toán ở môi trường test<br>- LINE user test đã kết bạn | 1. LINE user mở trang chi tiết đơn hàng (URL bị thêm param) rồi hoàn tất đăng ký mua → đếm tin của slot `申込完了時`<br>2. Chạy tới mốc trial → đếm tin slot `トライアル`<br>3. Chạy thanh toán lần đầu → đếm tin slot `初回決済時`<br>4. Chạy thanh toán chu kỳ tiếp theo → đếm tin slot `2回目以降決済時`<br>5. Dựng 1 lần thanh toán lỗi → đếm tin slot `決済エラー発生時`<br>6. Hủy hợp đồng → đếm tin slot `解約時`<br>7. Lập bảng 6 dòng: slot → có nhận tin không → nội dung có đúng slot không | 継続商品 với đủ 6 slot action, mỗi slot 1 nội dung tin riêng | Cả **6 slot** đều gửi đúng **1** tin đúng nội dung của slot đó, đúng thời điểm. Việc URL trang chi tiết đơn hàng bị thêm `sendActionSuccess=true` **không** chặn nhầm bất kỳ slot nào trong 6 slot này (param chỉ được dùng cho slot `商品ページ表示時`) |  | Lấp GAP-7 / cover impact F8, T3 · Thay cho `NEW-45` viết quá sơ sài · Đánh giá spec: Spec ghi rõ — dẫn từ `TC-BIL-83` (kho FA-026: 継続商品 có đúng 7 slot) · Evidence: bảng 6 dòng + ảnh chat LINE · **RULE-08 → product** (bill tiền) · regression |
| TC-REGSHARED001-04 | UI | REG-SHARED-001 | Slot action khác — edge state | Abnormal | manual | staging | Action của slot `商品ページ表示時` đã bị xóa giữa chừng — các slot còn lại không bị ảnh hưởng và trang không lỗi | - Sản phẩm `39742-ITEM-DEL` có action ở slot `商品ページ表示時` **và** slot `申込完了時`<br>- LINE user test đã mở trang 1 lần (URL đã có param) | 1. Ở màn quản trị, **xóa** action đang gắn ở slot `商品ページ表示時`<br>2. LINE user mở lại trang bằng link gốc sạch<br>3. Quan sát trang có lỗi không, đọc URL<br>4. Đếm tin action nhận được<br>5. Hoàn tất đăng ký mua → đếm tin slot `申込完了時` | Action slot `商品ページ表示時` bị xóa sau khi user đã mở trang 1 lần | - Trang mở bình thường, **không** lỗi 500, **không** lỗi JavaScript<br>- **Không** gửi tin của slot `商品ページ表示時` (action đã xóa)<br>- URL **không** bị thêm param (vì không có action nào được gửi)<br>- Slot `申込完了時` vẫn gửi **đúng 1** tin bình thường |  | Lấp GAP-7 / cover impact F8, T3 · Vá **AP-3** (regression có edge state) · Đánh giá spec: Spec ghi rõ — dẫn từ `TC-FORM-67`/`TC-FORM-68` (kho FA-011: copy form khi action đã xóa) · Evidence: ảnh URL + ảnh Console + ảnh chat |
| TC-FUNC001-04 | UI | FUNC-001 | 2 nhánh giới hạn trả lời của biểu mẫu | Abnormal | manual | staging | Biểu mẫu đạt giới hạn **và** URL chuyển hướng trỏ tới địa chỉ lỗi — cờ vẫn được ghi trước khi chuyển hướng | - Biểu mẫu v3 `39742-FORM-E`: action gửi tin ở mục khi mở page kiểu 「毎回」; bật giới hạn tổng số câu trả lời = 1 và đã có 1 câu trả lời (đạt giới hạn); bật URL chuyển hướng, **trỏ tới một địa chỉ không tồn tại**<br>- LINE user test chưa từng mở biểu mẫu này | 1. Mở link biểu mẫu của LINE user test<br>2. Chờ trang cố chuyển hướng sang địa chỉ lỗi<br>3. Bấm Back quay lại trang biểu mẫu<br>4. Đọc URL trên thanh địa chỉ<br>5. Đếm bản ghi action ở màn lịch sử action<br>6. F5 lại 1 lần rồi đếm lại | Biểu mẫu đạt giới hạn, URL chuyển hướng trỏ tới địa chỉ không tồn tại | - Dù đích chuyển hướng lỗi, khi Back về thì URL trang biểu mẫu **đã có** `sendActionSuccess=true`<br>- Tổng bản ghi action vẫn đúng **1**<br>- F5 sau đó **không** sinh action thứ 2 |  | Lấp GAP-8 / cover impact F1, F5 · Vá RULE-01 cho `FUNC-001` (đang thiếu Abnormal) · Đánh giá spec: Spec ghi rõ — file 03 mục 2 (ghi param TRƯỚC khi xử lý nhánh) · Evidence: video thao tác + ảnh URL sau khi Back |
| TC-FUNC001-05 | UI | FUNC-001 | 2 nhánh giới hạn trả lời của biểu mẫu | Boundary | manual | staging | Biểu mẫu ở đúng lần trả lời cuối cùng trước khi chạm giới hạn — cờ ghi đúng ở cả lần trong hạn và lần vượt hạn | - Biểu mẫu v3 `39742-FORM-F`: action gửi tin kiểu 「毎回」; giới hạn số lần trả lời theo người = 2; LINE user test đã trả lời **1** lần | 1. LINE user mở biểu mẫu (lần trong hạn cuối cùng) → đọc URL, đếm tin action<br>2. Trả lời và submit → xác nhận lưu được<br>3. Mở lại biểu mẫu bằng link gốc sạch (giờ đã vượt hạn) → quan sát màn hình, đọc URL, đếm tin action<br>4. F5 1 lần → đếm lại tin action | Giới hạn 2 lần/người, user đang ở lần thứ 2 rồi vượt sang lần thứ 3 | - Lần trong hạn: form hiển thị đủ câu hỏi, nhận **1** tin action, URL có `sendActionSuccess=true`<br>- Lần vượt hạn: hiện đúng thông báo/chuyển hướng đã cấu hình, URL **vẫn** được ghi cờ, nhận **1** tin action cho lần mở đó<br>- F5 sau lần vượt hạn: **không** sinh tin thêm |  | Lấp GAP-8 / cover impact F1 · Vá RULE-01 cho `FUNC-001` (đang thiếu Boundary) · Đánh giá spec: Spec ghi rõ — `form-answer/feature-spec.md:145` (EP-38 `action_open_type`) · Evidence: ảnh 2 trạng thái màn hình + ảnh URL + ảnh chat |
| TC-CONC001-02 | API | CONC-001 | Mở đồng thời — mức chặn trùng | Boundary | manual | product | Mở đồng thời N tab từ cùng link sạch: số action sinh ra không vượt quá số tab (chốt ngưỡng chấp nhận) | - Biểu mẫu v3 `39742-FORM-CONC`, action gửi tin kiểu 「毎回」<br>- LINE user test chưa từng mở biểu mẫu này<br>- **Leader đã chốt ngưỡng chấp nhận** (xem §6 mục 2) trước khi chạy TC này | 1. Chuẩn bị 5 tab cùng dán link gốc sạch<br>2. Tải cả 5 tab **đồng thời** (mở nhanh liên tiếp trong <1 giây)<br>3. Chờ cả 5 tab hiển thị xong<br>4. Đọc URL của từng tab<br>5. Đếm bản ghi action ở màn lịch sử action<br>6. Đếm tin action user nhận trong chat LINE | 5 tab mở đồng thời từ 1 link gốc sạch | - Số bản ghi action **≤ 5** (không vượt số tab) và **khớp** số tin user nhận<br>- Mỗi tab tự ghi `sendActionSuccess=true` vào URL của chính nó<br>- Đối chiếu với ngưỡng Leader đã chốt: vượt ngưỡng ⇒ **báo bug**, không ghi "ghi nhận số thực tế" rồi cho Đạt |  | Lấp GAP-9 / cover impact BUG, D3 · Thay expected không assert được của `NEW-14` · Đánh giá spec: **Spec không ghi** — `REQ-015` nêu khoảng hở, cần Leader chốt (§6 mục 2) · Evidence: ảnh 5 URL + ảnh màn lịch sử action + ảnh chat · **RULE-08 → product** (race) |

**Tổng: 15 TC đề xuất** — lấp 9 GAP. Phân bố loại case: Normal 7 · Abnormal 5 · Boundary 3.

### Sync log — đã push lên MCP LME TEST STUDIO (`2026-09-03`)

Human chỉ định loại 4 TC, push **11/15** vào **task #171** qua `testcase_create` (`client_ref` = `ID` → idempotent).

| ID (client_ref) | Studio `temp_id` | Studio `id` | GAP |
|---|---|---|---|
| `TC-DATADB001-01` | NEW-46 | 15651 | GAP-1 |
| `TC-LIFFENTRY001-03` | NEW-47 | 15652 | GAP-3 |
| `TC-LIFFENTRY001-04` | NEW-48 | 15653 | GAP-3 |
| `TC-ENV003-01` | NEW-49 | 15654 | GAP-4 |
| `TC-DATACOUNT001-01` | NEW-50 | 15655 | GAP-6 |
| `TC-DATACOUNT001-02` | NEW-51 | 15656 | GAP-6 |
| `TC-REGSHARED001-03` | NEW-52 | 15657 | GAP-7 |
| `TC-REGSHARED001-04` | NEW-53 | 15658 | GAP-7 |
| `TC-FUNC001-04` | NEW-54 | 15659 | GAP-8 |
| `TC-FUNC001-05` | NEW-55 | 15660 | GAP-8 |
| `TC-CONC001-02` | NEW-56 | 15661 | GAP-9 |

**KHÔNG push (human loại)** — 4 TC vẫn giữ trong report này để Leader cân nhắc lại sau:

| ID | GAP | Hệ quả nếu bỏ hẳn |
|---|---|---|
| `TC-DATADB001-02` | GAP-1 | GAP-1 còn `TC-DATADB001-01` cover → vẫn đóng được BLOCKER, mất nhánh "đổi bot giữa chừng" |
| `TC-DEPLOYASSET001-03` | GAP-2 | ⚠️ **GAP-2 hiện KHÔNG còn TC nào** → `[BLOCKER]` §4.1 **vẫn mở** |
| `TC-DEPLOYASSET001-04` | GAP-2 | ⚠️ như trên |
| `TC-COMPATLEGACY001-03` | GAP-5 | GAP-5 quay về phụ thuộc `NEW-33` — đang `skip` → `[MAJOR]` §4.2 **vẫn mở** |

⚠️ Sau khi thêm 11 TC: task `#171` có **52 TC**, `untested = 11`, và **`aiResult` chuyển từ `pass` → `null`** (kết luận AI của task bị vô hiệu cho tới khi chạy bộ mới). `toolWritten.rate` 92,7% → 73,1%.

---

## 6. Spec update needed

### 1. 🔴 Xung đột expected với kho TCs — `TC-BIL-85` (FA-026)

| | Nội dung |
|---|---|
| **Kho TCs nói** | `TC-BIL-85` — *"稼働回数 =「何度でも」→ **bắn action mỗi lần mở trang**"*. Steps: *"F2 mở 商品ページ **3 lần liên tiếp**"*. Expected: *"F2 nhận đúng **3 tin nhắn** (mỗi lần mở 1 tin)"*. Nguồn: `r70「mỗi lần user click mở link sẽ action」` |
| **Hành vi sau fix** | `NEW-23` (Studio) — mở trang rồi tải lại: **chỉ 1 tin**, các lần sau bị chặn bởi `sendActionSuccess=true` trên URL |
| **Vì sao mâu thuẫn** | `TC-BIL-85` không phân biệt *"mở lại bằng F5/reload trên cùng tab"* với *"tap lại link gốc sạch"*. Sau fix, 2 việc này cho kết quả **khác nhau**: F5 ⇒ 1 tin; tap link gốc ⇒ vẫn 3 tin. Chạy `TC-BIL-85` nguyên văn sau release sẽ **fail** nếu tester dùng F5 |
| **Cần chốt** | (a) `何度でも` sau fix nghĩa là *"mỗi lần **điều hướng mới** tới trang"* hay *"mỗi lần **trang được render**"*? (b) `TC-BIL-85` trong kho phải sửa lại như thế nào? |
| **KHÔNG tự chọn bên** | Đây là thay đổi hành vi nghiệp vụ khách nhìn thấy được (số tin nhận ít đi), không phải chi tiết kỹ thuật. Leader + Dev + PM chốt. |

### 2. 🔴 Ngưỡng chấp nhận cho mở đồng thời / mở lại link gốc (`REQ-015`)

Studio `REQ-015` đã **ghi nhận sẵn** 4 khoảng hở của cơ chế chặn bằng param URL: mất kết nối giữa lúc gửi action và lúc ghi param · mở song song 2 tab từ link chưa có param · URL có fragment (`#` — đã thành bug #40150) · bộ đếm vẫn tăng khi item cấu hình chỉ gửi lần đầu.

`NEW-14` viết expected là *"ghi nhận số thực tế… chỉ báo bug nếu số action lớn hơn số tab"* → **không có chuẩn để đánh giá**, TC không thể fail. **Cần Leader chốt**: mở đồng thời N tab từ link sạch thì **bao nhiêu action là chấp nhận được**? (1 — cần khoá phía server / N — chấp nhận theo thiết kế hiện tại). Chốt xong mới chạy `TC-CONC001-02`.

### 3. ⚠️ Mâu thuẫn nội bộ trong `03-dev-impact.md` mục 2 vs mục 3

Mục 2 viết *"**Không đụng phần bán hàng (bill tiền)** vì trang đó không có nhánh trả về sớm tương tự"*, nhưng mục 3 và 4.1 lại liệt kê `SalesManagementV2Controller::orderDetail` + `order/detail.blade.php` là **có sửa**. Bộ TC (`NEW-22`…`NEW-31`) cho thấy bill tiền **có** được port cách fix. Cần Dev sửa lại câu chữ để tránh reviewer vòng sau hiểu nhầm phạm vi.

### 4. ⚠️ `config/sns-line.php` bị sửa nhưng không được giải thích

File nằm trong 7 file thay đổi nhưng **không xuất hiện ở mục 2 lẫn mục 3** của `03-dev-impact.md`. `NEW-35` suy đoán đây là bump version asset. Cần Dev xác nhận chính thức — vì nó quyết định GAP-2 phải test những asset nào.

### 5. ⚠️ Hành vi "mở lại link gốc từ chat LINE" chưa được chốt là đúng hay sai

`03-dev-impact.md` mục 2 nêu kịch bản chính của bug là *"rất hay gặp: **mở lại link biểu mẫu từ lịch sử chat LINE**"*. Nhưng `NEW-43` (người viết) kết luận: tap lại link gốc từ tin nhắn ⇒ với setting `毎回` **vẫn gửi lại action**, và `NEW-38` ghi trong note rằng *"nhận thêm 1 tin cho mỗi lần mở link mới là **đúng thiết kế**"*.

⇒ **Kịch bản Dev nêu là động cơ chính của fix lại chính là kịch bản fix KHÔNG xử lý** (vì `history.replaceState` chỉ đổi URL của tab hiện tại, link trong tin nhắn vẫn sạch). Cần chốt: fix này có được coi là **đã giải quyết** khiếu nại gốc không, hay chỉ giảm tần suất? Nếu khách phàn nàn vì mở lại link từ chat, fix hiện tại **chưa đủ**.

---

> **Draft cho Leader verify** — không phải kết luận cuối. Mọi TC ở §5 cần Leader duyệt trước khi member đưa lên Studio/Sheet.
> TC Studio là **read-only** trong repo; mọi sửa/xóa thực hiện trên Studio (`testcase_update` / `testcase_delete`).
