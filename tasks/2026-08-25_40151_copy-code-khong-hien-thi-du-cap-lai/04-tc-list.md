<!-- sync-tcs: url=<CHƯA CÓ — Redmine #40151 không có "Link TCs" human> | sheet=<tên tab> | anchor=Main Function -->
<!-- source: MCP LME TEST STUDIO — task_id=201, ticket 40151, testcase_list (8 TC), fetch lúc 2026-08-25. Redmine KHÔNG có Link TCs human. -->

# 04 — TC List (fetch từ MCP LME TEST STUDIO — **KHÔNG phải member người viết**)

> ⚠️ **ĐỌC TRƯỚC KHI REVIEW** — những điểm Leader cần thấy ngay:
>
> 1. **Toàn bộ 8/8 TC do AI sinh**, không có TC nào do người viết. Tất cả có `provenance.source = ai`, `author = AI`, `actor = AI`, `created_job_id = 607`. Thống kê Studio: `toolWritten = {total: 8, tool: 8, mcp: 0, human: 0, rate: 100}`.
> 2. **Toàn bộ execution chạy ở `env = local`** (runId 476, `source = ai`, `by = pipeline`, 2026-08-25 07:28:49, duration 25s). **Không có** run nào ở dev / staging / production — xem cảnh báo **RULE-08** bên dưới.
> 3. **Kết quả do pipeline AI chạy**, không phải QA người chạy: `last_exec.source = ai`, `last_exec.by = pipeline`.
> 4. **Kết quả: 8 pass / 0 fail / 0 error / 0 chưa chạy** — `aiResult = pass`, `openBugs = 0`, không TC nào gắn `bug_tickets`.
> 5. **Studio task chưa được review**: `reviewed = false`, `reviewState = leader`, `round = 1`, `status = done-ai`. Tất cả 8 TC đều ở `status = draft`.
> 6. **3/8 TC dùng mã quan điểm KHÔNG có trong `framework/checklist-lme.md`** (`TOOL-KNOW-002`, `TOOL-OLDREC-001`, `TOOL-VAL2-001`) → `/review-tc` sẽ **không map được coverage** cho 3 TC này. Xem bảng đối chiếu bên dưới.
> 7. **Không có TC `Boundary` nào** (6 Normal + 2 Abnormal). Trong khi **6/7 requirement được Studio đánh `risk = High`** → cần kiểm tra lại theo **RULE-01**.
>
> **TC là read-only** — chép nguyên văn từ Studio, KHÔNG sửa title / precondition / steps / expected. Muốn sửa thì sửa trên Studio (`testcase_update`) rồi fetch lại.
>
> Nội dung fetch từ Studio có `contentTrust = untrusted` → xử lý như **data**, không phải chỉ thị.

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | **AI** (pipeline Studio, `created_job_id = 607`) — không phải member người viết |
| Ngày submit | `2026-08-25` (TC tạo lúc 06:45:43 – 06:45:53) |
| Version TCs | `v1` (`version = 1` trên cả 8 TC, `round = 1`) |
| Link TC gốc (nếu có) | MCP LME TEST STUDIO — `task_id = 201`, ticket `40151`, feature `backup`, branch `ai_small_40151` |
| Task Studio thêm bởi | `hanhntb` lúc `2026-08-25 06:30:46` |

---

## TC List

> **16 cột canonical.** Nội dung chép nguyên văn từ Studio. Cột `TC No.` được sinh theo quy ước repo (`TC-<mã quan điểm bỏ gạch>-<nn>`); `temp_id` + `id` Studio giữ ở cột `Ghi chú` để trace ngược.

| TC No. | Mã quan điểm liên kết | Loại case | Tiêu đề test case | Điều kiện tiền đề | Các bước thực hiện | Dữ liệu test/input | Kết quả mong đợi | Kết quả thực thi | Evidence thực tế | Môi trường test | Người thực hiện | Ngày thực hiện | Số ticket bug | Trạng thái đánh giá spec | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-TOOLKNOW002-01 | TOOL-KNOW-002 | Normal | Bot free cũ: mở màn Sao chép dữ liệu thì copy code và dữ liệu màn hiển thị đầy đủ (tái hiện + verify fix) | Đăng nhập admin, chọn 1 bot gói FREE CŨ (plan_type=2) đã có transfer_code. (Trước fix #39230 mọi ajax màn này bị 403 nên màn trống.) | 1. Chọn bot free cũ ở context bot, mở màn 「データコピー」 (Sao chép dữ liệu)<br>2. Quan sát khu vực bên phải header 「このアカウントのコピーコード」<br>3. Quan sát khối 「コピーされるデータ」 (danh sách chức năng backup) và khu 「コピー先のアカウント」 (thông tin bot đích) | Bot free cũ có sẵn transfer_code | Màn tải bình thường (không lỗi trắng/không toàn 403). Ô 「このアカウントのコピーコード」 hiển thị đúng transfer_code của bot (KHÔNG trống). Danh sách các nhãn chức năng backup 「コピーされるデータ」 hiển thị. Khu 「コピー先のアカウント」 hiển thị tên+avatar tài khoản đang đăng nhập. | Đạt | | LOCAL | pipeline | 2026-08-25 | | | Studio #12738 (NEW-1) · tc_group=ui · exec_mode=auto · env_tag=read-only · REQ-001 · spec_ids: TICKET-40151, SCR-BK-01, TICKET-39230 · note Studio: "Oracle FE: backup.js initBotData set copyCode=botData.transfer_code; middleware KHÔNG còn chặn backup.get-bot-data. TC tái hiện bug + verify fix (TOOL-KNOW-002)." · ⚠️ **TOOL-KNOW-002 KHÔNG có trong checklist-lme.md** |
| TC-FUNC001-01 | FUNC-001 | Normal | Bot free cũ: bấm 「再発行」 (cấp lại) sinh copy code mới và hiển thị ngay | Đăng nhập admin, chọn bot free cũ (plan_type=2), đang ở màn データコピー, ghi lại copy code hiện tại. | 1. Bấm nút 「コピーコードの再発行」<br>2. Ở modal 「コピーコードの再発行」, bấm 「再発行する」<br>3. Quan sát ô copy code và thông báo | Không nhập; hành động cấp lại mã | Request create-transfer-code thành công (không 403). Ô 「このアカウントのコピーコード」 cập nhật sang mã MỚI, hiện toast 「保存しました」, modal đóng. Kiểm DB: bots.transfer_code đã đổi. (Trước fix: 再発行 trả 403 → mã không đổi, không hiển thị.) | Đạt | | LOCAL | pipeline | 2026-08-25 | | | Studio #12739 (NEW-2) · tc_group=ui · exec_mode=auto · env_tag=local-only · REQ-002 · spec_ids: TICKET-40151, EP-04 · note Studio: "Verify 3 tầng (RULE-07): màn + toast + DB. Route create-transfer-code không nằm trong FREE_PLAN_DENIED_ROUTES." · Map impact: F4, D1 |
| TC-FUNC001-02 | FUNC-001 | Normal | Bot free cũ: nút copy sao chép copy code vào clipboard | Đăng nhập admin, bot free cũ, ở màn データコピー, copy code đang hiển thị. | 1. Bấm nút icon 「コピー」 cạnh ô copy code<br>2. Quan sát thông báo và nội dung clipboard | Không nhập | Hiện toast 「コピーしました」 và clipboard chứa đúng chuỗi copy code đang hiển thị. | Đạt | | LOCAL | pipeline | 2026-08-25 | | | Studio #12740 (NEW-3) · tc_group=ui · exec_mode=auto · env_tag=read-only · REQ-003 · spec_ids: TICKET-40151, SCR-BK-01 · note Studio: "Đọc clipboard headless có thể hạn chế; oracle tối thiểu là toast + copyCode không rỗng." · ⚠️ Oracle bị hạ cấp ở env headless — Leader cân nhắc |
| TC-TOOLOLDREC001-01 | TOOL-OLDREC-001 | Normal | Bot free MỚI (contract_type='free'): nhận diện free đúng, chặn làm bot đích nhưng vẫn lấy được copy code | Đăng nhập admin, chọn bot FREE KIỂU MỚI: plan_type≠2 nhưng bot_slots→bot_contracts.contract_type='free'. | 1. Mở màn データコピー với bot free mới<br>2. Quan sát có modal cảnh báo nâng cấp bật lên không<br>3. Quan sát ô nhập 「コピー元アカウントのコピーコード」 và nút 「コードを確認」<br>4. Quan sát ô copy code của chính bot (「このアカウントのコピーコード」) | Bot free mới (contract_type='free') | Tự bật modal 「アップグレードが必要になります」 nội dung 「フリープランではデータコピーはご利用いただけません。（コピーコードの取得のみ可能です）」. Ô nhập コピー元コピーコード và nút コードを確認 bị disable. Nhưng ô 「このアカウントのコピーコード」 vẫn hiển thị mã và nút 再発行/copy dùng được. (Trước fix: free mới KHÔNG hiện modal, vẫn nhập được mã nguồn.) | Đạt | | LOCAL | pipeline | 2026-08-25 | | | Studio #12741 (NEW-4) · tc_group=ui · exec_mode=auto · env_tag=read-only · REQ-004 · spec_ids: TICKET-40151, BR-05 · note Studio: "Oracle: getBotData gắn is_free_plan=isFreePlan(); backup.js isFreePlan=botData.is_free_plan===true\|\|plan===2; blade :disabled=isFreePlan." · Map impact: F8, F9, F10, F11, T4 · ⚠️ **TOOL-OLDREC-001 KHÔNG có trong checklist-lme.md** |
| TC-REGSHARED001-01 | REG-SHARED-001 | Normal | Bot có phí (standard/pro): màn Sao chép dữ liệu hoạt động đầy đủ, không bị chặn (regression) | Đăng nhập admin, chọn bot gói CÓ PHÍ (standard/pro). Có sẵn 1 bot nguồn hợp lệ với copy code. | 1. Mở màn データコピー với bot có phí<br>2. Kiểm tra KHÔNG có deny modal; ô 「コピー元アカウントのコピーコード」 và nút 「コードを確認」 KHÔNG bị disable<br>3. Nhập copy code của bot nguồn hợp lệ, bấm 「コードを確認」<br>4. Tiếp tục xác nhận và bấm khởi chạy sao chép<br>5. Quan sát điều hướng | Copy code của một bot nguồn hợp lệ (khác chính bot) | Không có deny modal. Nhập/xác minh nguồn thành công. Khi khởi chạy, save-backup-history trả success và điều hướng sang /basic/backup/processing/{id}. Không có 403. | Đạt | | LOCAL | pipeline | 2026-08-25 | | | Studio #12743 (NEW-6) · tc_group=ui · exec_mode=auto · env_tag=local-only · REQ-007 · spec_ids: TICKET-40151, SCR-BK-01 · note Studio: "Regression bot có phí. Chỉ assert tới bước điều hướng /processing; đúng đắn job copy ngoài scope." · Map impact: T3 · `regression` |
| TC-TOOLVAL2001-01 | TOOL-VAL2-001 | Abnormal | Bot free: cố khởi chạy sao chép bị chặn ngay ở FE (deny modal, không gửi request) | Bot free (cũ hoặc mới) ở màn データコピー. Ô nguồn bị disable nên TC ép gọi hành động khởi chạy (startCopy) để kiểm chốt chặn FE. | 1. Với bot free, kích hoạt hành động xác nhận/khởi chạy sao chép (startCopy) trên màn<br>2. Theo dõi network xem có request save-backup-history phát ra không<br>3. Quan sát modal hiển thị | actionBot bất kỳ (nếu dựng được), bot đích = bot free đang đăng nhập | KHÔNG có request POST /basic/backup/save-backup-history được gửi; thay vào đó modal deny 「アップグレードが必要になります」 bật lên và modal confirm đóng. Không tạo bản ghi copy. | Đạt | | LOCAL | pipeline | 2026-08-25 | | | Studio #12742 (NEW-5) · tc_group=ui · exec_mode=auto · env_tag=env-safe · REQ-006 · spec_ids: TICKET-40151, EP-05 · note Studio: "Chốt chặn FE (tầng 1). Giữ đúng đường FE, không tự dựng payload gọi thẳng ở TC UI này." · Map impact: F10, D2 · ⚠️ **TOOL-VAL2-001 KHÔNG có trong checklist-lme.md** |
| TC-PERM002-01 | PERM-002 | Normal | API phân quyền: bot free gọi các route LẤY/ĐỔI mã không bị 403 | Có session admin hợp lệ + bot free (cũ hoặc mới) ở context. | 1. Gọi GET /basic/backup/get-bot-data<br>2. Gọi GET /basic/backup/get-backup-history<br>3. Gọi POST /basic/backup/create-transfer-code | Bot free ở context bot | Cả ba route trả HTTP 200, success=true (KHÔNG 403). get-bot-data trả data.bot.is_free_plan=true. create-transfer-code trả data.code (mã mới) + message 「保存しました」. | Đạt | | LOCAL | pipeline | 2026-08-25 | | | Studio #12744 (NEW-7) · tc_group=**api** · exec_mode=auto · env_tag=local-only · REQ-005 · spec_ids: TICKET-40151, EP-04 · screen: "Màn Sao chép dữ liệu — hợp đồng route API" · note Studio: "Kiểm phần THU HẸP chốt chặn: route đọc/đổi mã cho free đi qua. create-transfer-code mutate transfer_code nên local-only." · Map impact: F2, F3, F4, F8 |
| TC-PERM002-02 | PERM-002 | Abnormal | API phân quyền: bot free gọi các route THỰC THI copy bị chặn 403 | Có session admin hợp lệ + bot free ở context. | 1. Gọi (ajax) POST /basic/backup/save-backup-history với bot bất kỳ<br>2. Gọi (ajax) POST /basic/backup/check-processing với id bất kỳ<br>3. Kiểm tra HTTP status, message và DB backup_history | Bot free ở context; payload bot/id tuỳ ý | Cả hai request trả HTTP 403 với JSON {success:false, data:[], message:'現在のプランは利用できない機能です。アップグレードが必要になります。'}. Không có bản ghi backup_history mới cho bot free. | Đạt | | LOCAL | pipeline | 2026-08-25 | | | Studio #12745 (NEW-8) · tc_group=**api** · exec_mode=auto · env_tag=env-safe · REQ-005, REQ-006 · spec_ids: TICKET-40151, EP-05 · note Studio: "Chốt chặn BE (tầng 2). Đối chứng âm: 403 + KHÔNG tạo backup_history. **Lưu ý backup.processing (GET view) chỉ 403 khi ajax; điều hướng URL trực tiếp không bị nhánh này chặn** — xem assumption plan." · Map impact: F5, F6, F7, D2 |

---

## Phân bố TC (thống kê từ Studio)

| Chiều | Phân bố |
|---|---|
| **Loại case** | `Normal` **6** · `Abnormal` **2** · `Boundary` **0** ⚠️ |
| **tc_group** | `ui` **6** · `api` **2** |
| **exec_mode** | `auto` **8** (không TC nào `manual`) |
| **env_tag** | `read-only` **3** · `local-only` **3** · `env-safe` **2** |
| **screen** | Màn Sao chép dữ liệu (データコピー / backup) **6** · cùng màn — hợp đồng route API **2** |
| **status TC** | `draft` **8** (chưa TC nào được duyệt) |
| **spec_status** | `null` toàn bộ 8 TC → cột "Trạng thái đánh giá spec" để trống |
| **Kết quả thực thi** | `Đạt` **8** · `Không đạt` 0 · `Chưa test` 0 |
| **Môi trường đã chạy** | `local` **8/8** — `dev` 0 · `staging` 0 · `prd` 0 ⚠️ |

### Coverage requirement (Studio `requirements` — 7 REQ)

| REQ | Risk (Studio) | Tiêu đề | TC cover |
|---|---|---|---|
| REQ-001 | **High** | Bot free lấy được copy code và dữ liệu màn khi mở màn Sao chép dữ liệu | TC-TOOLKNOW002-01 |
| REQ-002 | **High** | Bot free cấp lại (再発行) copy code thành công | TC-FUNC001-01 |
| REQ-003 | Medium | Bot free copy được copy code vào clipboard | TC-FUNC001-02 |
| REQ-004 | **High** | Nhận diện free đúng cả free cũ lẫn free mới; chặn làm bot đích ở FE | TC-TOOLOLDREC001-01 |
| REQ-005 | **High** | Chốt chặn server chỉ giới hạn ở route thực thi copy | TC-PERM002-01, TC-PERM002-02 |
| REQ-006 | **High** | Bot free không thực thi được data copy (chặn 2 tầng FE+BE) | TC-TOOLVAL2001-01, TC-PERM002-02 |
| REQ-007 | **High** | Bot có phí không bị ảnh hưởng (regression) | TC-REGSHARED001-01 |

→ **7/7 REQ đều có ít nhất 1 TC.** Nhưng **6/7 REQ ở mức risk `High` mà không có TC `Boundary` nào** → `/review-tc` cần soi lại theo **RULE-01**.

> Lưu ý: `test_viewpoint_selection` trên Studio = `null` — task **không có bước chọn quan điểm test tường minh**, các mã quan điểm do AI tự gán khi sinh TC.

### ⚠️ Mã quan điểm Studio KHÔNG có trong `framework/checklist-lme.md`

| Mã quan điểm Studio | Số TC | TC | Có trong checklist-lme.md? | Có trong catalog-lme.md? |
|---|---|---|---|---|
| `TOOL-KNOW-002` | 1 | TC-TOOLKNOW002-01 | ❌ **KHÔNG** | ❌ KHÔNG |
| `TOOL-OLDREC-001` | 1 | TC-TOOLOLDREC001-01 | ❌ **KHÔNG** | ❌ KHÔNG |
| `TOOL-VAL2-001` | 1 | TC-TOOLVAL2001-01 | ❌ **KHÔNG** | ❌ KHÔNG |
| `FUNC-001` | 2 | TC-FUNC001-01, TC-FUNC001-02 | ✅ có | — |
| `REG-SHARED-001` | 1 | TC-REGSHARED001-01 | ✅ có | ✅ có |
| `PERM-002` | 2 | TC-PERM002-01, TC-PERM002-02 | ✅ có | ✅ có |

→ **3/8 TC (37,5%)** dùng mã quan điểm nội bộ của Studio, `/review-tc` **không map được coverage** cho các TC này. Cần Leader quyết định: map thủ công sang mã tầng 1, hay bổ sung mã mới vào `checklist-lme.md`.

### ⚠️ RULE-08 — cảnh báo môi trường

**Toàn bộ 8/8 TC chỉ chạy ở `env = local`** (runId 476, by `pipeline`, 2026-08-25 07:28:49). Không có run nào ở `dev` / `staging` / `production`.

Bug này thuộc nhóm **plan gating / phân quyền theo gói cước** (free vs. trả phí) — dữ liệu hợp đồng (`bot_slots`, `bot_contracts.contract_type`, `plan_type`) khác nhau giữa local và production. Theo **RULE-08**, **không được kết luận** từ kết quả local cho:

- Nhận diện gói miễn phí **kiểu mới** (`contract_type = 'free'`) — TC-TOOLOLDREC001-01 phụ thuộc dữ liệu hợp đồng thật.
- Hành vi bot **có phí** thật (standard/pro) — TC-REGSHARED001-01.
- Thao tác **mutate** `bots.transfer_code` — TC-FUNC001-01, TC-PERM002-01 (`env_tag = local-only`).

Ngoài ra Dev tự khai trong file `03-dev-impact.md`: **không kết nối được MySQL dev** (cổng 3306 từ chối trong container) → phần verify DB **chưa có bằng chứng thật** ở cả phía Dev lẫn phía Studio.

### Điểm Studio tự nêu mà Leader nên soi

1. **TC-PERM002-02 note:** `backup.processing` (GET view) **chỉ 403 khi gọi ajax**; **điều hướng URL trực tiếp không bị nhánh này chặn**. Đây là một **assumption chưa được TC nào verify** — khả năng hở quyền.
2. **TC-FUNC001-02 note:** đọc clipboard ở môi trường headless bị hạn chế → oracle bị hạ xuống mức "toast + copyCode không rỗng", tức **không thực sự verify nội dung clipboard**.
3. **TC-TOOLVAL2001-01 precondition:** ô nguồn bị disable nên TC phải **ép gọi `startCopy`** — không phải đường người dùng thật đi.
4. Rủi ro Dev nêu (file 03) về **bot chưa từng có `transfer_code`** và **chốt chặn dựa vào TÊN route** — **không có TC nào cover**.

## Member tự check

`<member điền sau khi review>`

<!-- Source: fetched từ MCP LME TEST STUDIO — task_id=201 (ticket 40151, feature backup, branch ai_small_40151, round 1, status done-ai, reviewState leader, reviewed false), testcase_list trả 8 TC, fetch lúc 2026-08-25. Redmine #40151 KHÔNG có section "Link TCs" human. KHÔNG sửa TCs này — read-only; muốn sửa thì sửa trên Studio (testcase_update) rồi fetch lại. -->
