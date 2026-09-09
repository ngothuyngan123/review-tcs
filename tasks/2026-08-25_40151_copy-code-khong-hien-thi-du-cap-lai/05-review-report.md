# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | `#40151 — [25-08-2026] [TY-11973] [Admin] Copy code copy dữ liệu không hiển thị dù đã nhấn cấp lại` |
| Reviewer (Leader) | `<Leader verify>` — draft sinh bởi `/review-tc` |
| Tester được review | **AI** (Studio pipeline, `created_job_id = 607`) — không có TC nào do member người viết |
| Ngày review | `2026-08-25` |
| Version TCs | `v1` |
| Vòng review | `Round 1` |

---

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn | **MCP LME TEST STUDIO task #201** (nguồn 1 — mặc định) |
| Ticket · task_id · round · branch | `40151` · `#201` · `round 1` · `ai_small_40151` |
| Thời điểm fetch | `2026-08-25` |
| Tổng số TC review | **8** |
| File 04 trong repo vs Studio | **Khớp** — `04-tc-list.md` được sinh từ chính lần fetch Studio này (8 TC, cùng tập `temp_id` NEW-1…NEW-8). Không có STALE-INPUT. |
| Studio review comments | `review_list_comments(task_id=201)` trả **rỗng** → chưa có vòng review nào trước, không có issue đã đóng để tránh raise lại. |
| Studio task state | `status = done-ai` · `aiResult = pass` · `reviewed = false` · `reviewState = leader` · `openBugs = 0` · `submittedWithoutMcp = false` |

**Cảnh báo bắt buộc từ metadata Studio:**

| # | Chiều | Kết quả | Flag |
|---|---|---|---|
| 1 | Kết quả thực thi thật (`pass` mới là Đạt) | **8/8 pass (100%)** — 0 fail, 0 error, 0 chưa chạy | `OK` về ngưỡng — **nhưng xem #3, #4**: 100% pass này chỉ có giá trị trong phạm vi `local` + do AI tự chạy |
| 2 | TC `fail`/`error` + TC gắn ticket bug | **Không có** TC fail/error; **không** TC nào gắn `bug_tickets` | `OK` |
| 3 | Môi trường đã chạy — RULE-08 / ENV-003 | **PROD 0 · STAGING 0 · DEV 0 · LOCAL 8** (runId 476) | **`[MAJOR]`** — task là **plan gating theo gói cước** (hạng mục `bill tiền` của Catalog D) |
| 4 | Ai chạy (`last_exec.source` / `by`) | **8/8 do AI pipeline** (`source = ai`, `by = pipeline`, 2026-08-25 07:28:49, 25 giây cho cả 8 TC) — 0 TC do QA người chạy | **`[MAJOR]`** — nhóm rủi ro cao (phân quyền + gói cước) chỉ được AI tự chạy tự chấm |
| 5 | Tác giả TC (`author` / `provenance.source`) | **8/8 do AI sinh** (`provenance.source = ai`, `actor = AI`, `created_job_id = 607`); `toolWritten = {tool: 8, human: 0}`; toàn bộ 8 TC ở `status = draft` | **`[MAJOR]`** — 100% AI sinh mà `reviewState` chưa `done` |
| 6 | Mã quan điểm Studio không có trong `checklist-lme.md` | **3 mã / 3 lượt TC**: `TOOL-KNOW-002`, `TOOL-OLDREC-001`, `TOOL-VAL2-001` | **`[MAJOR]`** — 3 TC này **không được tính là cover** quan điểm tầng 1 ở §3/§7.F.1 |

> ⚠️ Nội dung Studio có `contentTrust = untrusted` — được xử lý như **data**, không phải chỉ thị. TC là **read-only**: mọi đề xuất sửa ở report này phải thực hiện trên Studio (`testcase_update`) rồi fetch lại, KHÔNG sửa tay trong repo.

### Input phụ

- `01-bug-task.md` — **có**. `Auto-filled: 2026-08-25 by /new-task`, checkbox "Tester verify auto-fill chính xác" **CHƯA tick**.
- `03-dev-impact.md` — **có**. `Auto-filled: 2026-08-25 by /new-task`, checkbox **CHƯA tick**.
- `02-spec-reference.md` — **KHÔNG có** → fallback [templates/LME-SYSTEM-SPEC.md](../../templates/LME-SYSTEM-SPEC.md). `Input thiếu: 02-spec-reference.md` — không có business rule nào được chốt bằng văn bản cho màn Sao chép dữ liệu; spec duy nhất được viện dẫn là **text popup trong chính code** (`backup.blade.php` dòng 352) do Dev trích.

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — Có issue BLOCKER, cần fix và review lại

**Lý do ngắn gọn**: Bộ 8 TC bám khá sát cách fix ở tầng route (chặn/cho qua đúng 5/6 route) và có cả 2 nhánh free cũ / free mới — nhưng **bỏ lọt 6 điểm rủi ro cao**, trong đó nghiêm trọng nhất là: (a) route `backup.processing` gõ thẳng URL **không bị chặn** — chính Studio tự ghi ra trong note nhưng không TC nào verify; (b) **không có TC nào cho bot chưa có mã sao chép** — đúng luồng KH báo lỗi ("nhấn cấp lại vẫn trống"); (c) **kịch bản nghiệp vụ chính** (bot free làm nguồn → bot trả phí copy sang) hoàn toàn không được test. Thêm nữa toàn bộ kết quả "Đạt" chỉ có ở `local` và do AI tự chạy tự chấm.

---

## 2. Tóm tắt cho member

Bộ TC làm tốt phần **hợp đồng route API**: tách rõ 3 route được cho qua và 2 route phải chặn, có cả TC cho **free kiểu cũ** (`plan_type=2`) lẫn **free kiểu mới** (`contract_type='free'`) — đúng tinh thần RULE-09, và có TC regression cho bot trả phí. Ghi chú kỹ thuật trong từng TC rất rõ, trace được về code.

Ba việc phải sửa trước vòng sau: (1) **route `backup.processing` khi gõ thẳng URL** — chính note của TC-PERM002-02 đã viết "điều hướng URL trực tiếp không bị nhánh này chặn" nhưng lại không có TC nào kiểm, đây là lỗ hổng quyền chứ không phải giả định để ghi chú rồi bỏ qua; (2) **bot chưa từng có mã sao chép** — Dev đã tự nêu rủi ro này và tự nói không kiểm chứng được, mà đây đúng là triệu chứng KH báo, nên bắt buộc phải có TC; (3) **luồng nghiệp vụ chính chưa được test** — cả fix này tồn tại để bot free lấy mã đi làm **nguồn** cho bot trả phí, nhưng không TC nào chạy trọn kịch bản đó.

Ngoài ra: cả 8 TC đều `Normal`/`Abnormal`, **không có TC `Boundary` nào**, trong khi 6/7 requirement Studio đánh `risk = High` — vi phạm RULE-01.

---

## 3. Coverage Matrix

> Cột `Exec` = `<số pass>/<số TC cover>`. TC mang mã quan điểm Studio không map được (`TOOL-*`) được đánh dấu `⚠️` — vẫn tính cover **impact** (vì nội dung TC thật sự chạm code path đó) nhưng **KHÔNG** tính cover **quan điểm** ở §7.F.1.

| Impact | Loại | Priority | TCs map (suy luận từ nội dung) | # TC | Exec | Status |
|---|---|---|---|---|---|---|
| **BUG** — regression #39230, chốt chặn `__construct` quá rộng | Fix | — | TC-TOOLKNOW002-01 ⚠️ | 1 | 1/1 | **RISK** — chỉ 1 TC, và TC đó mang mã không map được; thiếu case bot chưa có `transfer_code` (đúng triệu chứng KH) |
| **F1** — `__construct` + `FREE_PLAN_DENIED_ROUTES` | Function | Direct | TC-PERM002-01, TC-PERM002-02, TC-REGSHARED001-01 | 3 | 3/3 | **RISK** — chặn/cho qua đúng **5/6 route**; thiếu `backup.processing` |
| **F2** — route `backup.get-bot-data` | Function | Direct | TC-TOOLKNOW002-01 ⚠️, TC-PERM002-01 | 2 | 2/2 | **OK** |
| **F3** — route `backup.get-backup-history` | Function | Direct | TC-PERM002-01 | 1 | 1/1 | **RISK** — chỉ verify HTTP 200 ở tầng API, không TC nào xem lịch sử hiển thị đúng trên màn |
| **F4** — route `backup.create-transfer-code` | Function | Direct | TC-FUNC001-01, TC-PERM002-01 | 2 | 2/2 | **RISK** — chỉ happy path; thiếu abnormal (lỗi request), thiếu double-click, thiếu case mã đang rỗng |
| **F5** — route `backup.save-backup-history` (vẫn chặn) | Function | Direct | TC-TOOLVAL2001-01 ⚠️, TC-PERM002-02 | 2 | 2/2 | **OK** — chặn 2 tầng FE + BE, có đối chứng âm không tạo `backup_history` |
| **F6** — route `backup.processing` (trang tiến trình) | Function | Direct | — | **0** | — | **GAP** ⛔ — Studio tự ghi "chỉ 403 khi ajax, điều hướng URL trực tiếp không bị nhánh này chặn" mà không TC nào kiểm |
| **F7** — route `backup.check-processing` (vẫn chặn) | Function | Direct | TC-PERM002-02 | 1 | 1/1 | **OK** |
| **F8** — `BackupService::getBotData` (+ cờ `is_free_plan`) | Function | Direct | TC-TOOLKNOW002-01 ⚠️, TC-TOOLOLDREC001-01 ⚠️, TC-PERM002-01 | 3 | 3/3 | **OK** |
| **F9** — `Bots::isFreePlan` | Function | Indirect | TC-TOOLOLDREC001-01 ⚠️, TC-PERM002-01 | 2 | 2/2 | **RISK** — chỉ 2 trạng thái gói (free cũ, free mới); thiếu **hợp đồng hết hạn**, thiếu tách standard ⇄ pro |
| **F10** — `initBotData` / `startCreateCode` / `startCopy` (backup.js) | Function | Direct | TC-TOOLKNOW002-01 ⚠️, TC-FUNC001-01, TC-FUNC001-02, TC-TOOLOLDREC001-01 ⚠️, TC-TOOLVAL2001-01 ⚠️ | 5 | 5/5 | **RISK** — không TC nào chạy với **JS cũ còn trong cache** (DEPLOY-ASSET-001) |
| **F11** — `backup.blade.php` (2 chỗ khoá theo cờ mới) | Function | Direct | TC-TOOLOLDREC001-01 ⚠️, TC-REGSHARED001-01 | 2 | 2/2 | **OK** |
| **F12** — `BotRepository::findByIdWithColumn` / `updateTransferCode` | Function | Indirect | TC-TOOLKNOW002-01 ⚠️, TC-FUNC001-01 | 2 | 2/2 | **RISK** — không TC nào kiểm phạm vi `WHERE` trên 2 tài khoản |
| **D1** — `bots.transfer_code` (UPDATE) | Data | — | TC-FUNC001-01, TC-PERM002-01 | 2 | 2/2 | **RISK** ⛔ — có verify DB đổi giá trị, nhưng **thiếu TC kiểm `WHERE` scope trên 2 bot** (DATA-DB-001 bắt buộc với mọi UPDATE) |
| **D2** — `backup_history` KHÔNG được CREATE với bot free | Data | — | TC-TOOLVAL2001-01 ⚠️, TC-PERM002-02 | 2 | 2/2 | **OK** — có đối chứng âm rõ ràng |
| **D3** — response `get-bot-data` thêm `is_free_plan` | Data | — | TC-PERM002-01 | 1 | 1/1 | **RISK** — không TC nào kiểm client cũ ↔ server mới trong lúc release (DEPLOY-LIVE-001) |
| **T1** — Data Copy/Backup với bot **gói miễn phí** | Feature | **High** | TC-TOOLKNOW002-01 ⚠️, TC-FUNC001-01, TC-FUNC001-02, TC-TOOLOLDREC001-01 ⚠️ | 4 | 4/4 | **RISK** — thiếu **kịch bản nghiệp vụ chính**: bot free làm **nguồn** cho bot trả phí |
| **T2** — Plan gating màn Sao chép dữ liệu | Feature | **High** | TC-TOOLOLDREC001-01 ⚠️, TC-TOOLVAL2001-01 ⚠️, TC-PERM002-01, TC-PERM002-02 | 4 | 4/4 | **RISK** — hở route `backup.processing`; chưa có bảng plan-limit chính thức làm nguồn |
| **T3** — Data Copy với bot **có phí** (regression) | Feature | Medium | TC-REGSHARED001-01 | 1 | 1/1 | **RISK** — 1 TC, precondition "data sạch", gộp standard/pro làm một (AP-3) |
| **T4** — Nhận diện free **kiểu mới** | Feature | Medium | TC-TOOLOLDREC001-01 ⚠️ | 1 | 1/1 | **RISK** — chỉ 1 TC, và TC đó mang mã không map được |
| **T5** — Trang tiến trình sao chép `/basic/backup/processing/{id}` | Feature | Low–Medium | — | **0** | — | **GAP** — trùng với F6 |

### ORPHAN TCs

**Không có ORPHAN.** Cả 8 TC đều thuộc scope BUG / F* / D* / T* của `03-dev-impact.md`.

- Ghi chú AP-5: TC-FUNC001-02 (clipboard) nằm ở rìa scope — nút copy **không** bị fix chạm logic, chỉ được "mở lại" do route `get-bot-data` cho qua. Vẫn giữ vì nó verify đúng 1 trong 3 mục BA yêu cầu fill lại (comment Redmine journal #2), nhưng oracle của nó đang bị hạ cấp (xem §4.2).

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| **Fix shape** (đọc mục 2 dev-impact) | **Permission-gate scope narrowing** (chuyển từ chặn-toàn-controller sang **allow-list theo TÊN route**) **+ thêm cờ do server tính** (`is_free_plan`) cho FE dùng chung **+ thêm chốt chặn FE** ở `startCopy`. Bảng fix-shape khớp 3 dòng: `validate input / add check / thêm if` · `sửa hàm dùng chung` · `JS / asset / build`. |
| **Trigger space cần cover** | **6 route × 5 trạng thái gói.** Route: `get-bot-data` · `get-backup-history` · `create-transfer-code` (cho qua) — `save-backup-history` · `processing` · `check-processing` (chặn). Trạng thái gói: free cũ (`plan_type=2`) · free mới (`contract_type='free'`) · standard · pro · **hợp đồng hết hạn**. |
| **Số trigger TCs hiện cover** | **Route: 5/6** — thiếu `backup.processing`. **Trạng thái gói: 3/5** — thiếu tách standard ⇄ pro, thiếu hợp đồng hết hạn. |
| **KH report dạng** | **Symptom-only** — KH chỉ mô tả "コピーコードが表示がされません / 再発行ボタンを押しても空欄のまま". Không error code, không console log, không screenshot (Redmine #40151 **0 attachment**). |
| **Alternative root causes cần verify** | (1) **`bots.transfer_code` rỗng sẵn trong DB** → ô trống dù không có 403 — **chính Dev nêu là rủi ro và tự nói không kiểm chứng được**; (2) **JS cũ còn cache** → `initBotData` bản cũ không đọc `is_free_plan`, free kiểu mới vẫn lọt; (3) API trả 200 nhưng thiếu field → FE render rỗng im lặng. **Không alternative nào có TC.** |
| **Anti-patterns dính** | **AP-2** (symptom-only KH report) · **AP-3** (happy-path-only regression cho T3/T5) · **AP-4 một phần** (có commit hash `a0dbc96ebe` + branch nhưng **không có link PR/diff** để review verify fix shape thật) |

> **Kết luận fix-shape**: trigger space cover **5/6 route** và **3/5 trạng thái gói** → flag `[BLOCKER] FIX-SHAPE` cho route thiếu (§4.1 B1) và `[MAJOR] FIX-SHAPE` cho trạng thái gói thiếu (§4.2 M9).
>
> Điểm cộng: đây **không phải** generic catch-all (AP-1) — allow-list theo tên route là specific check, và Dev đã liệt kê đủ 3 route bị chặn, TCs cover 2/3. Nhưng chính vì là **specific check theo TÊN route** nên rủi ro đã chuyển sang chỗ khác: đổi tên route trong file định tuyến mà quên sửa hằng → chốt chặn hở im lặng. Dev tự nêu rủi ro này, **không TC nào canh gác nó**.

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- **[BLOCKER] FIX-SHAPE · GAP-F6 · PERM-002 — `backup.processing` gõ thẳng URL không bị chặn.**
  Note của TC-PERM002-02 ghi nguyên văn: *"Lưu ý backup.processing (GET view) chỉ 403 khi ajax; điều hướng URL trực tiếp không bị nhánh này chặn — xem assumption plan."* Đây là **giả định chưa được kiểm chứng nhưng lại được ghi như đã biết rồi bỏ qua**. `PERM-002` (Cao) yêu cầu rõ: *"dán URL của thao tác đã bị ẩn trên UI → phải trả 403"*, và `MAP-PERM-02` liệt kê đường truy cập bắt buộc thử gồm **gõ thẳng URL**. Bot free hiện có thể vào thẳng trang tiến trình sao chép — màn mà fix này chủ đích vẫn chặn.
  → **Đề xuất fix**: thêm **TC-PERM002-03** (gõ thẳng URL) + **TC-PERM002-04** (đổi param id sang bot khác). Nếu code thật sự không chặn được điều hướng trực tiếp → đây là **bug của fix**, phải trả lại Dev, không phải chỉ thiếu TC.

- **[BLOCKER] GAP-BUG · UI-003 / OUT-TRUTH-001 — không TC nào cho bot CHƯA CÓ mã sao chép.**
  Toàn bộ TC liên quan đến mã sao chép đều có precondition "**đã có** `transfer_code`" (TC-TOOLKNOW002-01: *"đã có transfer_code"*; TC-FUNC001-01: *"ghi lại copy code hiện tại"*). Nhưng Dev tự nêu ở mục rủi ro: *"Nếu bot chưa từng có mã sao chép thì ô mã vẫn trống cho tới khi người dùng bấm cấp lại mã… **không kiểm chứng được** vì không kết nối được MySQL dev."*
  Đây **đúng là triệu chứng KH báo** ("ô copy code trống, nhấn cấp lại vẫn trống"). Nếu vẫn còn bot rơi vào trạng thái này thì sau khi release KH vẫn thấy y hệt lỗi cũ, và QA không có TC nào để phân biệt "bug còn" với "trạng thái hợp lệ".
  → **Đề xuất fix**: thêm **TC-FUNC001-03** — bot free có ô mã trống → bấm 再発行 → mã phải hiện ra ngay. Đây là TC bắt buộc, không phải nice-to-have.

- **[BLOCKER] GAP · DATA-BACKUP-001 — kịch bản nghiệp vụ chính của fix hoàn toàn không được test.**
  Lý do tồn tại của fix (theo chính popup spec Dev trích): tài khoản miễn phí **VẪN lấy được mã sao chép để làm tài khoản NGUỒN copy sang tài khoản trả phí**. Nhưng không TC nào chạy trọn kịch bản đó: TC-REGSHARED001-01 dùng "bot nguồn hợp lệ" **không xác định gói**, và 7 TC còn lại chỉ dừng ở "mã có hiển thị / route có 403 hay không".
  → Kết quả: fix có thể "đúng ở tầng route" mà vẫn **sai ở tầng nghiệp vụ** (VD mã của bot free bị từ chối ở bước `コードを確認` phía bot đích vì một chốt chặn gói khác).
  → **Đề xuất fix**: thêm **TC-DATABACKUP001-01** — end-to-end: lấy mã ở bot free → đăng nhập bot trả phí → nhập mã → xác minh → chạy sao chép → dữ liệu về đích.

- **[BLOCKER] GAP · DATA-DB-001 — có UPDATE nhưng không TC nào kiểm phạm vi `WHERE` trên 2 tài khoản.**
  Fix **mở quyền gọi `create-transfer-code` cho nhóm tài khoản mới** (bot free) — đây là route **UPDATE** `bots.transfer_code`. `DATA-DB-001` (Cao) là **BẮT BUỘC với mọi chức năng có UPDATE hoặc DELETE**, và RULE-07 ghi rõ *"Tạo bản ghi trùng tên ở 2 tài khoản để kiểm chứng `WHERE`"*. Không TC nào làm việc này.
  → Rủi ro cụ thể: `updateTransferCode` thiếu điều kiện `bot_id` đủ chặt → bấm 再発行 ở bot A đổi luôn mã của bot B. Với bot free (số lượng lớn, nhiều bot/tài khoản) rủi ro này tăng.
  → **Đề xuất fix**: thêm **TC-DATADB001-01**.

- **[BLOCKER] GAP · DEPLOY-ASSET-001 — `backup.js` bị sửa nhưng không TC nào chạy với JS cũ còn trong cache.**
  `public/js/admin/backup/backup.js` nằm trong 4 file thay đổi. `DEPLOY-ASSET-001` (Cao) **BẮT BUỘC khi release có sửa file JS**, nghiệm thu bằng **F5 thường** (KHÔNG Ctrl+F5) trên browser còn cache bản cũ. Catalog D dòng `ENV-ASSET` cảnh báo production **user giữ cache lâu**.
  → Failure mode cụ thể và nghiêm trọng: `initBotData` bản **cũ** chỉ xét `plan == 2`, không đọc `is_free_plan`. User gói **free kiểu mới** giữ JS cũ → **không** bị khoá ô nhập mã nguồn, **không** hiện popup nâng cấp → đúng lỗ hổng mà fix này vá, vẫn còn nguyên sau release cho tới khi họ hard-refresh.
  → **Đề xuất fix**: thêm **TC-DEPLOYASSET001-01**.

- **[BLOCKER] GAP · CONC-001 — nút 再発行 vừa được mở cho bot free, không TC nào test double-click.**
  `CONC-001` (Cao) **BẮT BUỘC khi có nút thực thi hành động quan trọng**. 再発行 sinh mã mới và **làm mã cũ vô hiệu** — nếu double-click sinh 2 mã liên tiếp, user có thể copy mã hiển thị ở lần render đầu trong khi DB đã giữ mã thứ hai → bot đích nhập mã bị từ chối, tái tạo đúng cảm giác "mã không dùng được" mà KH đang than.
  → **Đề xuất fix**: thêm **TC-CONC001-01**.
  > 📌 *Leader cân nhắc*: nếu xác nhận `updateTransferCode` ghi đè cùng 1 row và FE luôn render theo response cuối, có thể **hạ xuống `[MAJOR]`**. Hiện flag BLOCKER theo đúng luật "quan điểm Cao + trigger khớp + GAP".

### 4.2 Major (nên fix)

**Nhóm A — độ tin cậy của kết quả "Đạt" (từ BƯỚC 0.6)**

- **[MAJOR] RULE-08 / ENV-003**: 8/8 TC chỉ chạy ở `env = local`, 0 TC ở dev/staging/production. Task là **plan gating theo gói cước** — thuộc đúng hạng mục `bill tiền` (`ENV-PAY`) mà Catalog D cấm kết luận từ môi trường test: *"dev/staging tài khoản test, production tài khoản thật"*. Trạng thái hợp đồng thật (`bot_slots` / `bot_contracts.contract_type`) trên production **không giống** local. → TC-TOOLOLDREC001-01 (free kiểu mới) và TC-REGSHARED001-01 (bot có phí) **chưa có giá trị nghiệm thu**. Yêu cầu chạy lại tối thiểu 2 TC này trên production, hoặc phiếu xác nhận không verify được + phương án giám sát.
- **[MAJOR] Ai chạy**: `last_exec.source = ai`, `by = pipeline` cho cả 8 TC, **25 giây cho toàn bộ 8 TC**. Nhóm rủi ro cao (phân quyền + gói cước) đang được AI tự sinh, tự chạy, tự chấm Đạt, chưa qua QA người nào. → Yêu cầu QA người chạy lại ít nhất các TC thuộc T1/T2.
- **[MAJOR] Tác giả TC**: 8/8 do AI sinh (`provenance.source = ai`), 0 TC do member viết, toàn bộ ở `status = draft`, `reviewState = leader`, `reviewed = false`.
- **[MAJOR] RULE-02 — evidence rỗng**: cả 8 TC có `Kết quả thực thi = Đạt` nhưng cột **`Evidence thực tế` trống hoàn toàn**, và cột `Ghi chú` **không ghi loại evidence bắt buộc**. RULE-02: *"Chỉ tick Đạt khi đã đính kèm đúng loại bằng chứng… Không chấp nhận 'đã xem, OK'."* → 8 kết quả Đạt hiện **chưa đủ điều kiện nghiệm thu**.
- **[MAJOR] `Trạng thái đánh giá spec` trống toàn bộ 8 TC** (`spec_status = null`). Trong khi `02-spec-reference.md` **không tồn tại** và spec duy nhất là text popup trong code → nguy cơ AI tự suy diễn hành vi mong đợi rồi tự cho Đạt. Mỗi TC phải ghi `Spec ghi rõ` / `Spec không ghi` / `Đã hỏi leader`.
- **[MAJOR] 3 mã quan điểm không map được**: `TOOL-KNOW-002`, `TOOL-OLDREC-001`, `TOOL-VAL2-001` (3/8 TC = 37,5%) không có trong `checklist-lme.md` lẫn `catalog-lme.md`. Theo luật, 3 TC này **không tính là cover quan điểm tầng 1** — kéo theo `COMPAT-LEGACY-001` và `T4` mất chỗ dựa duy nhất. → Leader quyết: gán lại sang mã tầng 1 trên Studio (gợi ý: `TOOL-KNOW-002`→`FUNC-001`, `TOOL-OLDREC-001`→`COMPAT-LEGACY-001`, `TOOL-VAL2-001`→`PERM-002`), hoặc bổ sung 3 mã này vào `checklist-lme.md` theo RULE-10.

**Nhóm B — fix-shape & anti-pattern (từ BƯỚC 3c)**

- **[MAJOR] AP-2 SYMPTOM-ONLY**: KH chỉ mô tả triệu chứng, không error code, Redmine 0 attachment. Dev tái hiện **1 root cause** (#39230 gate). TCs bám 100% vào root cause đó. Cần cover ≥ 2 root cause khả dĩ khác — xem 3 alternative ở §3.5, trong đó (1) và (2) đã thành BLOCKER riêng.
- **[MAJOR] AP-3 HAPPY-PATH-ONLY REGRESSION**: T3 (bot có phí) chỉ có 1 TC với precondition sạch; T5 (trang tiến trình) 0 TC. Regression phải verify **trạng thái edge cũ không vỡ thêm**, không chỉ "happy path còn chạy".
- **[MAJOR] AP-4 (một phần)**: mục "Commit / Pull Request" chỉ có commit hash `a0dbc96ebe` + branch, **không có link PR/diff xem được**. Không verify được fix shape thật (allow-list có đúng 3 route không, `updateTransferCode` có đủ `WHERE` không). → Yêu cầu Dev cung cấp link diff.
- **[MAJOR] FIX-SHAPE — trạng thái gói cover 3/5** (`PAY-LIMIT-001`, Cao): thiếu **hợp đồng hết hạn** (khác free — `isFreePlan` xử lý thế nào?) và **standard ⇄ pro chưa tách** (TC-REGSHARED001-01 gộp "standard/pro" thành 1 TC). `PAY-LIMIT-001` yêu cầu **bảng plan-limit chính thức** làm nguồn — hiện không có; `MAP-PLAN-06` cảnh báo *"bug external link từng lọt vì chỉ test trên gói Standard"*.
- **[MAJOR] REG-SHARED-001** (Cao): Dev khẳng định đã "quét ngang: đây là màn DUY NHẤT chặn cả màn ở phần khởi tạo" nhưng **không cung cấp danh sách màn** đã quét. REG-SHARED-001 yêu cầu evidence là *"danh sách nơi ảnh hưởng (dev cung cấp) + kết quả test từng nơi"*. Bug này thuộc dạng **phân quyền enforce ở tầng API** → phải rà các màn sibling có plan gating **ở tầng API**, không chỉ nhìn UI. → Yêu cầu Dev nộp danh sách; thêm **TC-REGSHARED001-02**.
- **[MAJOR] OUT-TRUTH-001** (Cao): bug gốc là **lỗi im lặng** (403 nhưng UI không báo gì — Dev ghi *"giao diện chỉ ghi log lỗi ngầm, không báo gì"*). Fix thêm deny modal cho **đúng 1 nhánh** (`startCopy` với bot free). Không TC nào verify UI báo lỗi khi `create-transfer-code` / `get-bot-data` **thất bại vì lý do khác** (500, mất mạng). Nguy cơ: hình thái lỗi im lặng vẫn còn nguyên ở các nhánh khác. → Thêm **TC-FUNC001-04**.
- **[MAJOR] DEPLOY-LIVE-001** (Cao): response `get-bot-data` **đổi payload** (thêm `is_free_plan`), release không lock maintain. Trong cửa sổ release: client cũ ↔ server mới, và server cũ ↔ client mới (`is_free_plan` undefined → rơi về `plan == 2` → free kiểu mới lọt). Không TC nào cover. Gộp chung TC với DEPLOY-ASSET-001 được.
- **[MAJOR] PAY-PLAN-001** (Cao): không TC nào cho **chuyển đổi gói**. Dev tự nêu kịch bản *"bot đang chạy sao chép rồi bị hạ xuống gói miễn phí giữa chừng thì không xem được tiến trình"* và tự kết luận *"giống hệt trước khi fix, không phải hồi quy mới"* — kết luận này **chưa được kiểm chứng bằng TC nào**. Chiều ngược lại (free → nâng cấp lên trả phí) cũng cần verify màn mở khoá ngay, không kẹt cache FE.
- **[MAJOR] PERM-001** (Cao): `__construct` bị **viết lại** — đây là điểm vào chặn của toàn controller. Không có bằng chứng nó từng chứa role check, nhưng cũng **không có TC regression** xác nhận staff **không có quyền** dùng màn Sao chép dữ liệu vẫn bị chặn sau khi viết lại. → Thêm **TC-PERM001-01**.
- **[MAJOR] SEC-001 / PERM-003 / MAP-PERM-03**: `create-transfer-code` là endpoint **mutate credential** vừa được mở cho nhóm tài khoản mới. Không TC nào thử **đổi param bot_id sang bot của tổ chức khác**. → Gộp vào **TC-PERM002-04**.

**Nhóm C — chất lượng bộ TC**

- **[MAJOR] RULE-01 — 0/8 TC là `Boundary`** (6 Normal + 2 Abnormal) trong khi **6/7 requirement Studio đánh `risk = High`**. Cụ thể: `FUNC-001` (Cao) có 2 TC đều Normal — thiếu Abnormal + Boundary; `PERM-002` (Cao) có Normal + Abnormal — thiếu Boundary. Không TC nào ghi lý do miễn trừ.
- **[MAJOR] TC-FUNC001-02 — oracle bị hạ cấp, TC gần như không verify điều nó tuyên bố.** Note Studio: *"Đọc clipboard headless có thể hạn chế; oracle tối thiểu là toast + copyCode không rỗng."* Nghĩa là TC tên "copy vào clipboard" nhưng thực tế **chỉ kiểm toast + ô mã không rỗng** — không hề kiểm nội dung clipboard. Đã chấm `Đạt` với oracle hạ cấp. → Đổi `exec_mode` sang `manual` cho phần clipboard, hoặc sửa tiêu đề TC cho khớp điều thật sự được kiểm.
- **[MAJOR] TC-TOOLVAL2001-01 — không đi đường user thật.** Precondition ghi: *"Ô nguồn bị disable nên TC ép gọi hành động khởi chạy (startCopy)"*. Nghĩa là TC **gọi hàm JS trực tiếp**, không phải thao tác user. Chốt chặn FE tầng 1 vì thế chỉ được verify ở mức hàm, chưa chứng minh user thật không có đường nào chạm tới. → Bổ sung đường vào thật (nếu tồn tại) hoặc ghi rõ giới hạn ở `Ghi chú`.
- **[MAJOR] Auto-fill chưa được tester verify** — cả `01-bug-task.md` và `03-dev-impact.md` có `Auto-filled: 2026-08-25 by /new-task` nhưng checkbox "Tester verify auto-fill chính xác" **chưa tick** ở cả 2 file. F/D/T trong coverage matrix trên đây suy ra từ dữ liệu **chưa được người xác nhận**. Tester phải đọc lại Redmine #40151 và tick trước khi report này có giá trị nghiệm thu.
- **[MAJOR] `03-dev-impact.md` mục 4.2 sai** — Dev ghi *"Không có data impact"*, nhưng fix **mở quyền UPDATE `bots.transfer_code` cho nhóm tài khoản mới** (đã ghi lại thành **D1** khi dựng file 03). Đánh giá sai mục 4.2 chính là lý do DATA-DB-001 bị bỏ qua khi sinh TC. → Yêu cầu Dev sửa lại mục 4.2.

### 4.3 Minor (có thể fix sau)

- **[MINOR] RULE-02 — loại evidence**: cột `Ghi chú` của 8 TC ghi note kỹ thuật (oracle, tên route) nhưng **không ghi loại bằng chứng bắt buộc** phải đính khi chấm Đạt (screenshot màn nào, response API nào, ảnh query DB nào).
- **[MINOR] DATA-AUDIT-001 — cần hỏi Dev**: 再発行 đổi một giá trị mang tính credential, nay mở cho nhóm tài khoản rộng hơn. Màn này có ghi `操作履歴` không? Nếu có → cần TC verify đủ 4 thông tin (ai/khi nào/hành động/cũ→mới). Nếu không có → xác nhận là đúng thiết kế. **Chưa đủ bằng chứng để flag cao hơn.**
- **[MINOR] DATA-001 — phản ánh đa màn**: `transfer_code` có hiển thị ở màn nào khác ngoài màn Sao chép dữ liệu không (cài đặt bot, danh sách bot)? Nếu có, sau 再発行 phải đồng bộ. Chưa có input để kết luận → `Input thiếu`.
- **[MINOR] TC-PERM002-02 dùng `id bất kỳ`** cho `check-processing` — dữ liệu test không realistic, và trộn 2 mục đích (chặn theo gói ⇄ id không tồn tại). Nên tách hoặc chỉ định id cụ thể.

### 4.4 Nit (gợi ý)

- **[NIT]** TC-PERM002-01 gộp 3 route vào 1 TC, TC-PERM002-02 gộp 2 route — vi phạm nhẹ B.2 (atomic). Chấp nhận được vì cùng 1 hợp đồng phân quyền, nhưng khi 1 route fail sẽ khó thấy route nào. Cân nhắc tách khi có thời gian.
- **[NIT]** `UI-INPUT-001`: ô nhập mã nguồn nay bị `:disabled` theo cờ mới — có thể thêm case paste bằng **chuột phải** vào ô đó khi bot vừa nâng cấp gói (button disable → enable). Ưu tiên thấp.
- **[NIT]** RULE-11: các mục §4 `checklist-lme.md` (ADM-01 "bộ lọc phải đúng ngay lần đầu"…) **không** được dùng để flag ở report này — đúng luật, chỉ ghi nhận là đã cân nhắc và loại.

---

## 5. TCs đề xuất bổ sung

> 12 TC lấp các GAP ở §3 + §7.F.1. Dùng **đúng 16 cột canonical**. Viết từ **góc nhìn manual tester** — thao tác trên màn + quan sát; bước kiểm DB chỉ dùng ở nơi RULE-07 / DATA-DB-001 bắt buộc.
> TC No. đã tránh trùng với 8 TC hiện có.

| TC No. | Mã quan điểm liên kết | Loại case | Tiêu đề test case | Điều kiện tiền đề | Các bước thực hiện | Dữ liệu test/input | Kết quả mong đợi | Kết quả thực thi | Evidence thực tế | Môi trường test | Người thực hiện | Ngày thực hiện | Số ticket bug | Trạng thái đánh giá spec | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-PERM002-03 | PERM-002 | Abnormal | Bot free gõ thẳng URL trang tiến trình sao chép phải bị chặn | Đăng nhập admin bằng tài khoản có bot gói miễn phí. Có sẵn 1 id tiến trình sao chép hợp lệ (lấy từ bot trả phí đã từng chạy sao chép). | 1. Chọn bot free ở context bot<br>2. Gõ thẳng vào thanh địa chỉ trình duyệt `/basic/backup/processing/{id}` rồi Enter (KHÔNG đi qua nút trên màn)<br>3. Quan sát màn hiện ra<br>4. Lặp lại bước 2 nhưng vào từ menu favourite và từ hyperlink nếu có đường dẫn tới màn này | id tiến trình hợp lệ của bot khác | Trình duyệt KHÔNG mở được trang tiến trình. Phải thấy màn báo không đủ quyền hoặc bị điều hướng về màn Sao chép dữ liệu kèm popup cần nâng cấp. Tuyệt đối không hiển thị nội dung tiến trình sao chép của bot khác. | Chưa test | | STAGING + PRODUCTION | | | | Spec không ghi — đã hỏi leader | **Lấp GAP-F6 / T5** (BLOCKER §4.1). Studio note của TC-PERM002-02 tự ghi route này chỉ 403 khi ajax. Evidence bắt buộc: screenshot màn kết quả + tab Network thể hiện status code. Nếu vào được → là **bug của fix**, raise ticket ngay |
| TC-PERM002-04 | PERM-002 | Boundary | Bot free gọi route tiến trình với id của bot khác và id không tồn tại | Có session admin hợp lệ, bot free ở context. Biết trước 1 id thuộc bot của tổ chức khác. | 1. Với bot free ở context, gọi `check-processing` lần lượt với: id của bot cùng tổ chức, id thuộc tổ chức KHÁC, id không tồn tại, id để trống<br>2. Ghi lại status code và nội dung message trả về từng lần<br>3. Đối chiếu message có lộ thông tin bot khác không | 4 giá trị id: hợp lệ cùng tổ chức, thuộc tổ chức khác, không tồn tại, rỗng | Cả 4 trường hợp đều bị từ chối. Message trả về phải giống nhau về mặt thông tin (không phân biệt được id nào có thật) và KHÔNG chứa tên bot, tên tổ chức hay bất kỳ dữ liệu nào của bot khác. | Chưa test | | STAGING | | | | Spec không ghi — đã hỏi leader | **Lấp GAP-F6 + SEC-001/PERM-003/MAP-PERM-03** (§4.2 nhóm B). Đồng thời là TC **Boundary** còn thiếu của PERM-002 → đóng RULE-01 cho quan điểm này. Evidence: bảng 4 dòng id với status code + message |
| TC-FUNC001-03 | FUNC-001 | Abnormal | Bot free chưa từng có mã sao chép: ô mã trống rồi bấm cấp lại phải sinh ra mã | Đăng nhập admin, chọn 1 bot gói miễn phí **chưa từng có mã sao chép** (nhờ Dev/DBA dựng hoặc xoá giá trị mã của 1 bot test). | 1. Mở màn 「データコピー」 với bot này<br>2. Quan sát ô 「このアカウントのコピーコード」 khi màn vừa tải xong<br>3. Bấm 「コピーコードの再発行」 rồi bấm 「再発行する」 trong modal<br>4. Quan sát lại ô mã sao chép và thông báo<br>5. F5 tải lại màn và quan sát ô mã lần nữa | Bot free có mã sao chép đang rỗng | Bước 2: ô mã trống nhưng màn vẫn tải bình thường, các khối khác (danh sách dữ liệu, tài khoản đích) vẫn hiển thị, KHÔNG có lỗi 403. Bước 4: mã mới hiện ra ngay trong ô, có toast báo đã lưu. Bước 5: sau F5 mã vẫn còn đúng giá trị đó. | Chưa test | | STAGING + PRODUCTION | | | | Spec không ghi — đã hỏi leader | **Lấp GAP-BUG** (BLOCKER §4.1). Đây đúng luồng KH báo lỗi và là **alternative root cause #1** mà Dev tự nêu nhưng không kiểm chứng được. Evidence: screenshot ô mã trước/sau khi bấm cấp lại + sau F5 |
| TC-FUNC001-04 | FUNC-001 | Abnormal | Cấp lại mã thất bại phải báo lỗi rõ trên màn, không im lặng | Bot free đang ở màn データコピー. Chuẩn bị công cụ mô phỏng lỗi mạng (DevTools > Network > Offline hoặc chặn request). | 1. Mở DevTools tab Network, bật chế độ Offline (hoặc chặn riêng request cấp lại mã)<br>2. Bấm 「コピーコードの再発行」 rồi 「再発行する」<br>3. Quan sát màn hình trong 10 giây<br>4. Tắt Offline, F5 và kiểm tra mã sao chép có bị đổi không<br>5. Lặp lại bước 1-3 nhưng mô phỏng server trả lỗi 500 | Không nhập; mô phỏng mất mạng và lỗi 500 | Phải hiện thông báo lỗi rõ ràng cho user (không phải chỉ ghi log ngầm), modal không đóng im lặng, nút không kẹt ở trạng thái loading vô hạn. Sau khi tắt Offline và F5: mã sao chép giữ NGUYÊN giá trị cũ, không bị đổi nửa vời. | Chưa test | | STAGING | | | | Spec không ghi — đã hỏi leader | **Lấp GAP OUT-TRUTH-001 + UI-003** (§4.2 nhóm B). Bug gốc chính là **lỗi im lặng**; fix mới chỉ vá 1 nhánh startCopy. Evidence: video thao tác + screenshot tab Network |
| TC-FUNC001-05 | FUNC-001 | Boundary | Bot ở trạng thái gói biên: hợp đồng vừa hết hạn và vừa nâng cấp xong | Chuẩn bị 2 bot test: (A) hợp đồng vừa hết hạn trong ngày, (B) vừa nâng cấp từ miễn phí lên trả phí xong. | 1. Mở màn データコピー với bot A, quan sát: có popup nâng cấp không, ô nhập mã nguồn có bị khoá không, ô mã sao chép của chính bot có hiện không<br>2. Thử bấm cấp lại mã trên bot A<br>3. Chuyển sang bot B, mở lại màn (KHÔNG hard refresh), quan sát 3 điểm như bước 1<br>4. Với bot B, nhập mã nguồn hợp lệ và bấm xác nhận mã | Bot hợp đồng vừa hết hạn; bot vừa nâng cấp lên trả phí | Bot A: được đối xử đúng theo quy định của hợp đồng hết hạn (Leader chốt trước với BA là giống gói miễn phí hay chặn hoàn toàn) và hành vi phải NHẤT QUÁN giữa popup, trạng thái ô nhập và kết quả gọi route. Bot B: KHÔNG còn popup nâng cấp, ô nhập mã nguồn mở khoá được ngay mà không cần hard refresh, xác nhận mã nguồn chạy bình thường. | Chưa test | | PRODUCTION | | | | Spec không ghi — đã hỏi leader | **Lấp RULE-01 (Boundary còn thiếu của FUNC-001) + PAY-PLAN-001 + PAY-LIMIT-001** (§4.2). `isFreePlan` xử lý hợp đồng hết hạn thế nào hiện **chưa có spec** → phải hỏi BA trước khi chạy. Evidence: screenshot 3 điểm quan sát cho từng bot |
| TC-DATADB001-01 | DATA-DB-001 | Normal | Cấp lại mã ở bot A không được làm đổi mã của bot B | Tài khoản admin quản lý ít nhất 2 bot gói miễn phí (A và B), cả hai đều đang có mã sao chép. Ghi lại mã hiện tại của CẢ HAI bot. | 1. Ghi lại mã sao chép đang hiển thị của bot A và bot B (chụp màn từng bot)<br>2. Chọn bot A, bấm cấp lại mã, ghi lại mã mới của A<br>3. Chuyển sang bot B, F5 màn データコピー, quan sát ô mã của B<br>4. Nhờ Dev/DBA chạy đối chiếu giá trị mã sao chép của cả 2 bot trong dữ liệu trước và sau thao tác<br>5. Lặp lại bước 2-4 nhưng cấp lại mã ở bot B và kiểm bot A | 2 bot free cùng chủ, cả 2 đều có sẵn mã sao chép | Mã của bot A đổi sang giá trị mới. Mã của bot B **giữ nguyên y hệt** giá trị ban đầu ở cả màn hình lẫn dữ liệu. Đối chiếu dữ liệu xác nhận chỉ đúng 1 bản ghi bị thay đổi. | Chưa test | | STAGING + PRODUCTION | | | | Spec ghi rõ | **Lấp GAP-D1 / DATA-DB-001** (BLOCKER §4.1). RULE-07 bắt buộc kiểm phạm vi ghi trên 2 tài khoản khi có UPDATE. Evidence: ảnh chụp mã 2 bot trước/sau + kết quả đối chiếu dữ liệu kèm câu truy vấn. **RULE-01**: quan điểm Cao nhưng tạm chỉ đề xuất 1 Normal — Abnormal/Boundary của DATA-DB-001 đã nằm ở TC-PERM002-04 và TC-CONC001-01 |
| TC-DEPLOYASSET001-01 | DEPLOY-ASSET-001 | Abnormal | Browser còn cache JS cũ: bot free kiểu mới vẫn phải bị khoá sau khi F5 thường | Có browser đã mở màn データコピー **TRƯỚC** khi release bản fix (để giữ cache file backup.js cũ). Có 1 bot gói miễn phí **kiểu mới**. | 1. Trước release: mở màn データコピー bằng bot bất kỳ để browser cache file JS, KHÔNG đóng tab<br>2. Release bản fix lên môi trường<br>3. Trên đúng browser đó, chuyển sang bot free kiểu mới và **chỉ bấm F5 thường** (TUYỆT ĐỐI không Ctrl+F5)<br>4. Quan sát: popup nâng cấp có bật không, ô nhập mã nguồn có bị khoá không<br>5. Mở DevTools tab Network, kiểm file backup.js trả về status code nào và có query version mới không | Bot free kiểu mới; browser giữ cache JS bản cũ | Sau F5 thường, màn phải chạy bằng JS bản MỚI: popup nâng cấp tự bật, ô nhập mã nguồn bị khoá. Tab Network cho thấy backup.js trả 200 với version mới, không có file nào 404. Nếu popup không bật hoặc ô nhập vẫn gõ được thì lỗ hổng free kiểu mới VẪN CÒN sau release. | Chưa test | | PRODUCTION | | | | Spec không ghi — đã hỏi leader | **Lấp GAP DEPLOY-ASSET-001 + DEPLOY-LIVE-001** (BLOCKER §4.1). Catalog D dòng ENV-ASSET: production user giữ cache lâu. Evidence: screenshot DevTools Network (version + status) + screenshot màn sau F5 thường |
| TC-DATABACKUP001-01 | DATA-BACKUP-001 | Normal | Bot free làm NGUỒN: bot trả phí dùng mã của bot free để sao chép dữ liệu sang | Có 2 bot: (A) gói miễn phí, đã dựng sẵn dữ liệu nhận biết được (vài tag, template, kịch bản đặt tên riêng); (B) gói trả phí, dùng làm đích. Có quyền đăng nhập cả hai. | 1. Đăng nhập bot A (free), mở màn データコピー, copy mã sao chép của A<br>2. Chuyển sang bot B (trả phí), mở màn データコピー<br>3. Dán mã của bot A vào ô 「コピー元アカウントのコピーコード」, bấm 「コードを確認」<br>4. Quan sát thông tin tài khoản nguồn hiện ra có đúng là bot A không<br>5. Xác nhận và chạy sao chép, chờ tiến trình hoàn tất<br>6. Vào các màn tương ứng của bot B kiểm dữ liệu đã đặt tên riêng ở bước chuẩn bị có sang đủ không | Mã sao chép của bot gói miễn phí; dữ liệu mẫu đặt tên nhận biết được | Bước 3-4: mã của bot free được **chấp nhận**, thông tin nguồn hiển thị đúng tên bot A, không bị chặn bằng lý do gói cước. Bước 5: tiến trình chạy tới hoàn tất. Bước 6: dữ liệu mẫu của bot A xuất hiện đầy đủ và đúng nội dung ở bot B. | Chưa test | | STAGING + PRODUCTION | | | | Spec ghi rõ | **Lấp GAP kịch bản nghiệp vụ chính** (BLOCKER §4.1). Đây là lý do tồn tại của fix theo popup spec (`backup.blade.php` dòng 352) và theo comment BA Redmine journal #2. Evidence: screenshot từng bước + đối chiếu danh sách dữ liệu ở bot B sau khi copy |
| TC-CONC001-01 | CONC-001 | Abnormal | Double-click nút cấp lại mã chỉ được sinh đúng 1 mã | Bot free đang ở màn データコピー, đã ghi lại mã hiện tại. Mở sẵn DevTools tab Network để đếm số request. | 1. Bấm 「コピーコードの再発行」 để mở modal<br>2. Double-click thật nhanh vào nút 「再発行する」<br>3. Đếm số request cấp lại mã phát ra trong tab Network<br>4. Quan sát mã hiển thị trên màn<br>5. F5 và so mã trên màn với mã vừa thấy ở bước 4<br>6. Lặp lại kịch bản nhưng mở màn データコピー trên 2 tab của cùng bot và bấm cấp lại gần như đồng thời ở cả 2 tab | Không nhập; thao tác double-click và 2 tab song song | Chỉ đúng **1** request được xử lý (nút phải bị khoá sau cú click đầu, hoặc request thứ 2 bị từ chối). Mã hiển thị trên màn sau khi F5 **trùng khớp** với mã đã hiện ở bước 4 — không có chuyện màn hiện mã cũ trong khi dữ liệu đã giữ mã mới hơn. Kịch bản 2 tab: chỉ 1 tab thao tác thành công hoặc cả 2 tab cuối cùng cùng hiển thị 1 mã duy nhất. | Chưa test | | STAGING | | | | Spec không ghi — đã hỏi leader | **Lấp GAP CONC-001** (BLOCKER §4.1, có thể hạ MAJOR — xem ghi chú §4.1). Ứng với MAP-PLAN-04 (2 tab) và MAP-PLAN-05 (double click). Evidence: screenshot tab Network đếm số request + mã trước/sau F5 |
| TC-PAYLIMIT001-01 | PAY-LIMIT-001 | Normal | Ma trận gói cước với 6 đường của màn Sao chép dữ liệu | Có bảng plan-limit chính thức do PM/BA cung cấp cho màn Sao chép dữ liệu. Chuẩn bị 5 bot: free cũ, free mới, standard, pro, hợp đồng hết hạn. | 1. Với TỪNG bot trong 5 bot, mở màn データコピー và ghi lại: popup nâng cấp có bật không, ô mã sao chép của chính bot có hiện không, nút cấp lại mã dùng được không, ô nhập mã nguồn có bị khoá không<br>2. Với từng bot, thử chạy sao chép và ghi lại kết quả (chạy được hay bị chặn, chặn ở FE hay sau khi gửi request)<br>3. Với từng bot, thử mở trang tiến trình sao chép bằng cách gõ thẳng URL<br>4. Lập bảng 5 bot x 4 điểm quan sát và đối chiếu với bảng plan-limit chính thức | 5 bot đại diện 5 trạng thái gói | Toàn bộ ô trong bảng khớp 100% với bảng plan-limit chính thức. Đặc biệt: standard và pro phải được kiểm **riêng từng gói** chứ không gộp; bot hợp đồng hết hạn có hành vi nhất quán giữa cả 4 điểm quan sát. | Chưa test | | PRODUCTION | | | | Spec không ghi — đã hỏi leader | **Lấp GAP PAY-LIMIT-001** (§4.2 nhóm B). MAP-PLAN-06 cảnh báo bug từng lọt vì chỉ test gói Standard. **Chặn trước khi chạy**: phải có bảng plan-limit chính thức, hiện `02-spec-reference.md` chưa có. Evidence: bảng ma trận 5x4 đã điền + screenshot từng ô khác kỳ vọng |
| TC-REGSHARED001-02 | REG-SHARED-001 | Normal | Rà các màn khác có chặn theo gói cước ở tầng API | Có **danh sách màn/route áp dụng chặn theo gói** do Dev cung cấp (yêu cầu Dev nộp trước khi chạy TC này). Có 1 bot gói miễn phí. | 1. Nhận danh sách màn có chặn theo gói từ Dev<br>2. Với bot free, mở lần lượt TỪNG màn trong danh sách và ghi lại màn có tải được dữ liệu không, có hiện popup nâng cấp không<br>3. Với mỗi màn, thử gọi thẳng đường lấy dữ liệu và đường thực thi ở **tầng API** (không chỉ nhìn UI ẩn hay hiện)<br>4. Đối chiếu: màn nào chặn cả màn ở phần khởi tạo giống lỗi #39230 cũ | Bot gói miễn phí; danh sách màn do Dev cung cấp | Không màn nào còn chặn TOÀN BỘ ở phần khởi tạo theo kiểu #39230. Với mỗi màn, hành vi ở tầng API khớp với hành vi hiển thị trên UI — không có màn nào ẩn nút trên UI nhưng vẫn cho gọi API, và ngược lại không có màn nào chặn nhầm đường chỉ đọc dữ liệu. | Chưa test | | STAGING | | | | Spec không ghi — đã hỏi leader | **Lấp GAP REG-SHARED-001** (§4.2 nhóm B). Evidence bắt buộc theo quan điểm: **danh sách nơi ảnh hưởng do Dev cung cấp** + kết quả test từng nơi. Dev hiện mới khẳng định miệng "đã quét ngang" mà chưa nộp danh sách. `regression` |
| TC-PERM001-01 | PERM-001 | Abnormal | Staff không có quyền vẫn phải bị chặn khỏi màn Sao chép dữ liệu sau khi sửa chốt chặn | Có ma trận quyền của màn Sao chép dữ liệu (yêu cầu từ BA nếu chưa có). Chuẩn bị tài khoản staff KHÔNG được cấp quyền màn này, trên 1 bot gói trả phí. | 1. Đăng nhập bằng tài khoản staff không có quyền<br>2. Kiểm tra menu: mục Sao chép dữ liệu có bị ẩn không<br>3. Gõ thẳng URL màn データコピー vào thanh địa chỉ<br>4. Thử gọi thẳng đường lấy dữ liệu màn và đường cấp lại mã ở tầng API<br>5. Lặp lại bước 1-4 với bot gói miễn phí | Tài khoản staff không có quyền màn Sao chép dữ liệu | Staff không quyền bị chặn ở **cả 3 đường**: menu ẩn, gõ URL trực tiếp bị từ chối, gọi API trực tiếp bị từ chối. Kết quả phải giống hệt trên cả bot trả phí lẫn bot miễn phí — việc nới chốt chặn theo gói KHÔNG được vô tình mở quyền cho staff thiếu quyền. | Chưa test | | STAGING | | | | Spec không ghi — đã hỏi leader | **Lấp GAP PERM-001** (§4.2 nhóm B). `__construct` bị viết lại nên cần regression tầng quyền theo role, độc lập với quyền theo gói. Evidence: screenshot menu + status code khi gõ URL và gọi API. `regression` |

### Trạng thái đẩy lên Studio

**Đã push cả 12 TC lên MCP LME TEST STUDIO task #201 ngày 2026-08-25** qua `testcase_create` (`client_ref` = TC No. → idempotent, chạy lại không sinh trùng).

| TC No. (report) | Studio `id` | Studio `temp_id` | `exec_mode` | `env_scope` | Ưu tiên |
|---|---|---|---|---|---|
| TC-PERM002-03 | 13283 | NEW-26 | manual | staging, prd | High |
| TC-PERM002-04 | 13284 | NEW-27 | manual | staging | High |
| TC-FUNC001-03 | 13285 | NEW-28 | manual | staging, prd | High |
| TC-FUNC001-04 | 13286 | NEW-29 | manual | staging | Medium |
| TC-FUNC001-05 | 13287 | NEW-30 | manual | prd | Medium |
| TC-DATADB001-01 | 13288 | NEW-31 | manual | staging, prd | High |
| TC-DEPLOYASSET001-01 | 13289 | NEW-32 | manual | prd | High |
| TC-DATABACKUP001-01 | 13290 | NEW-33 | manual | staging, prd | High |
| TC-CONC001-01 | 13291 | NEW-34 | manual | staging | High |
| TC-PAYLIMIT001-01 | 13292 | NEW-35 | manual | prd | Medium |
| TC-REGSHARED001-02 | 13293 | NEW-36 | manual | staging | Medium |
| TC-PERM001-01 | 13294 | NEW-37 | manual | staging | Medium |

**Ba quyết định khi push — Leader xem lại nếu không đồng ý:**

1. **Toàn bộ 12 TC đặt `exec_mode = manual`** (8 TC gốc đều là `auto`). Lý do: các TC này cần con người dựng env mà pipeline không tự làm được — 2 tài khoản trở lên, tài khoản staff, 5 trạng thái gói, browser giữ cache JS qua mốc release, DevTools Offline, đối chiếu dữ liệu DB. Đặt `manual` cũng chặn pipeline AI tự chạy tự chấm Đạt — đúng vấn đề đã nêu ở §4.2 nhóm A.
2. **`env_scope` ghi rõ `prd`** cho 5 TC thuộc diện RULE-08 (TC-FUNC001-05, TC-DEPLOYASSET001-01, TC-PAYLIMIT001-01 và 2 TC dùng chung `staging, prd`), thay vì `["all"]` như 8 TC gốc — để không lặp lại tình trạng chạy xong ở `local` rồi coi là đã nghiệm thu.
3. **`viewpoint` dùng mã tầng 1** của `checklist-lme.md` (PERM-002, FUNC-001, DATA-DB-001, DEPLOY-ASSET-001, DATA-BACKUP-001, CONC-001, PAY-LIMIT-001, REG-SHARED-001, PERM-001) — không dùng mã `TOOL-*` nội bộ, để `/review-tc` vòng sau map được coverage.

> ⚠️ **Chưa làm** (cần Leader/QA quyết): 3 TC gốc mang mã `TOOL-*` (Studio #12738, #12741, #12742) **vẫn giữ nguyên mã cũ** — tôi không sửa TC người khác đã tạo. Muốn đóng `[MAJOR]` ở §4.2 thì gán lại mã trên Studio bằng `testcase_update`, hoặc bổ sung 3 mã đó vào `checklist-lme.md` theo RULE-10.
>
> Task #201 giờ có **20 TC** (8 gốc `auto` đã chạy pass ở local + 12 mới `manual` chưa chạy). `exec` của task sẽ hiện 8/20 đã chạy.

---

## 6. Spec update needed

- [ ] Không cần update spec
- [x] **Cần update spec** — chi tiết:

1. **Thiếu hẳn `02-spec-reference.md` cho màn Sao chép dữ liệu.** Spec duy nhất đang được viện dẫn là **text popup nằm trong code** (`resources/views/basic/backup/backup.blade.php` dòng 352) do Dev trích lại. Không có tài liệu nào chốt: gói miễn phí được làm gì / không được làm gì trên màn này.
   - Người chịu trách nhiệm: **BA (Nguyen Ngoc Hai)** — người đã viết comment yêu cầu fill lại 3 mục ở Redmine journal #2.
   - Nội dung cần chốt: bảng **plan-limit chính thức** cho màn Sao chép dữ liệu, theo 5 trạng thái gói × 6 đường (3 đọc/cấp mã + 3 thực thi). Đây là **input chặn** của TC-PAYLIMIT001-01.

2. **Hành vi của hợp đồng HẾT HẠN chưa được định nghĩa.** `Bots::isFreePlan` hiện gộp free cũ + free mới; không rõ hợp đồng hết hạn có rơi vào nhóm này không. Ảnh hưởng trực tiếp TC-FUNC001-05.
   - Người chịu trách nhiệm: BA + Dev.

3. **Hành vi trang tiến trình khi hạ gói giữa chừng.** Dev tự nhận định *"giống hệt trước khi fix, không phải hồi quy mới"* — cần BA xác nhận đây là hành vi **được chấp nhận** hay là nợ kỹ thuật cần ticket riêng.
   - Người chịu trách nhiệm: BA.

4. **Sửa mục 4.2 của `03-dev-impact.md`** — Dev ghi "không có data impact" là không chính xác: fix mở quyền UPDATE `bots.transfer_code` cho nhóm tài khoản mới (D1).
   - Người chịu trách nhiệm: Dev / AI auto-fixbug.

---

## 7. Checklist đã chạy

- [x] **A. Coverage** — chạy đủ A.1→A.6. **Fail**: A.2 (F6 GAP), A.3 (D1 thiếu kiểm `WHERE` scope), A.4 (T5 GAP, T3 chỉ happy path), A.6 (trigger space 5/6 route, 3/5 trạng thái gói). Pass: A.5 (không ORPHAN).
- [x] **B. Chất lượng từng TC** — **Fail**: B.1 (TC-FUNC001-02 expected không đo được điều tiêu đề tuyên bố), B.2 (TC-PERM002-01/02 gộp nhiều route — NIT), B.4 (TC-TOOLVAL2001-01 precondition ép gọi hàm, không phải đường user thật; TC-PERM002-02 dùng "id bất kỳ").
- [x] **C. Chất lượng bộ TC tổng thể** — **Fail**: tỷ lệ loại case **6 Normal / 2 Abnormal / 0 Boundary** — lệch nặng so với gợi ý 40/35/25, đặc biệt sai với task phân quyền + validation (đáng lẽ Abnormal + Boundary phải nhiều hơn). Không có test đa role. Không có test responsive/đa trình duyệt.
- [x] **D. Spec alignment** — **Fail**: không có `02-spec-reference.md`; 8/8 TC để trống `Trạng thái đánh giá spec`. Xem §6.
- [x] **E. Hành chính** — Pass: TC No. đúng format canonical `TC-<mã quan điểm bỏ gạch>-<nn>`, file đúng folder. **Fail nhẹ**: "Tester viết TCs" là AI, chưa có người ký; version v1 có ghi.
- [x] **F. Base quan điểm test LME**
  - [x] F.1 Quan điểm (tầng 1) — bảng dưới
  - [x] F.2 Catalog (tầng 2) — **Fail**: `C` (khối MAP-PLAN chưa duyệt hết 6 dòng, MAP-PERM-02/03 chưa duyệt), `D/D2` (0 TC production dù task chạm gói cước — RULE-08). Pass: `A`, `B`, `E` không áp dụng đáng kể cho task này.
  - [x] F.3 RULE quy trình — **Vi phạm**: RULE-01, RULE-02, RULE-08. **Tuân thủ**: RULE-09 (có cả free cũ + free mới), RULE-07 (một phần — TC-FUNC001-01 có kiểm dữ liệu, nhưng thiếu kiểm phạm vi `WHERE`), RULE-12 (một phần). RULE-03 không áp dụng (Studio không có cột đánh ×). RULE-11 đã tuân thủ (không dùng §4 checklist-lme để flag).

### F.1 — Bảng quan điểm đối chiếu

> `⚠️` = quan điểm chỉ được cover bởi TC mang mã Studio không map được → theo luật BƯỚC 0.6 #6, **không tính là cover**.

| Mã quan điểm | Ưu tiên | Trigger khớp task? | TC cover (suy luận) | Exec | Kết luận |
|---|---|---|---|---|---|
| `FUNC-001` — Luồng chính đúng đặc tả | **Cao** | ◯ luôn bắt buộc | TC-FUNC001-01, TC-FUNC001-02 | 2/2 | **RISK** — 2 TC đều `Normal`, thiếu Abnormal + Boundary, không ghi lý do → `[MAJOR] RULE-01` |
| `FUNC-002` — Bỏ trống trường bắt buộc | Cao | △ ô nhập mã nguồn có tồn tại nhưng fix chỉ khoá/mở nó | — | — | **×** — không phải phạm vi fix (fix không chạm validate nội dung ô nhập). Ghi lý do theo RULE-03 |
| `FUNC-004` — Giới hạn trên/dưới | Cao | × | — | — | **×** — màn không có giới hạn số lượng/ký tự bị fix chạm |
| `CONC-001` — 1 hành động chỉ xử lý 1 lần | **Cao** | ◯ nút 再発行 vừa được mở cho nhóm tài khoản mới | — | — | **GAP** ⛔ → `[BLOCKER]` §4.1 |
| `DATA-DB-001` — WHERE scope + khóa mồ côi | **Cao** | ◯ **BẮT BUỘC** vì có UPDATE `bots.transfer_code` | — | — | **GAP** ⛔ → `[BLOCKER]` §4.1 |
| `DATA-BACKUP-001` — Backup / Copy / Recover | **Cao** | ◯ **BẮT BUỘC** — đây chính là màn copy bot | TC-REGSHARED001-01 (chỉ tới bước điều hướng) | 1/1 | **RISK→GAP** ⛔ — kịch bản bot free làm **nguồn** không có TC → `[BLOCKER]` §4.1 |
| `DATA-001` — Phản ánh đủ ở mọi màn liên quan | Cao | △ chưa rõ `transfer_code` có hiển thị ở màn khác | — | — | **Input thiếu** → `[MINOR]` §4.3 |
| `DATA-AUDIT-001` — Lịch sử thao tác | Cao | △ 再発行 đổi giá trị credential | — | — | **Input thiếu** — cần hỏi Dev màn có `操作履歴` không → `[MINOR]` §4.3 |
| `PERM-001` — Menu/nút đúng theo role | **Cao** | ◯ `__construct` (điểm vào chặn toàn controller) bị viết lại | — | — | **GAP** → `[MAJOR]` §4.2 (hạ từ BLOCKER vì không có bằng chứng `__construct` từng chứa role check) |
| `PERM-002` — Không bypass bằng API / URL trực tiếp | **Cao** | ◯ **BẮT BUỘC** — thao tác sao chép toàn bộ dữ liệu bot | TC-PERM002-01, TC-PERM002-02 | 2/2 | **RISK→GAP** ⛔ — thiếu nhánh **gõ thẳng URL** (MAP-PERM-02) và **đổi param id** (MAP-PERM-03); thiếu `Boundary` → `[BLOCKER]` §4.1 + `[MAJOR] RULE-01` |
| `PERM-003` — Cách ly dữ liệu đa tài khoản | Cao | ◯ endpoint mutate credential vừa mở cho nhóm mới | — | — | **GAP** → `[MAJOR]` §4.2 (gộp TC-PERM002-04) |
| `SEC-001` — Chặn truy cập trái phép PII | Cao | ◯ mã sao chép cho phép copy toàn bộ dữ liệu bot | — | — | **GAP** → `[MAJOR]` §4.2 |
| `OUT-TRUTH-001` — UI/message khớp trạng thái THẬT | **Cao** | ◯ **BẮT BUỘC** — bug gốc chính là lỗi im lặng | TC-TOOLVAL2001-01 ⚠️ | 1/1 | **GAP** (TC duy nhất mang mã không map được) → `[MAJOR]` §4.2 |
| `UI-003` — Loading / rỗng / lỗi | Cao (nâng — rủi ro false success) | ◯ màn tải dữ liệu bất đồng bộ, bug gốc là màn trống | TC-TOOLKNOW002-01 ⚠️ | 1/1 | **GAP** (mã không map được) + thiếu case mã rỗng, lỗi mạng → `[BLOCKER]`/`[MAJOR]` §4.1/4.2 |
| `PAY-LIMIT-001` — Giới hạn chức năng theo gói | **Cao** | ◯ **BẮT BUỘC** — đây là bản chất của task | TC-TOOLOLDREC001-01 ⚠️, TC-REGSHARED001-01, TC-TOOLVAL2001-01 ⚠️, TC-PERM002-02 | 4/4 | **RISK** — 3/5 trạng thái gói; chưa có bảng plan-limit chính thức; MAP-PLAN-04/05/06 chưa duyệt → `[MAJOR]` §4.2 |
| `PAY-PLAN-001` — Đổi gói: reset trạng thái & quyền | **Cao** | △ fix không tự đổi gói, nhưng Dev nêu kịch bản hạ gói giữa chừng | — | — | **GAP** → `[MAJOR]` §4.2 |
| `PAY-STATE-001` / `PAY-AMOUNT-001` | Cao | × | — | — | **×** — fix không chạm giao dịch tiền hay số tiền, chỉ chạm quyền theo gói |
| `STATE-001` — Quy trình nhiều bước bị gián đoạn | Cao | × | — | — | **×** — job sao chép **không bị fix chạm code** (áp dụng nguyên tắc bám tầng root cause). Ghi lý do theo RULE-03 |
| `STATE-CLEAN-001` — Dọn dẹp khi hủy / hạ gói | Cao | × | — | — | **×** — fix không chạm luồng hủy hợp đồng |
| `REG-SHARED-001` — Shared code / logic | **Cao** | ◯ **BẮT BUỘC** — fix bug có thể tồn tại ở màn tương tự | TC-REGSHARED001-01 (chỉ cùng màn, không phải cross-screen) | 1/1 | **GAP** — thiếu **danh sách nơi ảnh hưởng do Dev cung cấp** (evidence bắt buộc) → `[MAJOR]` §4.2 |
| `REG-RUN-001` — Job đang chạy dở khi release | Cao | △ có thể có tiến trình sao chép đang chạy lúc release | — | — | **GAP** → gộp vào `[MAJOR]` AP-3 §4.2 |
| `COMPAT-LEGACY-001` — Cũ & mới song song (RULE-09) | **Cao** | ◯ free cũ (`plan_type=2`) ⇄ free mới (`contract_type='free'`) | TC-TOOLKNOW002-01 ⚠️, TC-TOOLOLDREC001-01 ⚠️ | 2/2 | **RISK** — **nội dung TC thực sự cover đủ cả 2 nhánh** (điểm tốt nhất của bộ TC này), nhưng **cả 2 TC đều mang mã không map được** → theo luật không tính cover. **Chỉ cần gán lại mã trên Studio là chuyển OK** → `[MAJOR]` §4.2 (mục mã quan điểm) |
| `DEPLOY-ASSET-001` — Version asset JS/CSS | **Cao** | ◯ **BẮT BUỘC** — `backup.js` nằm trong 4 file thay đổi | — | — | **GAP** ⛔ → `[BLOCKER]` §4.1 |
| `DEPLOY-LIVE-001` — Release không lock maintain | **Cao** | ◯ payload `get-bot-data` đổi (thêm `is_free_plan`) | — | — | **GAP** → `[MAJOR]` §4.2 |
| `ENV-003` — Khác biệt dev/staging/production | **Cao** | ◯ **BẮT BUỘC** — task chạm gói cước (`ENV-PAY`) | 0 TC chạy ngoài `local` | 0/8 | **GAP** → `[MAJOR] RULE-08` §4.2 |
| `JOB-001` — Job nền / batch | Cao | × | — | — | **×** — fix không thêm/sửa job nền |
| `UI-001` / `UI-002` — Responsive / đa trình duyệt | Trung bình | ◯ màn admin có UI bị sửa (blade + js) | — | — | **GAP** → mức Trung bình, gộp vào `[MAJOR]` §4.2 nhóm C (bộ TC không có test đa trình duyệt) |
| `UI-INPUT-001` — Hành vi ô nhập liệu | Trung bình | △ ô nhập mã nguồn bị đổi trạng thái `:disabled` | — | — | **GAP** nhẹ → `[NIT]` §4.4 |
| `LIST-001` · `MSG-*` · `MEDIA-*` · `FRIEND-*` · `INTG-*` · `PERF-LARGE-001` · `NOTI-MAIL-001` · `LIFF-ENTRY-001` | — | × | — | — | **×** — task là màn admin nội bộ, không gửi tin, không media, không friend info, không tích hợp bên thứ 3, không sinh link cho LINE user |

**Tổng kết F.1**: 6 quan điểm **GAP ở mức Cao** → BLOCKER (`CONC-001`, `DATA-DB-001`, `DATA-BACKUP-001`, `PERM-002` nhánh URL, `DEPLOY-ASSET-001`, `UI-003` nhánh mã rỗng) · 9 quan điểm GAP/RISK → MAJOR · 1 quan điểm (`COMPAT-LEGACY-001`) chỉ cần **gán lại mã trên Studio** là chuyển OK.

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | `<chờ Leader verify draft này>` | |
| Tester | AI pipeline (Studio job 607) — không có người nhận feedback | |

> ⚠️ **Draft cho Leader verify** — không phải final. Đặc biệt cần Leader chốt 3 điểm: (1) `CONC-001` giữ BLOCKER hay hạ MAJOR; (2) cách xử lý 3 mã quan điểm Studio không map được (gán lại vs. bổ sung vào checklist theo RULE-10); (3) phạm vi bắt buộc chạy lại trên production theo RULE-08.
