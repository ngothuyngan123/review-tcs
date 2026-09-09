# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | `#39040 — [Upload image][Profile bot] Không hiển thị thông báo lỗi khi OA thực hiện upload ảnh cho bot vượt dung lượng tối đa` |
| Reviewer (Leader) | `<tên — Leader fill>` |
| Tester được review | **AI Studio** (12/13 TC, job #615) + `haodtb@mcp` (1/13 TC) |
| Ngày review | `2026-08-26` |
| Version TCs | Studio `round = 1`, `status = done-ai`, `reviewState = leader` |
| Vòng review | `Round 1` |

---

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | **(1) MCP LME TEST STUDIO — task #202** |
| Vì sao không dùng nguồn ưu tiên cao hơn | N.A. — dùng nguồn 1 (ưu tiên cao nhất). `task_list(ticket_id=39040)` trả về đúng 1 task chưa archived, `round = 1`. |
| Ticket · task_id · round · branch | `39040` · `#202` · `round 1` · `ai_fixbug_39040` |
| Thời điểm fetch | `2026-08-26` (`testcase_list` + `task_get_context` + `task_get_report`) |
| Tổng số TC review | **13** |
| Snapshot đã ghi | `04-tc-list.md` — đã có sẵn snapshot cùng nguồn (`<!-- source: MCP LME TEST STUDIO — task_id=202 ... fetch lúc 2026-08-26 -->`, do `/new-task` sinh cùng ngày, cùng payload) → **không cần refresh, giữ nguyên** |
| Đối chiếu chéo nguồn | **KHÔNG** — đã dừng ở nguồn 1 |
| Metadata task | `aiResult = pass` · `openBugs = 0` · `reviewed = false` · `submittedWithoutMcp = false` · `toolWritten: tool 12 / mcp 1 / human 0` |

### Cảnh báo bắt buộc về chất lượng nguồn (Nguồn 1 — Studio)

| # | Chiều | Kết quả | Flag |
|---|---|---|---|
| 1 | Kết quả thực thi thật | **13/13 hiện là `Đạt` (100%)** — nhưng đây là trạng thái *sau khi chạy tay lại*. Auto-run #486 (`pipeline`, 2026-08-25) thực chất **status = `fail`: 7 pass / 0 fail / 4 `error`**. 4 TC `error` (#12826, #12849, #12850, #12851) được `haodtb` chạy tay lại ngày 2026-08-26 → pass. | `OK` về tỷ lệ · nhưng xem #2 |
| 2 | TC `fail`/`error` + ticket bug | 0 TC `fail`, **4 TC `error` ở auto-run**, 0 bug ticket. Không TC nào cần raise ticket (triage xác định là lỗi hạ tầng env test, không phải bug sản phẩm). ⚠️ **Nhưng 3/4 TC error (#12849/12850/12851) có triage ghi rõ *"save-success bất khả thi trong env test"*** — kết quả manual pass sau đó không có evidence để chứng minh đã vượt được rào đó. | `[MAJOR]` → §4.2 M4 |
| 3 | Môi trường đã chạy — RULE-08 / ENV-003 | **PROD 0 · STAGING 0 · DEV 0 · LOCAL 13** (`envAuto` xác nhận `dev/staging/prd` đều 0 run). Task chạm **media (upload / lưu / resize ảnh)**. | `[MAJOR] RULE-08 / ENV-003` → §4.2 M1 |
| 4 | Ai chạy (`last_exec.source` / `by`) | AI `pipeline` **7 TC** · QA người `haodtb` **6 TC**. ⚠️ **Cả 4 requirement `risk = High` (REQ-001, REQ-002, REQ-005, REQ-006) đều CHỈ được verify bởi AI pipeline**, không có QA người chạy lại. | `[MAJOR]` → §4.2 M8 |
| 5 | Tác giả TC (`provenance.source`) | **AI 12/13 (92%)** · human (`haodtb@mcp`) **1/13**. `reviewState = leader` (chưa `done`). | `[MAJOR]` → §4.2 M9 |
| 6 | Mã quan điểm KHÔNG có trong `checklist-lme.md` | **2 mã / 4 lượt TC**: `TOOL-KNOW-002` (2 TC), `TOOL-VAL2-001` (2 TC). Đã grep cả `checklist-lme.md` lẫn `catalog-lme.md` — không có. | `[MAJOR]` → §4.2 M6. **4 TC này KHÔNG được tính là cover quan điểm** ở §3 / §7 F.1 |

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED**

**Lý do ngắn gọn**: Có 2 `[BLOCKER]` — (1) **mức giới hạn 2MB chưa được chốt trong spec**, mà toàn bộ 13 TC đều hard-code `2MB` + chuỗi 「2MB以下のをアップしてください。」 trong `Kết quả mong đợi`; (2) spec `bot-edit` **BR-15** ghi rõ ảnh bot còn một **đường ghi thứ hai — clone từ URL (`link_of_image`)** — không TC nào cover và không nằm trong mục 3 của `03-dev-impact.md`, nên bug gốc "ảnh >2MB được lưu im lặng" vẫn có thể tái hiện qua đường này.

---

## 2. Tóm tắt cho member

Bộ TC này có **cấu trúc rất tốt cho một bug validate**: tách đủ 3 điểm biên (2097151 / 2097152 / 2097153), có TC **bypass JS gọi thẳng server** cho **cả 2 màn** (mới `/admin/setting-bot` + cũ `/admin/bot-edit`), có TC **đối chứng âm** (xóa ảnh, đổi tên bot không kèm ảnh) để bắt lỗi "chặn oan", và có TC cache asset sau release. Đây đúng là các chiều mà một fix đổi ngưỡng cần.

Hai điểm phải xử lý trước khi nghiệm thu: **mức 2MB chưa có trong spec** (`spec-features/admin/bot-edit/feature-spec.md` BR-12~BR-15 **không ghi giới hạn dung lượng nào**, và Dev cũng ghi spec sprint #34620 UP-07 bỏ ngỏ mục này) — nếu PM chốt con số khác thì `Kết quả mong đợi` của cả 13 TC đều sai; và **đường clone ảnh từ URL (`link_of_image`)** ghi vào cùng trường `bots.bot_image` nhưng chưa có TC nào chạm tới.

Ngoài ra: **toàn bộ 13 TC chạy ở `env = local`** trong khi đây là task media (RULE-08 bắt buộc production), và **6 kết quả chạy tay đều không đính evidence** (RULE-02) — hai điểm này làm kết quả "13/13 Đạt" chưa đủ điều kiện nghiệm thu.

---

## 3. Coverage Matrix

| Impact | Loại | Priority | TCs map | # TC | Exec | Status |
|---|---|---|---|---|---|---|
| **BUG** — màn mới `/admin/setting-bot` đặt limit 10MB thay vì 2MB; auto-save ngay khi chọn file → ảnh 2–10MB lưu im lặng, không báo lỗi | Fix | — | TC-TOOLKNOW002-01 (5MB reject), TC-FUNC004-03 (2MB+1 reject), TC-TOOLVAL2001-01 (bypass JS → server reject) | 3 | 3/3 pass | **RISK** — reproduce đúng flow KH ✔, nhưng chỉ chạy `local` + chỉ AI pipeline chạy; và **đường `link_of_image` chưa cover** (xem BLOCKER-2) |
| **F1** — `SettingBotController@update` (server màn mới) | Function | Direct | TC-TOOLVAL2001-01 (reject path), TC-FUNC004-01 / TC-FUNC004-02 (accept path) | 3 | 3/3 pass | **RISK** — nhánh `image` file đã cover; nhánh **`link_of_image` clone URL chưa xác nhận có tồn tại trên màn mới hay không** |
| **F2** — `onAvatarSelected` / `saveImageImmediately` (`setting-bot.js`) | Function | Direct | TC-TOOLKNOW002-01, TC-FUNC001-01, TC-FUNC004-01, TC-FUNC004-02, TC-FUNC004-03, TC-REGSHARED001-01 | 6 | 6/6 pass | **OK** — đủ chiều accept / reject / biên / đối chứng âm (xóa ảnh) |
| **F3** — `BotController@botChange` (server màn cũ) | Function | Direct | TC-TOOLVAL2001-02 (reject ✔), TC-FUNC001-02 / TC-FUNC004-04 / TC-REGSHARED001-02 (accept — **chưa verify được**) | 4 | 4/4 "pass" | **RISK** — nhánh **reject** đã verify thật; nhánh **accept (lưu thành công)** bị `api.line.me` OAuth chặn ở auto-run, manual pass không evidence → xem M4 |
| **F4** — `readURL` (`public/js/admin/bot.js`, JS màn cũ) | Function | Direct | TC-TOOLKNOW002-02 (alert + `inputCleared=true` + `previewUnchanged=true`) | 1 | 1/1 pass | **OK** — verify đúng hành vi mới (xóa file input sau reject) |
| **F5** — `ChangeBotController@store`, `change_bot.js`, `change_new_bot.js`, `olioa.js` (màn thêm / đổi tài khoản) | Function | Indirect — Dev để **ngoài phạm vi** | — | **0** | — | **GAP** — Dev xác nhận các màn này **hoàn toàn không kiểm dung lượng** → §4.2 M5 |
| **D1** — không có data bị update | Data | — | N.A. — Dev ghi "chỉ siết bước kiểm tra đầu vào, không đổi cấu trúc hay dữ liệu đã lưu"; không migrate, không recover | — | — | **N.A.** ✔ (đã đối chiếu: `bots.bot_image` + `bots_profiles.avt_path` là ghi của luồng save sẵn có, fix không đổi logic ghi) |
| **T1** — LOA Connection Settings (**FA-038**) — chặn ảnh >2MB + báo lỗi, ở **cả màn mới lẫn màn cũ** | Feature | Medium | 12/13 TC (trừ TC-DEPLOYASSET001-01) | 12 | 12/12 "pass" | **RISK** — cover cả 2 màn (điểm mạnh, thỏa COMPAT-LEGACY-001) nhưng: 0 TC production, nhánh accept màn cũ chưa verify, thiếu biến thể input (0 byte / sai định dạng / >10MB / pixel lớn) |
| **T2** — Màn thêm / đổi tài khoản (`change_bot` / `change_new_bot` / `olioa`) | Feature | `<Dev không đánh giá>` | — | **0** | — | **GAP** → §4.2 M5 |
| **Asset JS** (`setting-bot.js`, `bot.js` bị sửa → release có đổi asset) | Deploy | — | TC-DEPLOYASSET001-01 | 1 | 1/1 "pass" **nhưng sai env** | **RISK** — TC khai `env_scope = ["staging"]` + note "cần release thật", lại đánh Đạt ở `local` → §4.2 M3 |

### ORPHAN TCs

**Không có ORPHAN.** Đã trace từng TC trong 13 TC về code path Dev đã sửa (F1–F4) hoặc về asset JS bị đổi — mọi TC đều nằm trong phạm vi fix. Không phát hiện TC test layer downstream không bị chạm code (AP-5 **không dính**).

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| Fix shape (mục 2 dev-impact) | **Validation** (chính) + **Upload / media** + **Asset JS** + **Shared code** — 4 shape cùng khớp |
| KH report dạng | **Có root cause cụ thể** — KH nêu rõ steps, expected message và giá trị ngưỡng. **Không** phải symptom-only → không cần cover alternative root cause |
| Anti-patterns dính | **AP-3** (happy-path-only regression) · **AP-4** (một phần) · Không dính AP-1, AP-2, AP-5, AP-6 |

### Shape 1 — **Validation** ("hạ giới hạn… sửa cả phần kiểm tra phía JS lẫn phía server")

| Câu hỏi adversarial | Trả lời từ bộ TC hiện tại | Kết luận |
|---|---|---|
| Có test **server-side** (gọi thẳng API bỏ qua JS) không? | **CÓ** — TC-TOOLVAL2001-01 (`POST /admin/ajax/setting-bot/update`) + TC-TOOLVAL2001-02 (`POST /admin/bot-save`), cả 2 pass với response `success:false` đúng chuỗi | ✔ **Đạt** — đây là điểm mạnh nhất của bộ TC |
| Đủ **5 pattern biên** (biên / biên−1 / biên+1 / 0 / rỗng)? | biên `2097152` ✔ · biên−1 `2097151` ✔ · biên+1 `2097153` ✔ · **0 byte ✗** · **file rỗng / không chọn file** — có gián tiếp qua TC-REGSHARED001-02 (save không kèm ảnh) | ⚠️ **Thiếu 0 byte** → M10 |
| Cover bao nhiêu **input variant**? | Chỉ **JPEG/PNG hợp lệ, dung lượng khác nhau**. **Không có**: file sai định dạng (.gif/.webp/.pdf), MIME type lạ, file đổi đuôi, ảnh pixel rất lớn nhưng nhẹ, ảnh >10MB (trên cả ngưỡng cũ) | ⚠️ `[MAJOR]` → M10, M11 |
| Đủ **luồng vào** (create / edit / copy / import / API)? | **edit ✔** (cả 2 màn) · **create ✗** (thêm bot mới — F5) · **clone từ URL (`link_of_image`) ✗** — spec BR-15 ghi rõ đường này tồn tại | 🚨 `[BLOCKER]` → BLOCKER-2 · `[MAJOR]` → M5 |

### Shape 2 — **Upload / media / ảnh**

| Câu hỏi adversarial | Trả lời | Kết luận |
|---|---|---|
| Có TC chạy **production** không? (media staging ≠ production; ảnh sync lên B2 `p.lmes.jp`) | **KHÔNG** — 13/13 chạy `local` | `[MAJOR] RULE-08 / ENV-003` → M1 |
| Test **resize 2048px** / chặn **10.000px** (Catalog E `MED-L10`)? | **KHÔNG** — Studio coverage tự báo `BR-13` (resize max 2048px) `level = none`. ⚠️ Sắc hơn: **không TC nào gửi ảnh pixel lớn nhiều-MB thẳng tới server (bypass JS)** — TC API chỉ dùng đúng `2097153 bytes`. Nếu server kiểm size **sau** bước resize thì ảnh 5MB resize xuống <2MB sẽ lọt; TC-TOOLKNOW002-01 (5MB) không phát hiện được vì **bị JS chặn trước** (`update_requests=0`) | `[MAJOR]` → M11 |
| Verify **file cũ bị xóa thật** (404 kèm `?v=x`, cả local và `p.lmes.jp`)? | **KHÔNG** — chức năng có thay/xóa ảnh nhưng không TC nào kiểm | `[MINOR]` → M13 (fix không chạm cleanup — Leader quyết, xem lý do ở §4.3) |
| **PNG nền trong suốt** giữ alpha? | **KHÔNG** có TC | `[MINOR]` → M10 |

### Shape 3 — **Asset JS** (`setting-bot.js`, `bot.js` bị sửa)

| Câu hỏi adversarial | Trả lời | Kết luận |
|---|---|---|
| Test **F5 thường** (không Ctrl+F5) trên browser còn cache bản cũ? | **CÓ TC** (TC-DEPLOYASSET001-01) — nội dung TC viết đúng chuẩn DEPLOY-ASSET-001. **Nhưng chạy ở `local`**, trái với `env_scope=["staging"]` và trái với chính note của TC ("cần release thật; không kiểm được ở local build đơn lẻ") | `[MAJOR]` — kết quả **vô hiệu** → M3 |
| Network tab: asset trả **200 với query version mới**, không 404? | Không có trong Expected của TC | `[MINOR]` → M3 |

### Shape 4 — **Shared code** (`BotController@botChange` dùng chung cho save ảnh / đổi tên / đổi `channel_secret`)

| Câu hỏi adversarial | Trả lời | Kết luận |
|---|---|---|
| Có **danh sách nơi ảnh hưởng do DEV cung cấp**? | **CÓ** — `03-dev-impact.md` mục 3 liệt kê 4 function + mục 2 nêu yokoten F5. **Không dính AP-6** | ✔ Không BLOCKER |
| TC test **từng nơi** trong danh sách? | F1 ✔ · F2 ✔ · F3 ✔ (một phần) · F4 ✔ · **F5 ✗** | `[MAJOR]` → M5 |
| Nhánh dùng chung **không bị chặn oan**? | Đổi tên bot ✔ (TC-REGSHARED001-02) · Xóa ảnh ✔ (TC-REGSHARED001-01) · **Đổi `channel_secret` ✗** — REQ-007 của Studio ghi rõ nhánh này nhưng không TC nào cover | `[MAJOR]` → M7b |

### Anti-pattern dính

- **[AP-3] Happy-path-only regression** — T1 có TC nhưng mọi precondition đều là "bot sạch, ảnh hợp lệ"; T2 (F5) **0 TC**. Không có TC regression ở trạng thái edge (bot chưa có ảnh, bot free plan, bot chưa kết nối LOA).
- **[AP-4] (một phần)** — mục "Commit / Pull Request" **không có link PR**, chỉ có branch `ai_fixbug_39040` + commit `5c33646743`. Fix shape ở đây là đổi hằng số nên rủi ro thấp → hạ xuống `[NIT]`, nhưng cần branch để Leader tự đối chiếu điểm đặt check size **trước hay sau bước resize** (liên quan trực tiếp M11).

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- **[BLOCKER] SPEC — GAP-0: Mức giới hạn 2MB chưa được chốt ở bất kỳ spec nào, nhưng 13/13 TC đều hard-code nó vào `Kết quả mong đợi`.**
  Bằng chứng: (a) `spec-features/admin/bot-edit/feature-spec.md` §5.4 **BR-12 ~ BR-15** mô tả path ảnh, resize 2048px, xóa ảnh, clone URL — **không có dòng nào về giới hạn dung lượng**; (b) `spec-features/admin/bot-edit/web/api-spec.md` EP-02: param `image` cột **Validation = `—`** (trống); (c) `framework/catalog-lme.md` Khối E1 có `MED-L01`…`MED-L10` cho chat / friend info / template / richmenu nhưng **không có dòng nào cho ảnh đại diện bot**; (d) chính Dev ghi *"Sprint spec #34620 (`screens/unclear-points.md` UP-07) bỏ ngỏ giới hạn dung lượng ảnh đại diện"* và *"mức 2MB cần PM xác nhận"*; (e) `spec_status = null` ở **toàn bộ 13 TC** → không TC nào khai `Spec ghi rõ` / `Đã hỏi leader`.
  → **Đề xuất fix**: chốt với PM mức giới hạn chính thức + chuỗi thông báo trước khi chạy lại; sau khi chốt, set `spec_status` cho 13 TC (`Spec ghi rõ` hoặc `Đã hỏi leader` + tên người chốt); bổ sung dòng `MED-L11 | Profile bot (ảnh đại diện LOA) | Ảnh | 2MB` vào `framework/catalog-lme.md` Khối E1 và một BR mới vào `feature-spec.md` §5.4 (xem §6).
  ⚠️ Nếu PM chốt con số khác 2MB → **toàn bộ 13 TC phải sửa Expected**, kết quả "13/13 Đạt" hiện tại mất giá trị.

- **[BLOCKER] FIX-SHAPE — GAP-1: Đường ghi ảnh thứ hai (`link_of_image` — clone ảnh từ URL) không được fix chạm tới và không TC nào cover.**
  Bằng chứng: `feature-spec.md` **BR-15** — *"Ảnh có thể upload trực tiếp (file) hoặc clone từ URL (`link_of_image`)"*; `web/logic-spec.md` bước **8. XỬ LÝ ẢNH**: `a. url_image == '/images/camera.png' → xóa` · **`b. Nếu link_of_image → grab_image() clone từ URL`** · `c. Nếu image file upload → Image::make() → resize`. Tức nhánh **8b (clone URL)** và **8c (file upload)** là **2 nhánh song song ghi vào cùng `bots.bot_image`**. `api-spec.md` EP-02 xác nhận `link_of_image` là param hợp lệ và có mã lỗi riêng (`'cannot clone this image'`).
  Mục 2 + mục 3 của `03-dev-impact.md` chỉ nói tới "kiểm tra phía JS khi chọn file" và "phía server khi lưu ảnh" — **không nhắc `link_of_image`/`grab_image`**. Nếu check 2MB chỉ đặt ở nhánh 8c, thì **bug gốc "ảnh >2MB được lưu im lặng, không báo lỗi" vẫn tái hiện nguyên vẹn qua nhánh 8b**.
  → **Đề xuất fix**: (1) hỏi Dev xác nhận `grab_image()` có bị chặn 2MB không, và màn mới `/admin/setting-bot` có nhận `link_of_image` không; (2) bổ sung TC **TC-FUNC004-05** (§5) trước khi nghiệm thu; (3) nếu nhánh này thật sự không được chặn → yêu cầu Dev fix bổ sung trong cùng ticket, **không tách ticket** (cùng root cause, cùng trường dữ liệu).

### 4.2 Major (nên fix)

- **[MAJOR] M1 — RULE-08 / ENV-003: 13/13 TC chạy ở `env = local`, 0 TC production, trong khi đây là task media.**
  `envAuto` của Studio xác nhận `dev = 0 run · staging = 0 run · prd = 0 run`. Catalog D: production dùng **media server riêng qua `p.lmes.jp`**, ảnh lưu tạm ~1 ngày rồi **sync lên B2**; `ENV-003` ghi rõ *"Media có update BẮT BUỘC check trên production"*.
  → **Fix**: chạy lại tối thiểu bộ core (TC-TOOLKNOW002-01, TC-FUNC004-01, TC-FUNC004-03, TC-TOOLVAL2001-01, TC-FUNC001-01) trên **PRODUCTION**, kèm evidence là URL ảnh sau lưu (kiểm cả link local lẫn `p.lmes.jp`). Xem thêm **TC-ENV003-01** ở §5.

- **[MAJOR] M2 — RULE-02: 6/6 kết quả chạy tay không có evidence.**
  `task_get_report` mục `manual.results`: cả 6 bản ghi (`id` 4437, 4438, 4453, 4463, 4464, 4465) đều có `actual = null` và `evidence = []`. Trong đó **4 bản ghi là để "cứu" TC vừa `error` ở auto-run** → đây chính là nhóm cần bằng chứng nhất.
  → **Fix**: đính screenshot/video cho 6 TC này (toast + ảnh đại diện sau thao tác + giá trị `bots.bot_image`) rồi mới tick Đạt.

- **[MAJOR] M3 — TC-DEPLOYASSET001-01 chạy sai môi trường → kết quả vô hiệu.**
  TC khai `env_scope = ["staging"]`, `exec_mode = manual`, `env_tag = read-only`, note ghi *"cần release thật để tái hiện cache asset; không kiểm được ở local build đơn lẻ"* — nhưng được đánh **Đạt ở `env = local`**. `DEPLOY-ASSET-001` là quan điểm ★ ưu tiên **Cao**, trigger bắt buộc vì release này sửa 2 file JS.
  → **Fix**: chạy lại **sau khi release lên staging/production**, chỉ **F5 thường** (không Ctrl+F5); bổ sung vào Expected: DevTools > Network trả **200 với query version mới**, không có 404.

- **[MAJOR] M4 — 3 TC nhánh "lưu thành công" của màn cũ chưa thực sự được verify.**
  TC-FUNC001-02 (#12849), TC-FUNC004-04 (#12850), TC-REGSHARED001-02 (#12851) đều `error` ở auto-run #486. Triage ghi: *"`botChange` gọi `api.line.me` OAuth vô điều kiện với channel credentials giả của bot test ⇒ luôn 「入力した情報が間違っています」 ⇒ **save-success bất khả thi trong env test**"*. Runner chỉ xác nhận được `jsAccepted=true` / `gatePassed=true` / `not2mb=true` — tức **"2MB-gate không chặn oan"**, **KHÔNG** phải "ảnh được lưu thành công". Manual pass sau đó không có evidence nên không rõ đã dùng bot có credentials thật chưa.
  Hệ quả: **REQ-005 và REQ-007 mới cover được một nửa** (nhánh không-bị-chặn-oan), nửa còn lại (lưu thật, `bots.bot_image` đổi) chưa có bằng chứng.
  → **Fix**: chạy lại 3 TC này với **bot có `channel_secret` / `channel_access_token` THẬT** để vượt bước OAuth, kèm evidence `bots.bot_image` trước/sau.

- **[MAJOR] M5 — F5 / T2 (màn thêm & đổi tài khoản) có 0 TC, dù Dev đã tự nêu là không kiểm dung lượng.**
  Mục 2 `03-dev-impact.md`: *"Yokoten: các màn thêm/đổi tài khoản (`change_bot.js` / `change_new_bot.js` / `olioa.js` + `ChangeBotController@store`) **hoàn toàn không kiểm dung lượng** nhưng khác phạm vi ticket."* → cùng trường `bots.bot_image`, cùng lớp bug, đã được Dev xác nhận là đang hở.
  `REG-SHARED-001` (Cao) yêu cầu *"TC test **từng nơi** trong danh sách nơi ảnh hưởng do DEV cung cấp"* — danh sách có 5 mục, TC cover 4.
  → **Fix**: Leader chốt 1 trong 2 — (a) đưa vào phạm vi ticket này (thêm **TC-REGSHARED001-03** ở §5), hoặc (b) raise **ticket riêng** và ghi quyết định vào report. **Không để trống không quyết.**

- **[MAJOR] M6 — 4/13 TC (31%) mang mã quan điểm ngoài `framework/checklist-lme.md` → không tính là cover.**
  `TOOL-KNOW-002` (TC-TOOLKNOW002-01, TC-TOOLKNOW002-02) và `TOOL-VAL2-001` (TC-TOOLVAL2001-01, TC-TOOLVAL2001-02) — đã grep, không có trong `checklist-lme.md` lẫn `catalog-lme.md`. Đây là mã nội bộ Studio.
  ⚠️ Hệ quả nặng: 4 TC này chính là các TC **verify trực tiếp bug fix** và **server-side bypass** — về nội dung thì rất tốt, nhưng vì mã lạ nên coverage của các quan điểm chuẩn bị **hụt trên giấy** (xem M7).
  → **Fix**: remap trên Studio (`testcase_update`) — `TOOL-KNOW-002` → **`FUNC-004`** (giới hạn dung lượng, Abnormal) hoặc **`MEDIA-001`**; `TOOL-VAL2-001` → **`FUNC-004`** (ghi thêm "server-side, bypass FE" ở `note`). Sau remap, `TC No.` đổi theo quy ước `TC-FUNC004-<nn>`.

- **[MAJOR] M7 — RULE-01: 3 quan điểm ưu tiên Cao không đủ 3 loại case, không ghi lý do.**
  - `FUNC-001` (Cao): 2 TC — **Normal ×2**, thiếu Abnormal + Boundary.
  - `FUNC-004` (Cao): 4 TC — **Boundary ×4**, thiếu Normal + Abnormal.
  - `REG-SHARED-001` (Cao): 2 TC — **Normal ×2**, thiếu Abnormal + Boundary.
  Về **hành vi** thì bộ TC đã có đủ cả 3 chiều — chỉ là bị **rải sang mã quan điểm khác** (phần Abnormal nằm ở `TOOL-KNOW-002`/`TOOL-VAL2-001`). Đây chủ yếu là **lỗi gắn mã**, không phải thiếu test thật.
  → **Fix**: xử lý **cùng lúc với M6** — sau khi remap 4 TC `TOOL-*` về `FUNC-004`, `FUNC-004` sẽ có đủ Abnormal + Boundary; bổ sung 1 Normal cho `FUNC-004` (ảnh hợp lệ được chấp nhận qua đúng đường giới hạn) hoặc ghi lý do ở `Ghi chú`.

- **[MAJOR] M7b — REQ-007 thiếu nhánh `channel_secret`.**
  Requirement Studio REQ-007 ghi: *"Bấm 「保存」 không kèm ảnh / **đổi tên bot** / **đổi `channel_secret`** trên màn cũ vẫn lưu thành công"*. TC-REGSHARED001-02 chỉ cover **đổi tên bot**. Nhánh `channel_secret` quan trọng vì nó kích hoạt LINE OAuth + có thể tạo lại LIFF app (BR-08 ~ BR-11) — nếu check 2MB đặt sai vị trí trong `botChange` thì nhánh này có thể bị chặn oan.
  → **Fix**: bổ sung **TC-REGSHARED001-04** (§5).

- **[MAJOR] M8 — Cả 4 requirement `risk = High` chỉ được AI pipeline verify, không có QA người chạy lại.**
  REQ-001 → TC-TOOLKNOW002-01 (`by = pipeline`) · REQ-002 → TC-TOOLVAL2001-01 (`pipeline`) · REQ-005 → TC-TOOLKNOW002-02 (`pipeline`) · REQ-006 → TC-TOOLVAL2001-02 (`pipeline`). 6 TC do người chạy đều rơi vào nhóm risk Medium/Low.
  → **Fix**: QA người chạy lại 4 TC này, kèm evidence (đây cũng là 4 TC bắt buộc chạy production theo M1).

- **[MAJOR] M9 — 12/13 TC (92%) do AI sinh, `reviewState = leader` (chưa `done`), `reviewed = false`.**
  Chỉ TC-FUNC004-02 (Studio #12879) có `provenance.source = human`. Lưu ý phân biệt: `toolWritten.human = 0` **không** có nghĩa "không ai viết" — đó là **kênh ghi** (MCP), tác giả thật đọc ở `provenance.source`.
  → **Fix**: report này chính là vòng review Leader đang cần; sau khi xử lý §4.1 + §4.2, chuyển `reviewState` → `done`.

- **[MAJOR] M10 — FUNC-003 / MEDIA-001: thiếu biến thể input, chỉ test ảnh hợp lệ khác dung lượng.**
  Không có TC cho: **file 0 byte** · **file sai định dạng** (.gif / .webp / .pdf — đối chiếu tiền lệ `TC-RM-89` ở `kho-tcs/fa004`) · **file đổi đuôi / MIME lạ** (ảnh chụp từ điện thoại, Google Drive, máy scan — `MEDIA-001` yêu cầu bộ file **đa nguồn thật**) · **PNG nền trong suốt** giữ alpha · **ảnh >10MB** (trên cả ngưỡng cũ) để chắc chắn message hiển thị là 「2MB以下…」 chứ không phải chuỗi 10MB cũ còn sót.
  → **Fix**: bổ sung **TC-FUNC003-01**, **TC-FUNC004-06** (§5).

- **[MAJOR] M11 — MEDIA-IMG-001 / BR-13: không TC nào phân biệt được check size chạy TRƯỚC hay SAU bước resize 2048px.**
  Studio coverage tự báo `BR-13` (resize max 2048px) `level = none`, `BR-12` `level = none`. Sâu hơn: 2 TC API (`TC-TOOLVAL2001-01/02`) chỉ dùng đúng `2097153 bytes` — file nhỏ, pixel nhỏ, **không kích hoạt bước resize**. TC dùng ảnh 5MB (`TC-TOOLKNOW002-01`) thì **bị JS chặn trước khi gửi** (`update_requests=0`), nên **server chưa bao giờ nhận một file vừa nhiều-MB vừa pixel lớn**.
  Nếu `resizeImageToMaxSize(path, 2048)` chạy **trước** bước kiểm dung lượng, một ảnh 5MB / 8000×6000 sẽ resize xuống <2MB rồi **được lưu** — tức bug gốc vẫn còn với đúng loại ảnh KH gặp (ảnh chụp từ điện thoại).
  → **Fix**: bổ sung **TC-MEDIAIMG001-01** và **TC-MEDIAIMG001-02** (§5); song song nhờ Dev xác nhận thứ tự `check size` ↔ `resize` trên branch `ai_fixbug_39040`.

- **[MAJOR] M12 — Auto-fill từ Redmine chưa được tester verify.**
  `01-bug-task.md:42` và `03-dev-impact.md:20` đều có `Auto-filled: 2026-08-26 by /new-task` nhưng checkbox **"Tester verify auto-fill chính xác" CHƯA tick** ở cả 2 file. F/D/T trong report này suy ra từ nội dung chưa được người xác nhận.
  → **Fix**: tester đọc lại Redmine #39040 (journal #131894) và tick 2 checkbox trước khi report này có hiệu lực.

### 4.3 Minor (có thể fix sau)

- **[MINOR] M13 — MEDIA-CLEAN-001: chức năng cho phép thay/xóa ảnh nhưng không TC nào kiểm file cũ trả 404.**
  `MEDIA-CLEAN-001` là ★ **BẮT BUỘC (nâng Cao)** khi chức năng cho phép **xóa hoặc thay thế** file/ảnh đã upload — màn này có cả 2. Catalog E `MED-11`: *"File cũ trả 404 ở cả server local và B2 khi truy cập kèm `?v=x`"*.
  **Lý do chỉ để MINOR**: fix lần này **không chạm** logic dọn file (mục 4.2 Dev: "không đổi cấu trúc hay dữ liệu đã lưu"), và `RULE-12` giới hạn phạm vi regression = smoke + danh sách của Dev + case từng fail. Đề xuất TC ở đây sẽ rơi vào **AP-5 (over-coverage layer downstream)**.
  → **Leader quyết**: đưa vào bộ TC nền của FA-038 (chạy độc lập với ticket này), **không** chặn nghiệm thu #39040.

- **[MINOR] M14 — DATA-DB-001: không có TC kiểm `WHERE` scope trên 2 tài khoản / 2 bot.**
  Task có thao tác UPDATE (`bots.bot_image`), theo quy tắc thông thường sẽ là `[BLOCKER] DATA-DB-001`. **Hạ xuống MINOR** vì fix chỉ thêm một cổng kiểm dung lượng, **không chạm câu lệnh UPDATE, không chạm điều kiện `WHERE`, không chạm `bot_id`** — bắt lỗi scope ở đây là test layer không bị sửa (AP-5). Các TC hiện tại đã verify `bots.bot_image` đúng bot đang thao tác.
  → **Ghi nhận**, không chặn merge.

- **[MINOR] M15 — Expected của TC-DEPLOYASSET001-01 chưa xuống tới DevTools Network.**
  `DEPLOY-ASSET-001` yêu cầu evidence là *"screenshot DevTools Network (query version + 200)"*; Expected hiện chỉ dừng ở "hệ thống phải chặn với 「2MB以下…」".
  → Bổ sung vào Expected khi chạy lại theo M3.

- **[MINOR] M16 — `TC No.` gốc trên Studio dùng `temp_id` dạng `NEW-1`…`NEW-13`, không theo quy ước repo `TC-<mã quan điểm bỏ gạch>-<nn>`.**
  Đã map lại trong `04-tc-list.md` và giữ `Studio #<id> (<temp_id>)` ở cột `Ghi chú` để trace ngược. Sau khi remap mã quan điểm theo M6 thì `TC No.` cũng phải đánh lại.

### 4.4 Nit (gợi ý)

- **[NIT] [AP-4] Không có link PR** — chỉ có branch `ai_fixbug_39040` + commit `5c33646743`. Fix shape là đổi hằng số nên rủi ro thấp, nhưng Leader cần branch để tự đối chiếu **vị trí đặt check size so với bước `resizeImageToMaxSize`** (liên quan trực tiếp M11).
- **[NIT] RULE-06 — ảnh đại diện bot là "ảnh người gửi" hiển thị cho LINE user.** Catalog E `MED-03`: *"Profile người gửi — Upload, sửa — Ảnh — Ảnh profile áp dụng đúng khi gửi template"* (`MEDIA-001`, `MSG-004`). Về nguyên tắc RULE-06 sẽ đòi verify tới LINE app thật. **Không đề xuất TC** vì fix không chạm luồng gửi tin (tránh AP-5) — ghi nhận để Leader quyết.
- **[NIT] CONC-003 (race UI)** — màn mới **auto-save ngay khi chọn file**; chọn nhanh 2 file liên tiếp có thể tạo 2 request chồng nhau. Ưu tiên Trung bình, giá trị thấp với fix này.
- **[NIT] `kho-tcs/` chưa có file cho FA-038** — nên bộ TC của màn này không có kho tham chiếu. Đề nghị chạy `/collect-tcs` cho FA-038 để lần review sau có vùng regression đối chiếu.

---

## 4.5 TC trùng lặp nội dung

**Đã rà toàn bộ 13 TC theo 4 yếu tố** (`mã quan điểm` × `loại case` × `đối tượng + thao tác` × `tiền đề tương đương` → `expected` tương đương). Phát hiện **1 nhóm trùng**.

| Nhóm trùng | TC giữ lại | TC đề nghị xóa / gộp | Loại trùng | 4 yếu tố trùng nhau | Severity |
|---|---|---|---|---|---|
| DUP-1 | **TC-FUNC004-01** (Studio #12823 — `2097152 bytes`) | **TC-FUNC004-02** (Studio #12879 — `2097151 bytes`) → đề nghị **GỘP**, không xóa | `DUP-SUBSET` | ① mã quan điểm `FUNC-004` · ② loại case `Boundary` · ③ đối tượng+thao tác: chọn file ảnh tại vùng avatar màn mới `/admin/setting-bot` · ④ tiền đề: OA đăng nhập, đã chọn bot, mở `/admin/setting-bot/{id}` → **expected tương đương**: ảnh được chấp nhận + toast 「アカウント画像を変更しました」 + `bots.bot_image` cập nhật | `[MINOR]` |

**Phân tích DUP-1**: `2097151` (biên−1) và `2097152` (đúng biên) cùng nằm trong lớp tương đương "≤ giới hạn" và cho cùng kết quả. Bất kỳ lỗi nào `2097151` phát hiện được thì `2097152` cũng phát hiện được — ngược lại thì không (chỉ `2097152` mới phân biệt được implement `>` đúng chuẩn với `>=` sai chuẩn). Vì vậy `2097151` là **tập con** của `2097152` về năng lực phát hiện lỗi.

- **Gate đã chạy**: giả định gộp TC-FUNC004-02 vào TC-FUNC004-01 → chạy lại §3 + §7 F.1 trên tập còn lại. Coverage **còn nguyên** (TC-FUNC004-01 vẫn cover REQ-003 + REQ-004 + F1 + F2, `FUNC-004` vẫn có Boundary). ⇒ **Đủ điều kiện xóa, nhưng vẫn đề nghị GỘP thay vì xóa** vì chi phí chạy thấp và đây là **TC duy nhất do người viết** trong bộ 13 TC.
- **Cách gộp đề nghị**: giữ TC-FUNC004-01, thêm `2097151 bytes` vào cột `Dữ liệu test/input` (2 giá trị cùng 1 expected) — giống cách `kho-tcs/fa004` gộp 6 input cùng kết quả ở `TC-RM-88`. Đồng thời **bổ sung `requirement_keys` cho #12879** (hiện đang rỗng) nếu Leader quyết giữ riêng.
- `DUP-INFLATE`: **không có** — không nhóm trùng nào che GAP. `FUNC-004` dù bỏ TC-FUNC004-02 vẫn còn 3 TC Boundary.
- `DUP-CONFLICT`: **không có** — không cặp TC nào cùng tiền đề + cùng steps mà `Kết quả mong đợi` mâu thuẫn.
- **Không tính là trùng** (đã cân nhắc và loại): TC-TOOLVAL2001-01 vs TC-FUNC004-03 (cùng `2097153` màn mới nhưng khác **tầng**: gọi thẳng server vs thao tác UI) · TC-TOOLKNOW002-01 vs TC-FUNC004-03 (khác **loại case**: Abnormal 5MB vs Boundary 2MB+1) · TC-TOOLVAL2001-01 vs TC-TOOLVAL2001-02 (khác **màn / endpoint**).
- Xóa/gộp thật do human thực hiện trên Studio (`testcase_update` / `testcase_delete`) — **report này không tự sửa TC**.

---

## 5. TCs đề xuất bổ sung

**Đã đối chiếu trước khi viết** (BƯỚC 5a / 5b):

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | **`kho-tcs/` chưa có file cho `FA-038`** — không đối chiếu trực tiếp được. Đã đọc chéo `kho-tcs/fa004-richmenu-リッチメニュー.md` (nhóm "Step 1 — Ảnh", `TC-RM-88` → `TC-RM-104`) và `kho-tcs/fa001-chat11-11チャット.md` (`TC-CHT-195`) vì cùng lớp quan điểm `MEDIA-001` / `MEDIA-IMG-001`. |
| Vùng regression phát hiện từ kho | `TC-RM-94` (richmenu >10MB → 「10MB以下のをアップしてください。」) — xác nhận **chuỗi thông báo dạng `<N>MB以下のをアップしてください。` là mẫu dùng chung nhiều màn** → hỗ trợ TC-FUNC004-06 (phải hiện đúng "2MB", không sót chuỗi "10MB" cũ). `TC-RM-96/97/98` (resize theo dung lượng) + `TC-CHT-195` (resize ảnh lớn) — xác nhận **tiền lệ về thứ tự resize ↔ kiểm dung lượng** → hỗ trợ TC-MEDIAIMG001-01/02. `TC-RM-99` (PNG trong suốt bị chuyển nền trắng — bug #31953 chưa fix hết) → hỗ trợ TC-FUNC003-01. |
| Conflict expected vs kho | **Không.** `TC-RM-94` dùng mức 10MB nhưng cho **richmenu** (`MED-L09`), khác đối tượng với ảnh đại diện bot → không mâu thuẫn. |
| GAP dùng lại TC kho (không viết mới) | **Không** — kho chưa có TC nào cho màn Profile bot / LOA接続設定. |
| Xác nhận chống trùng | **Đã đối chiếu 13 TC ở BƯỚC 0 + 3 file kho nêu trên — không TC đề xuất nào trùng.** Cụ thể đã loại 2 ý tưởng vì đã có TC: "reject 5MB trên màn mới" (đã có TC-TOOLKNOW002-01) và "reject 2MB+1 qua API màn cũ" (đã có TC-TOOLVAL2001-02). Các GAP chỉ cần **chạy lại đúng env / đúng precondition** (M1, M3, M4) đã ghi ở §4, **không đẻ TC mới**. |
| Bổ sung sau round 1 (2026-08-27) | Leader chỉ định thêm 2 quan điểm **chưa có trong bảng F.1 của round 1**: `OUT-PREVIEW-001` (Cao) và `UI-001`. Đã soạn **TC-OUTPREVIEW001-01** + **TC-UI001-01** (đánh dấu ✅ trong bảng dưới) và **đã push lên Studio task #202** (`testcase_create`, `client_ref` = TC No. → idempotent): Studio **#14593** (`NEW-14`) và **#14594** (`NEW-15`), `status = draft`, chưa chạy. Đã rà chống trùng với 13 TC gốc + 9 TC đề xuất còn lại — không trùng (chi tiết ghi ở cột `Ghi chú` của từng TC). |

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-FUNC004-05 | API | FUNC-004 | Ảnh đại diện bot — clone từ URL (`link_of_image`) | Abnormal | Clone ảnh >2MB từ URL ngoài vào ảnh đại diện bot — phải bị chặn như upload file | - Đăng nhập OA (主管理者), bot A đang có ảnh đại diện, ghi lại ảnh hiện tại<br>- Có sẵn 1 URL ảnh công khai truy cập được, dung lượng ~5MB (VD ảnh đặt trên Drive/CDN test)<br>- Đã hỏi Dev xác nhận màn nào còn lối nhập URL ảnh (màn cũ `/admin/bot-edit` — spec BR-15) | 1. Mở màn cài đặt kết nối bot, tìm chỗ đặt ảnh đại diện bằng đường dẫn ảnh (không chọn file từ máy)<br>2. Dán URL ảnh ~5MB vào ô đó<br>3. Bấm 「保存」<br>4. Đọc thông báo hiện ra<br>5. Làm mới màn, quan sát ảnh đại diện<br>6. Lặp lại bước 1–5 với URL ảnh ~1MB để đối chứng | ① URL ảnh ~5MB · ② URL ảnh ~1MB (đối chứng) | - ① Hiện thông báo lỗi 「2MB以下のをアップしてください。」; ảnh đại diện **giữ nguyên ảnh cũ**, không đổi sau khi làm mới<br>- ② Ảnh ~1MB clone thành công, ảnh đại diện đổi sang ảnh mới<br>- Không xuất hiện lỗi hệ thống / trang trắng ở cả 2 trường hợp | | **Lấp GAP-1 (BLOCKER-2)** · cover impact F1, F3, BUG · Môi trường: PRODUCTION · Đánh giá spec: Đã hỏi leader (spec BR-15 `feature-spec.md:511` + `logic-spec.md` bước 8b `grab_image()`) · Evidence: screenshot thông báo + ảnh đại diện trước/sau + URL ảnh đang dùng · ⚠️ Nếu Dev xác nhận màn hiện tại **không còn** lối nhập URL ảnh thì đóng GAP-1 bằng xác nhận đó, không cần chạy TC |
| TC-MEDIAIMG001-01 | UI | MEDIA-IMG-001 | Ảnh đại diện bot — dung lượng vs kích thước ảnh | Abnormal | Ảnh nhiều MB + pixel rất lớn gửi thẳng tới server (bỏ qua kiểm tra trên trình duyệt) — vẫn phải bị chặn, không được "gầy đi" rồi lọt | - Đăng nhập OA (主管理者), bot A đang có ảnh đại diện, ghi lại ảnh hiện tại<br>- Chuẩn bị ảnh JPEG **8000×6000 px, ~5MB**<br>- Dùng công cụ gửi request có sẵn phiên đăng nhập (không thao tác qua giao diện) để mô phỏng trường hợp trình duyệt bị bỏ qua | 1. Gửi ảnh 8000×6000 ~5MB thẳng tới chức năng lưu ảnh đại diện của màn mới, dùng phiên đăng nhập hợp lệ<br>2. Đọc nội dung phản hồi<br>3. Làm mới màn cài đặt kết nối bot, quan sát ảnh đại diện<br>4. Lặp lại bước 1–3 với màn cũ | Ảnh JPEG 8000×6000 px, ~5MB | - Phản hồi báo lỗi với đúng chuỗi 「2MB以下のをアップしてください。」<br>- Ảnh đại diện **giữ nguyên ảnh cũ** sau khi làm mới, ở cả 2 màn<br>- **Không** có ảnh mới nào được tạo ra trong thư mục ảnh của bot | | **Lấp GAP từ M11** · cover impact F1, F3 · Môi trường: PRODUCTION · Đánh giá spec: Spec không ghi — đã hỏi Dev về thứ tự kiểm dung lượng ↔ thu nhỏ ảnh (`resizeImageToMaxSize` 2048px, spec BR-13) · Evidence: nội dung phản hồi + ảnh đại diện trước/sau + danh sách file ảnh của bot trước/sau · **Đây là case phân biệt: ảnh 5MB ở TC-TOOLKNOW002-01 bị chặn ngay trên trình duyệt nên chưa bao giờ chạm tới bước kiểm phía máy chủ** |
| TC-MEDIAIMG001-02 | UI | MEDIA-IMG-001 | Ảnh đại diện bot — thu nhỏ ảnh sau khi lưu | Normal | Ảnh hợp lệ (≤2MB) nhưng cạnh lớn hơn 2048px — lưu được và ảnh được thu nhỏ đúng tỉ lệ | - Đăng nhập OA (主管理者), bot A, mở màn cài đặt kết nối bot<br>- Chuẩn bị ảnh JPEG **4096×2048 px, ~1.5MB** (dưới giới hạn dung lượng, trên giới hạn kích thước) | 1. Chọn ảnh 4096×2048 ~1.5MB tại vùng ảnh đại diện<br>2. Quan sát thông báo hiện ra<br>3. Làm mới màn, mở ảnh đại diện ra xem<br>4. Tải ảnh đại diện đang hiển thị về máy, xem thuộc tính để đọc số đo pixel | Ảnh JPEG 4096×2048 px, ~1.5MB | - Không hiện thông báo lỗi dung lượng; hiện toast 「アカウント画像を変更しました」<br>- Ảnh đại diện đổi sang ảnh mới<br>- Ảnh tải về có **cạnh lớn nhất = 2048px**, cạnh còn lại **1024px** (đúng tỉ lệ gốc 2:1) | | **Lấp GAP từ M11** (`BR-13` Studio báo coverage `none`) · cover impact F1, T1 · Môi trường: PRODUCTION · Đánh giá spec: Spec ghi rõ (`feature-spec.md` BR-13 + Catalog E `MED-L10`) · Evidence: ảnh gốc + ảnh tải về **kèm số đo px** của cả 2 · regression |
| TC-FUNC004-06 | UI | FUNC-004 | Ảnh đại diện bot — thông báo lỗi | Abnormal | Ảnh vượt cả ngưỡng cũ (>10MB) — thông báo phải là 2MB, không được sót chuỗi 10MB cũ | - Đăng nhập OA (主管理者), bot A, mở màn cài đặt kết nối bot bản mới<br>- Chuẩn bị ảnh JPEG ~12MB | 1. Chọn ảnh ~12MB tại vùng ảnh đại diện<br>2. Đọc **nguyên văn** thông báo hiện ra, chụp lại<br>3. Làm mới màn, quan sát ảnh đại diện<br>4. Lặp lại bước 1–3 trên màn cũ | Ảnh JPEG ~12MB | - Thông báo hiện đúng 「2MB以下のをアップしてください。」 (có dấu 。)<br>- **KHÔNG** hiện chuỗi cũ 「10MB以下のをアップしてください。」<br>- Ảnh đại diện giữ nguyên ảnh cũ, ở cả 2 màn | | **Lấp GAP từ M10** · cover impact F1, F2, F3, F4 · Đánh giá spec: Đã hỏi leader (phụ thuộc BLOCKER-1 chốt mức giới hạn) · Evidence: screenshot thông báo đọc rõ nguyên văn · dẫn tiền lệ chuỗi từ `kho-tcs/fa004` `TC-RM-94` |
| TC-FUNC003-01 | UI | FUNC-003 | Ảnh đại diện bot — định dạng & file hỏng | Abnormal | File 0 byte / sai định dạng / đổi đuôi — báo lỗi rõ ràng, không lưu, không lỗi hệ thống | - Đăng nhập OA (主管理者), bot A đang có ảnh đại diện, ghi lại ảnh hiện tại<br>- Chuẩn bị 4 file: ① ảnh JPEG **0 byte** · ② file `.pdf` ~500KB · ③ file `.pdf` ~500KB **đổi đuôi thành `.jpg`** · ④ ảnh **PNG nền trong suốt** ~800KB | 1. Lần lượt chọn từng file ① → ④ tại vùng ảnh đại diện<br>2. Sau mỗi lần: đọc thông báo, quan sát ảnh đại diện và vùng xem trước<br>3. Làm mới màn sau mỗi lần, xác nhận ảnh đại diện<br>4. Riêng file ④: tải ảnh đại diện về, mở bằng công cụ xem ảnh có nền ô caro | ① JPEG 0 byte · ② PDF 500KB · ③ PDF đổi đuôi .jpg · ④ PNG trong suốt 800KB | - ①②③: hiện thông báo lỗi rõ ràng (không phải trang trắng / không im lặng); ảnh đại diện **giữ nguyên ảnh cũ** sau khi làm mới<br>- ④: lưu thành công và **giữ nguyên nền trong suốt**, không bị chuyển thành nền trắng/đen<br>- Không trường hợp nào gây lỗi hệ thống | | **Lấp GAP từ M10** · cover impact F1, F2, T1 · Môi trường: PRODUCTION (phần ④ theo RULE-08) · Đánh giá spec: Spec không ghi — cần hỏi leader về thông báo lỗi mong đợi cho từng loại · Evidence: screenshot thông báo từng file + ảnh PNG tải về trên nền caro · ⚠️ Tiền lệ `kho-tcs/fa004` `TC-RM-99`: PNG trong suốt **đã từng bị chuyển nền trắng** (bug #31953) → có khả năng FAIL, nếu fail thì raise ticket riêng |
| TC-FUNCSEQ001-01 | UI | FUNC-SEQ-001 | Ảnh đại diện bot — thao tác liên tiếp sau khi bị chặn | Normal | Bị chặn vì ảnh quá cỡ rồi chọn tiếp ảnh hợp lệ — vẫn lưu được bình thường | - Đăng nhập OA (主管理者), bot A, mở màn cài đặt kết nối bot bản mới<br>- Chuẩn bị 1 ảnh ~5MB và 1 ảnh ~1MB<br>- Ghi lại ảnh đại diện hiện tại | 1. Chọn ảnh ~5MB → đọc thông báo lỗi<br>2. **Không** làm mới màn, chọn tiếp ảnh ~1MB tại cùng vùng ảnh đại diện<br>3. Quan sát thông báo và ảnh đại diện<br>4. Làm mới màn, xác nhận ảnh đại diện<br>5. Lặp lại chuỗi trên **2 lần liên tiếp** | ① ảnh ~5MB → ② ảnh ~1MB, lặp 2 vòng | - Bước 1: hiện lỗi 「2MB以下のをアップしてください。」<br>- Bước 2–3: ảnh ~1MB lưu thành công, toast 「アカウント画像を変更しました」, **không** còn thông báo lỗi cũ đọng lại trên màn<br>- Bước 4: ảnh đại diện là ảnh ~1MB<br>- Lặp lần 2 cho kết quả y hệt | | **Lấp GAP từ §7 F.1 `FUNC-SEQ-001`** · cover impact F2 · Đánh giá spec: Spec không ghi — hành vi suy từ luồng tự lưu ngay khi chọn file · Evidence: video quay liền mạch cả chuỗi thao tác · ⚠️ Màn mới **tự lưu ảnh ngay khi chọn** nên đây là chuỗi thao tác người dùng gặp thật sau khi bị báo lỗi |
| TC-REGSHARED001-03 | UI | REG-SHARED-001 | Màn thêm / đổi tài khoản — ảnh đại diện | Abnormal | Xác nhận hành vi hiện tại khi upload ảnh >2MB ở màn thêm / đổi tài khoản (Dev báo chưa có kiểm dung lượng) | - Đăng nhập OA (主管理者) còn slot tạo bot (`countBot < max_bot`)<br>- Chuẩn bị ảnh JPEG ~5MB<br>- Xác định trước 3 lối vào cần thử: thêm tài khoản mới, đổi tài khoản, và lối vào từ danh sách tài khoản | 1. Vào màn thêm tài khoản mới, chọn ảnh đại diện ~5MB<br>2. Hoàn tất các bước và lưu<br>3. Đọc thông báo, quan sát ảnh đại diện của bot vừa tạo<br>4. Lặp lại bước 1–3 ở màn đổi tài khoản<br>5. Ghi lại hành vi thực tế của **từng lối vào** | Ảnh JPEG ~5MB, thử ở 3 lối vào | - **Kết quả mong đợi theo chuẩn**: cả 3 lối vào đều chặn ảnh >2MB và hiện 「2MB以下のをアップしてください。」<br>- ⚠️ **DỰ KIẾN FAIL** — Dev xác nhận các màn này *"hoàn toàn không kiểm dung lượng"*<br>- Nếu ảnh >2MB lưu được ở bất kỳ lối vào nào → **raise ticket** kèm ghi rõ lối vào nào | | **Lấp GAP F5 / T2 (M5)** · cover impact F5, T2 · Môi trường: PRODUCTION · Đánh giá spec: Đã hỏi leader — **Dev cố ý để ngoài phạm vi #39040**, TC này để *xác nhận hành vi*, không phải verify fix · Evidence: screenshot từng lối vào + ảnh đại diện sau khi lưu · ⚠️ **Chỉ chạy sau khi Leader chốt M5 (đưa vào ticket này hay tách ticket riêng)** |
| TC-REGSHARED001-04 | UI | REG-SHARED-001 | Màn cũ `/admin/bot-edit` — nhánh dùng chung `botChange` | Normal | Đổi Channel Secret (không kèm ảnh) vẫn lưu thành công, không bị kiểm dung lượng chặn oan | - Đăng nhập OA (主管理者), mở `/admin/bot-edit?id={id}`<br>- Bot A **có channel credentials THẬT** (bắt buộc — nếu dùng credentials giả, bước xác thực với LINE sẽ chặn và không kết luận được)<br>- Bot A đang có ảnh đại diện; ghi lại ảnh và thời hạn token hiện tại | 1. **Không** chọn file ảnh mới<br>2. Nhập Channel Secret hợp lệ (giá trị thật, có khoảng trắng thừa ở đầu/cuối để kiểm luôn việc cắt khoảng trắng)<br>3. Bấm 「保存」<br>4. Đọc thông báo<br>5. Làm mới màn: kiểm Channel Secret đã lưu, ảnh đại diện, và thông tin kết nối | Channel Secret hợp lệ (có khoảng trắng thừa), không đính ảnh | - Lưu thành công, **không** xuất hiện thông báo 「2MB以下のをアップしてください。」<br>- Channel Secret được lưu đúng (khoảng trắng thừa bị cắt)<br>- Ảnh đại diện **giữ nguyên** ảnh cũ<br>- Trạng thái kết nối LOA vẫn bình thường | | **Lấp GAP REQ-007 nhánh `channel_secret` (M7b)** · cover impact F3, T1 · Môi trường: PRODUCTION · Đánh giá spec: Spec ghi rõ (`feature-spec.md` BR-08 ~ BR-11) · Evidence: screenshot thông báo + màn sau khi làm mới + trạng thái kết nối · **regression** — chứng minh cổng kiểm 2MB chỉ áp dụng khi có file ảnh · ⚠️ Đây là nhánh khiến 3 TC màn cũ bị `error` ở auto-run (M4) — precondition credentials thật là bắt buộc |
| TC-OUTPREVIEW001-01 ✅ | UI | OUT-PREVIEW-001 | Ảnh đại diện bot — xem trước vs ảnh lưu thật | Normal | Ảnh xem trước trước khi lưu và ảnh đại diện sau khi lưu phải là cùng một ảnh | - Đăng nhập OA (主管理者), đã chọn bot A<br>- Bot A đang có ảnh đại diện; chụp lại màn hình ảnh hiện tại để đối chiếu<br>- Chuẩn bị 1 ảnh JPEG hợp lệ ~1MB, kích thước 3000×1500 (ảnh có nội dung dễ nhận biết: có chữ và có góc trên-trái đánh dấu rõ, để phát hiện xoay/lật/cắt)<br>- Mở `/admin/bot-edit?id={id}` | 1. Trên màn cũ `/admin/bot-edit`, chọn file ảnh 3000×1500 ~1MB tại vùng ảnh đại diện<br>2. Quan sát vùng xem trước, chụp lại ảnh xem trước (chưa bấm lưu)<br>3. Bấm 「保存」, chờ thông báo lưu xong<br>4. Làm mới màn, chụp lại ảnh đại diện đang hiển thị<br>5. Copy đường dẫn ảnh đại diện, mở bằng tab mới và so sánh với ảnh xem trước đã chụp ở bước 2<br>6. Mở màn mới `/admin/setting-bot/{id}` và lặp lại: chọn cùng file ảnh đó, quan sát vùng xem trước và ảnh đại diện ngay sau khi màn tự lưu, rồi làm mới màn và so sánh lại | Ảnh JPEG 3000×1500, ~1MB, có chữ và dấu mốc ở góc trên-trái | - Ảnh xem trước ở bước 2 và ảnh đại diện sau khi lưu là **CÙNG MỘT ảnh**: cùng nội dung, cùng hướng, dấu mốc vẫn ở góc trên-trái, không bị xoay / lật / cắt mất phần nào<br>- Đường dẫn ảnh đại diện mở xem được ở **cả 2 thời điểm**: ngay sau khi lưu và sau khi làm mới màn<br>- Trên màn mới (tự lưu ngay khi chọn file): ảnh xem trước và ảnh đại diện sau khi tự lưu khớp nhau, **không** có tình trạng vùng xem trước hiện ảnh mới nhưng ảnh đại diện vẫn là ảnh cũ<br>- Cả 2 màn cho kết quả giống nhau | | **Leader bổ sung sau review round 1 (2026-08-27)** · Lấp GAP quan điểm `OUT-PREVIEW-001` (**Cao**) — không có TC nào trong 13 TC gốc · cover impact **F2, F4, T1** · Môi trường: PRODUCTION · Đánh giá spec: Spec ghi rõ (`feature-spec.md` BR-12/BR-13 + Catalog E `MED-12`) · Evidence: **cặp ảnh chụp preview vs ảnh đại diện sau khi lưu, đặt cạnh nhau** · Trigger: fix có sửa `readURL` (`public/js/admin/bot.js`) — chính là hàm sinh vùng xem trước · ⚠️ Phân biệt: phần **đo số đo pixel sau resize** thuộc TC-MEDIAIMG001-02; TC này chỉ đối chiếu *có phải cùng một ảnh không*. Nhánh ảnh bị từ chối (preview không được đổi) đã có ở Studio #12847 · **Đã push Studio #14593 (NEW-14)** |
| TC-UI001-01 ✅ | UI | UI-001 | Ảnh đại diện bot — hiển thị thông báo lỗi | Normal | Thông báo lỗi 2MB hiển thị đầy đủ, không vỡ layout ở độ phân giải 1366×768 | - Đăng nhập OA (主管理者), đã chọn bot A<br>- Chuẩn bị 1 ảnh JPEG ~5MB (vượt giới hạn để kích hoạt thông báo lỗi)<br>- Chuẩn bị được 2 độ phân giải cửa sổ trình duyệt: **1366×768** (thấp nhất được hỗ trợ) và 1920×1080<br>- Ghi lại ảnh đại diện hiện tại để đối chiếu | 1. Đặt cửa sổ trình duyệt về đúng 1366×768, mở màn mới `/admin/setting-bot/{id}`<br>2. Chọn file ảnh ~5MB tại vùng ảnh đại diện để kích hoạt thông báo lỗi<br>3. Chụp toàn bộ khung nhìn: đọc nguyên văn thông báo, kiểm xem có bị cắt chữ, tràn ra ngoài khung nhìn hay che mất nút thao tác không<br>4. Khi thông báo đang hiện, thử bấm các nút thao tác chính trên màn xem có bấm được không<br>5. Cuộn ngang màn hình để xác nhận không xuất hiện thanh cuộn ngang thừa<br>6. Lặp lại bước 2–5 trên màn cũ `/admin/bot-edit?id={id}`<br>7. Đổi cửa sổ về 1920×1080 và lặp lại toàn bộ trên cả 2 màn để đối chiếu | Ảnh JPEG ~5MB; 2 độ phân giải cửa sổ: 1366×768 và 1920×1080 | - Ở **1366×768**, thông báo hiển thị **ĐẦY ĐỦ** nguyên văn 「2MB以下のをアップしてください。」 (có dấu 。), đọc được hết chữ, không bị cắt cụt, không tràn ra ngoài khung nhìn<br>- Thông báo **không che mất nút thao tác nào**; các nút chính vẫn bấm được bình thường khi thông báo đang hiện<br>- Bố cục màn không vỡ: các khối vẫn thẳng hàng, **không xuất hiện thanh cuộn ngang thừa**<br>- Nội dung thông báo ở 1366×768 và 1920×1080 **giống hệt nhau**<br>- Cả màn mới và màn cũ đều cho kết quả nhất quán | | **Leader bổ sung sau review round 1 (2026-08-27)** · Lấp GAP quan điểm `UI-001` — không có TC nào trong 13 TC gốc · cover impact **F1, F2, F3, F4** · Đánh giá spec: Spec không ghi — hành vi hiển thị suy từ Catalog B · Evidence: **screenshot toàn khung nhìn ở CẢ 2 độ phân giải, trên CẢ 2 màn (4 ảnh)** · Trigger: fix đổi **nội dung** chuỗi thông báo (10MB → 2MB) ở cả `setting-bot.js` lẫn `bot.js`; chuỗi tiếng Nhật mới có độ dài khác chuỗi cũ · Chuẩn: `UI-001` "bắt buộc kiểm ở 1366×768" + Catalog B `UIC-13`, `UIC-11`, `UIC-02` · **Phạm vi surface**: chỉ admin web PC — màn cài đặt kết nối bot không có bản mobile app và không chạy trong LIFF → 2 surface đó đánh × **có lý do** (RULE-03) · Gợi ý mở rộng `UI-002` nếu Leader duyệt: chạy thêm trên **Safari/Mac** (nhóm người dùng chính là chủ salon / cửa hàng nhỏ) · **Đã push Studio #14594 (NEW-15)** |
| TC-ENV003-01 | API | ENV-003 | Ảnh đại diện bot — môi trường production | Normal | Chạy lại bộ core trên PRODUCTION và kiểm ảnh truy cập được qua cả đường local lẫn `p.lmes.jp` | - Tài khoản OA **thật** trên `step.lme.jp`, bot dùng để test đã thống nhất với Leader (tránh đụng dữ liệu khách)<br>- Ghi lại ảnh đại diện hiện tại để khôi phục sau khi test<br>- Chuẩn bị ảnh ~1MB và ảnh ~5MB | 1. Trên production, chọn ảnh ~5MB → xác nhận bị chặn với 「2MB以下のをアップしてください。」<br>2. Chọn ảnh ~1MB → xác nhận lưu thành công<br>3. Copy đường dẫn ảnh đại diện đang hiển thị, mở bằng tab mới<br>4. Chờ qua chu kỳ đồng bộ media, mở lại đường dẫn ảnh lần nữa<br>5. Khôi phục ảnh đại diện ban đầu | ① ảnh ~5MB (chặn) · ② ảnh ~1MB (lưu được) | - Bước 1: chặn đúng, ảnh đại diện không đổi<br>- Bước 2: lưu thành công, ảnh mới hiển thị<br>- Bước 3 và 4: đường dẫn ảnh **mở xem được ở cả 2 lần** (trước và sau chu kỳ đồng bộ), không lỗi 404, ảnh hiển thị đúng | | **Lấp GAP M1 (RULE-08 / ENV-003)** · cover impact BUG, F1, F2, T1 · Môi trường: **PRODUCTION** (bắt buộc — Catalog D: production dùng media server riêng `p.lmes.jp` + đồng bộ B2) · Đánh giá spec: Spec ghi rõ (Catalog D mục Media) · Evidence: screenshot thông báo + ảnh mở được qua đường dẫn ở **cả 2 thời điểm** · ⚠️ Tránh tạo/xóa dữ liệu thật — nhớ khôi phục ảnh cũ ở bước 5 |

---

## 6. Spec update needed

- [ ] Không cần update spec
- [x] **Cần update spec** — 3 hạng mục:

**(1) Giới hạn dung lượng ảnh đại diện bot — chưa tồn tại ở bất kỳ đâu** *(gốc của BLOCKER-1)*
- **Section**: `spec-features/admin/bot-edit/feature-spec.md` §5.4 "Image Handling (BR-12 ~ BR-15)" + `web/api-spec.md` EP-02 (param `image`, cột Validation đang trống)
- **Nội dung cần update**: thêm business rule mới, VD `BR-12b | Ảnh đại diện bot: giới hạn dung lượng <N>MB; vượt → chặn ở cả JS và server, thông báo 「<N>MB以下のをアップしてください。」`. Áp dụng cho **cả** `/admin/setting-bot` (mới) và `/admin/bot-edit` (cũ).
- **Liên quan**: Sprint spec **#34620** `screens/unclear-points.md` **UP-07** đang bỏ ngỏ mục này — cần đóng UP-07 cùng lúc.
- **Người chịu trách nhiệm**: PM (chốt con số) → Dev (cập nhật spec-features) → QA (set `spec_status` cho 13 TC)

**(2) Màn mới `/admin/setting-bot` chưa có spec trong `spec-features/`**
- **Section**: `spec-features/admin/` — grep `"setting-bot"` toàn bộ `spec-features/` trả về **0 kết quả**. `templates/LME-SYSTEM-SPEC.md:573` vẫn ghi URL chính của FA-038 là `/admin/bot-edit?id={id}`, trong khi Dev xác nhận sidebar v2 (`resources/views/layout/v2/admin/sidebar.blade.php:175,182`) đã trỏ sang route `settingBot` = `/admin/setting-bot`.
- **Nội dung cần update**: bổ sung spec cho màn mới (endpoint `/admin/ajax/setting-bot/update`, luồng **tự lưu ảnh ngay khi chọn file** — khác hẳn màn cũ phải bấm 「保存」), và cập nhật URL chính của FA-038 trong `LME-SYSTEM-SPEC.md`.
- **Ảnh hưởng review**: đây là lý do `02-spec-reference.md` không lập được cho màn đang bị bug — mọi Expected của 6 TC màn mới hiện dựa trên mô tả của Dev, không dựa trên spec.
- **Người chịu trách nhiệm**: Dev / PM

**(3) `framework/catalog-lme.md` Khối E1 thiếu dòng cho ảnh đại diện bot** *(RULE-10)*
- **Section**: `catalog-lme.md` → Catalog E → Khối E1 "Giới hạn dung lượng theo nơi sử dụng" (hiện có `MED-L01` … `MED-L10`, không có dòng nào cho Profile bot / LOA接続設定)
- **Nội dung cần update**: thêm `MED-L11 | Profile bot (ảnh đại diện LOA) | Ảnh | <N> MB | ⚠️ Khác giới hạn của chat 1:1 (10MB) và template (10MB) — đây chính là chỗ lấy nhầm mức 10MB gây bug #39040`
- **Lý do**: RULE-10 yêu cầu mỗi bug lọt production sinh 1 dòng quan điểm/catalog mới. Root cause của #39040 đúng là *"code lấy nhầm mức 10MB của các màn khác"* — thiếu dòng catalog này là điều kiện để bug tái diễn ở màn tiếp theo.
- **Người chịu trách nhiệm**: Test Leader

---

## 7. Checklist đã chạy

- [x] **A. Coverage** — ⚠️ có GAP: F5, T2 (0 TC); BUG chưa cover đường `link_of_image`
- [x] **B. Chất lượng từng TC** — ✔ **Đạt**: steps tuần tự, precondition đủ để dựng env, Expected đo lường được (có chuỗi thông báo chính xác + trạng thái `bots.bot_image`), atomic, độc lập
- [x] **C. Chất lượng bộ TC tổng thể** — ⚠️ thiếu biến thể input (M10, M11); có 1 nhóm DUP-SUBSET (§4.5)
- [x] **D. Spec alignment** — ❌ **KHÔNG đạt**: mức 2MB không có trong spec (BLOCKER-1); BR-13 + BR-12 coverage `none`; BR-15 không cover (BLOCKER-2); `spec_status = null` ở 13/13 TC
- [x] **E. Hành chính** — ⚠️ `TC No.` gốc dùng `temp_id` (M16); không có link PR (NIT); checkbox verify auto-fill chưa tick ở cả 01 và 03 (M12)
- [x] **F. Base quan điểm test LME**
  - [x] **F.1** Quan điểm (tầng 1) — bảng dưới
  - [x] **F.2** Catalog (tầng 2) — đã mở **Catalog A** (`DI-16` upload ảnh), **Catalog D** (media production / B2 / `p.lmes.jp`, asset version), **Catalog E** (`MED-L10` resize 2048px & chặn 10.000px · `MED-03` profile người gửi · `MED-11` file cũ 404 · `MED-12` path trước/sau save). ⚠️ Khối E1 **thiếu dòng cho ảnh đại diện bot** → §6 mục (3)
  - [ ] **F.3** RULE quy trình — **vi phạm RULE-02** (M2), **RULE-08** (M1), **RULE-01** (M7). RULE-06 ✔ (không áp dụng — fix không chạm luồng output ra LINE). RULE-09 ✔ (test cả màn cũ và màn mới). RULE-03 ✔ (không có × cần lý do). RULE-07 ⚠️ một phần (verify DB `bots.bot_image` + màn + toast ✔; thiếu case 2 tài khoản — M14, đã hạ MINOR có lý do)

### F.1 — Bảng quan điểm đối chiếu

| Mã quan điểm | Ưu tiên | Trigger khớp task? | TC cover (suy luận) | Exec | Kết luận |
|---|---|---|---|---|---|
| `FUNC-001` — Luồng chính đúng đặc tả | **Cao** | ◯ — lưu ảnh ≤2MB phải vẫn chạy | TC-FUNC001-01, TC-FUNC001-02 | 2/2 pass | **RISK** — chỉ có Normal (RULE-01, M7); nhánh accept màn cũ chưa verify thật (M4) |
| `FUNC-004` — Giới hạn trên/dưới | **Cao** | ◯ — **trọng tâm của bug** | TC-FUNC004-01/02/03/04 | 4/4 pass | **RISK** — chỉ có Boundary (M7); thiếu 0 byte + >10MB (M10). Sau khi remap M6 sẽ có thêm Abnormal |
| `FUNC-002` — Bỏ trống trường bắt buộc | **Cao** | ◯ — không chọn file thì save vẫn phải chạy | TC-REGSHARED001-02, TC-REGSHARED001-01 | 2/2 "pass" | **OK** (gián tiếp) — nhánh không-đính-ảnh đã được đối chứng âm |
| `FUNC-003` — Nhập sai định dạng | Trung bình | ◯ — upload file, `DI-16` | — | — | **GAP** → `[MAJOR]` M10 · TC đề xuất: TC-FUNC003-01 |
| `FUNC-SEQ-001` ★ — Thao tác liên tiếp & reload | Trung bình | ◯ — màn mới **tự lưu ngay khi chọn file** | — | — | **GAP** → `[MAJOR]` · TC đề xuất: TC-FUNCSEQ001-01 |
| `MEDIA-001` — Định dạng file/ảnh upload | Trung bình → **Cao** (ảnh bot hiển thị cho LINE user) | ◯ — **BẮT BUỘC** khi có upload file | TC-TOOLKNOW002-01/02 (mã lạ → **không tính**) | — | **GAP** → `[MAJOR]` M10 (bộ file đa nguồn / MIME lạ / PNG alpha) |
| `MEDIA-IMG-001` ★ — Resize / kích thước | Trung bình → **Cao** | ◯ — Catalog E `MED-L10`; spec BR-13 | — | — | **GAP** → `[MAJOR]` M11 (Studio tự báo BR-13 = `none`) · TC đề xuất: TC-MEDIAIMG001-01/02 |
| `MEDIA-CLEAN-001` ★ — Dọn file (local + B2) | Trung bình → **Cao** (có thay/xóa ảnh) | ◯ | — | — | **GAP** → `[MINOR]` M13 (hạ mức: fix không chạm cleanup, tránh AP-5 — Leader quyết) |
| `ENV-003` ★ — Khác biệt dev/staging/production | **Cao** | ◯ — **BẮT BUỘC** khi chạm media | — (13/13 chạy `local`) | 0 prod | **GAP** → `[MAJOR]` M1 · TC đề xuất: TC-ENV003-01 |
| `DEPLOY-ASSET-001` ★ — Version asset | **Cao** | ◯ — release sửa `setting-bot.js` + `bot.js` | TC-DEPLOYASSET001-01 | 1/1 "pass" **sai env** | **RISK** → `[MAJOR]` M3 — nội dung TC đúng, kết quả vô hiệu |
| `REG-SHARED-001` — Shared code / logic | **Cao** | ◯ — `botChange` dùng chung nhiều nhánh | TC-REGSHARED001-01, TC-REGSHARED001-02 | 2/2 "pass" | **RISK** → `[MAJOR]` M5 (F5 chưa cover) + M7b (nhánh `channel_secret`) · Danh sách Dev **có** → không BLOCKER |
| `COMPAT-LEGACY-001` ★ — Cũ & mới song song | **Cao** | ◯ — màn cũ `/admin/bot-edit` và màn mới `/admin/setting-bot` **cùng tồn tại** | 6 TC màn mới + 6 TC màn cũ | 12/12 "pass" | **OK** ✔ — **điểm mạnh nhất của bộ TC**, thỏa RULE-09 |
| `UI-003` — Loading / rỗng / lỗi (rủi ro **false success**) | Trung bình → **Cao** | ◯ — bug gốc chính là **false success** (lưu im lặng, không báo lỗi) | TC-TOOLKNOW002-01 (`update_requests=0`), TC-TOOLKNOW002-02 (`inputCleared`, `previewUnchanged`) | 2/2 pass | **OK** ✔ về hành vi — nhưng mã lạ (M6) nên trên giấy chưa map được |
| `OUT-TRUTH-001` — UI khớp trạng thái THẬT | **Cao** | ◯ — sau reject, màn không được hiện ảnh chưa lưu | TC-TOOLKNOW002-01, TC-TOOLKNOW002-02 | 2/2 pass | **OK** ✔ (verify ảnh đại diện giữ nguyên sau reload) |
| `DATA-DB-001` ★ — Verify DB + `WHERE` scope | **Cao** | ◯ — có UPDATE `bots.bot_image` | 11 TC verify `bots.bot_image` | — | **RISK** → `[MINOR]` M14 (hạ mức có lý do: fix không chạm `WHERE`/`bot_id`) |
| `DATA-001` — Dữ liệu phản ánh đủ ở mọi màn | **Cao** | ◯ — ảnh bot hiện ở nhiều màn | TC-FUNC001-01 (làm mới màn, ảnh mới hiển thị) | 1/1 pass | **RISK** — chỉ verify trên chính màn cài đặt; chưa verify ở danh sách tài khoản / header. Fix không chạm luồng hiển thị → **không đề xuất TC** (AP-5) |
| `CONC-003` ★ — Race ở tầng giao diện | Trung bình | ◯ (yếu) — tự lưu ngay khi chọn file | — | — | **GAP** → `[NIT]` — giá trị thấp với fix này |
| `MSG-004` — Preview khớp nội dung nhận thật trên LINE | **Cao** | × — fix không chạm luồng gửi tin | — | — | **×, có lý do** (RULE-03): ảnh bot là ảnh người gửi (`MED-03`) nhưng fix chỉ siết validate đầu vào, không đổi luồng gửi → tránh AP-5. Ghi `[NIT]` để Leader quyết |
| `PERM-001` / `PERM-002` / `PERM-003` | **Cao** | × — fix không chạm phân quyền | — | — | **×, có lý do** (RULE-03) |
| `DATA-MIG-001` / `DATA-BACKUP-001` | **Cao** | × — không migrate, không đổi schema (mục 4.2 Dev: không có data update) | — | — | **×, có lý do** (RULE-03) |
| `JOB-001` / `INTG-HOOK-001` | **Cao** | × — không có job nền / webhook trong phạm vi fix | — | — | **×, có lý do** (RULE-03) |
| `CONC-001` / `PAY-*` / `MSG-001` / `DATA-COUNT-001` | **Cao** | × — không chạm concurrency, thanh toán, gửi tin, số đếm | — | — | **×, có lý do** (RULE-03) |

**Tổng kết F.1**: 8 quan điểm **GAP** (2 → BLOCKER/MAJOR nặng: `ENV-003`, `MEDIA-IMG-001`; 3 → MAJOR: `FUNC-003`, `FUNC-SEQ-001`, `MEDIA-001`; 1 → MINOR: `MEDIA-CLEAN-001`; 1 → NIT: `CONC-003`) · 6 quan điểm **RISK** · 4 quan điểm **OK** · 9 nhóm **× có lý do**.

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | | |
| Tester | (đã đọc & hiểu feedback) | |

---

<!-- Draft sinh bởi /review-tc ngày 2026-08-26. Nguồn TC: MCP LME TEST STUDIO task_id=202 (13 TC), dừng ở nguồn 1, KHÔNG đối chiếu chéo. TC read-only — mọi đề xuất xóa/gộp/remap ở §4.5 + M6 do human thực hiện qua testcase_update / testcase_delete trên Studio. -->
