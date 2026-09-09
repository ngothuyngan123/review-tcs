<!-- sync-tcs: url=<chưa có — Redmine #39040 KHÔNG có Link TCs human> | sheet=<chưa có> | anchor=Main Function -->
<!-- source: MCP LME TEST STUDIO — task_id=202, ticket 39040, testcase_list (13 TC) + task_get_report, fetch lúc 2026-08-26. Redmine KHÔNG có Link TCs human. -->

# 04 — TC List (fetch từ MCP LME TEST STUDIO — **KHÔNG phải member người viết**)

## ⚠️ CẢNH BÁO ĐỌC TRƯỚC (Leader cần thấy ngay)

| # | Cảnh báo | Chi tiết |
|---|---|---|
| 1 | **TCs do AI sinh, không phải member người viết** | 12/13 TC có `provenance.source = ai` (`actor = AI`, `created_job_id = 615`). Chỉ **1 TC** do người viết: `TC-FUNC004-02` (Studio #12879, `provenance.source = human`, `actor = haodtb@mcp`). Studio `toolWritten` báo `human = 0` vì đó là **kênh ghi** (MCP), không phải tác giả — tác giả thật đọc ở `provenance.source`. |
| 2 | **Toàn bộ 13 TC chạy ở `env = local`** | ⚠️ **RULE-08**: task này chạm **media (upload / resize ảnh)** → **không được kết luận từ local**. Studio `envAuto` xác nhận `dev / staging / prd` đều **0 run**. Cần chạy lại tối thiểu trên STAGING, và TC deploy-asset phải chạy trên môi trường release thật. |
| 3 | **Auto-run #486 thực chất `fail`: 7 pass / 4 error** | `task_get_report` cho thấy run auto #486 (2026-08-25, `by = pipeline`) status = **fail** — 4 TC `error`: #12826, #12849, #12850, #12851. Trạng thái "13/13 Đạt" hiện tại là do **haodtb chạy tay lại 6 TC ngày 2026-08-26**, vẫn ở `env = local`. |
| 4 | **6 manual run KHÔNG có evidence** | Tất cả manual result (`id` 4437, 4438, 4453, 4463, 4464, 4465) có `actual = null` và `evidence = []` → **vi phạm RULE-02** (Đạt bắt buộc có evidence). |
| 5 | **`TC-DEPLOYASSET001-01` chạy sai môi trường** | TC khai `env_scope = ["staging"]`, `exec_mode = manual`, note ghi *"cần release thật để tái hiện cache asset; không kiểm được ở local build đơn lẻ"* — nhưng lại được đánh **Đạt ở `env = local`**. Kết quả này **không có giá trị kết luận**. |
| 6 | **3 TC màn cũ `/admin/bot-edit` chưa verify được luồng lưu end-to-end** | #12849 / #12850 / #12851 auto error vì `botChange` gọi `api.line.me` OAuth vô điều kiện với channel credentials giả → luôn 「入力した情報が間違っています」. Triage kết luận **lỗi hạ tầng, không phải bug #39040**, và chỉ verify được **2MB-gate không chặn oan**, **KHÔNG** verify được "lưu thành công". Manual pass sau đó không kèm evidence nên không rõ đã vượt được rào OAuth chưa. |
| 7 | **2 quan điểm Studio KHÔNG có trong `framework/checklist-lme.md`** | `TOOL-KNOW-002` (2 TC) và `TOOL-VAL2-001` (2 TC) — `/review-tc` sẽ **không map được coverage** cho 4 TC này. Xem bảng đối chiếu §Mã quan điểm bên dưới. |
| 8 | **2 business rule coverage = `none`** | Studio coverage báo `BR-12` (upload path `media/images/{adminId}/{botId}/bot/`; `url_image = '/images/camera.png'` → xóa ảnh) và `BR-13` (resize max 2048px giữ aspect ratio) — **0 TC**. Đây là logic upload **dùng chung** với đường fix. |
| 9 | **Chưa có TC nào cho F5 (màn thêm / đổi tài khoản)** | `03-dev-impact.md` F5: `ChangeBotController@store`, `change_bot.js`, `change_new_bot.js`, `olioa.js` — Dev xác nhận **không kiểm dung lượng**, cố ý ngoài phạm vi. Studio cũng không có TC. Leader quyết. |
| 10 | **`reviewState = leader`, `reviewed = false`, `openBugs = 0`** | Task đang chờ Leader review; chưa TC nào raise bug. |

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | **AI Studio** (12 TC, job #615) + `haodtb@mcp` (1 TC — Studio #12879) |
| Ngày submit | `2026-08-25` (task added `2026-08-25 07:25:29` by `haodtb`) |
| Version TCs | Studio `round = 1` (`status = done-ai`, `aiResult = pass`, `reviewState = leader`) |
| Link TC gốc (nếu có) | MCP LME TEST STUDIO — `task_id = 202`, `feature = bot-edit`, `branch = ai_fixbug_39040` |
| Nguồn fetch | `task_list(ticket_id=39040)` → `testcase_list(task_id=202)` + `task_get_context` + `task_get_report` |

### Thống kê thực thi (từ `task_get_report`)

| Chỉ số | Giá trị |
|---|---|
| Tổng TC | **13** |
| Trạng thái hiện tại | **13 Đạt** / 0 Không đạt / 0 Chưa test |
| Auto run #486 (`pipeline`, 2026-08-25 07:47→08:38, env `local`) | status **fail** — pass **7**, fail 0, skip 0, **error 4** |
| Manual run (`haodtb`, 2026-08-26 07:58→08:22, env `local`) | pass **6**, fail 0, blocked 0, skip 0 — **evidence rỗng toàn bộ** |
| Môi trường đã chạy | **`local` 100%** — `dev` 0 run · `staging` 0 run · `prd` 0 run |
| Nguồn kết quả | 7 TC do **pipeline AI** chạy · 6 TC do **QA người (`haodtb`)** chạy tay |
| Bug đã raise | **0** |

### Phân bố

| Chiều | Phân bố |
|---|---|
| `case_type` | Normal **4** · Abnormal **5** · Boundary **4** |
| `tc_group` | `ui` **11** · `api` **2** |
| `exec_mode` | `auto` **12** · `manual` **1** |
| `env_tag` | `local-only` **11** · `env-safe` **1** · `read-only` **1** |
| `screen` | Màn Profile bot mới `/admin/setting-bot` **6** · Màn Profile bot cũ `/admin/bot-edit` **6** · Release asset **1** |
| `requirement_keys` | REQ-001 ×2 · REQ-002 ×1 · REQ-003 ×2 · REQ-004 ×2 · REQ-005 ×2 · REQ-006 ×1 · REQ-007 ×3 · REQ-008 ×1 · REQ-009 ×1 · **1 TC không gắn REQ** (`TC-FUNC004-02` / Studio #12879) |
| `spec_status` | `null` toàn bộ 13 TC → cột "Trạng thái đánh giá spec" **để trống** |
| `status` | `draft` toàn bộ 13 TC |

---

## TC List

> 16 cột canonical. **TCs là read-only** — chép nguyên văn từ Studio, KHÔNG sửa title / precondition / steps / expected. Muốn sửa thì sửa trên Studio (`testcase_update`) rồi fetch lại.

| TC No. | Mã quan điểm liên kết | Loại case | Tiêu đề test case | Điều kiện tiền đề | Các bước thực hiện | Dữ liệu test/input | Kết quả mong đợi | Kết quả thực thi | Evidence thực tế | Môi trường test | Người thực hiện | Ngày thực hiện | Số ticket bug | Trạng thái đánh giá spec | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-FUNC001-01 | FUNC-001 | Normal | Luồng thành công: upload ảnh ≤2MB (1MB) trên màn mới lưu và cập nhật avatar | OA đăng nhập, đã chọn bot, mở /admin/setting-bot/{id}. Ảnh JPEG ~1MB hợp lệ. | 1. Chọn file ảnh ~1MB trên vùng avatar<br>2. Quan sát toast và ảnh hiển thị<br>3. Làm mới màn kiểm tra ảnh đại diện đã đổi | File JPEG ~1MB. | Lưu thành công: toast 「アカウント画像を変更しました」, bots.bot_image trỏ file mới, màn hiển thị ảnh mới. | Đạt | | LOCAL | pipeline | 2026-08-25 | | | Studio #12825 (NEW-5) · `ui`/`auto`/`local-only` · REQ-004 · spec_ids: TICKET-39040, SRC-REGRESSION-011, SRC-REGRESSION-016 · note Studio: "Verify 3 tầng DB+màn+toast (RULE-07)." · auto pass 13165ms, actual: toast success + bot_image=/msg_template/media/images/990353641/990353675/bot/1787646895Qd9KEr.jpeg |
| TC-REGSHARED001-01 | REG-SHARED-001 | Normal | Regression: xóa ảnh đại diện trên màn mới vẫn thành công, không vướng check 2MB | OA đăng nhập, bot đang có ảnh đại diện, mở /admin/setting-bot/{id}. | 1. Bấm thao tác xóa ảnh đại diện<br>2. Quan sát toast và ảnh hiển thị<br>3. Làm mới màn xác nhận ảnh đã bị xóa | delete_image=1 qua thao tác xóa trên UI. | Xóa thành công, toast 「アカウント画像を削除しました」, bots.bot_image=null, màn hiện ảnh mặc định. | Đạt | | LOCAL | haodtb (manual) | 2026-08-26 | | | **regression** · Studio #12826 (NEW-6) · `ui`/`auto`/`local-only` · REQ-008 · note Studio: "Đối chứng âm: nhánh xóa không bị check size chặn oan." · ⚠️ **auto run #486 = `error`** (triage: modal 利用規約 `#popupTerm` che nút 削除, `hideModals` không dismiss được) → artifacts `486/tc-12826/` (screenshot + video + trace); sau đó haodtb chạy tay pass **không kèm evidence** |
| TC-TOOLKNOW002-01 | TOOL-KNOW-002 ⚠️ | Abnormal | Chặn ảnh vượt cỡ (5MB) khi upload avatar bot trên màn mới — hiện thông báo lỗi, không lưu | Đăng nhập OA (主管理者) qua /login-v2; đã chọn bot; mở màn Profile bot mới /admin/setting-bot/{id} (link sidebar v2). Chuẩn bị 1 file ảnh JPEG/PNG khoảng 5MB (nằm trong khoảng 2MB<size≤10MB từng lưu được trước fix). | 1. Trên màn Profile bot, bấm vùng chọn ảnh đại diện và chọn file ảnh ~5MB từ máy<br>2. Quan sát thông báo hiển thị và trạng thái ảnh đại diện<br>3. Mở lại màn (hoặc bấm làm mới) để xác nhận ảnh đại diện không thay đổi | File JPEG ~5MB (ví dụ 5242880 bytes). Có thể lặp với PNG cùng cỡ và tên file tiếng Nhật để phủ biến thể DI-16. | Hiện toast lỗi đúng chuỗi 「2MB以下のをアップしてください。」 (có dấu 。); KHÔNG gửi request lưu; ảnh đại diện giữ nguyên ảnh cũ, bots.bot_image không đổi. Trước fix: file 2–10MB được lưu im lặng không báo lỗi — nay phải bị chặn. | Đạt | | LOCAL | pipeline | 2026-08-25 | | | **TC verify trực tiếp bug fix** · Studio #12821 (NEW-1) · `ui`/`auto`/`local-only` · REQ-001 · spec_ids: TICKET-39040, SRC-REGRESSION-014, EP-SETBOT-UPDATE · note Studio: "Kích hoạt từ browser thật, không dựng payload thủ công. **Mức 2MB cần PM xác nhận.**" · auto pass 11294ms, actual: toast error đúng chuỗi + `update_requests=0` · ⚠️ mã quan điểm `TOOL-KNOW-002` **không có trong checklist-lme.md** |
| TC-FUNC004-01 | FUNC-004 | Boundary | Biên dung lượng: ảnh đúng 2MB được chấp nhận và lưu thành công trên màn mới | OA đăng nhập, đã chọn bot, mở /admin/setting-bot/{id}. Ảnh đúng 2097152 bytes. | 1. Chọn file ảnh đúng 2097152 bytes<br>2. Quan sát toast và ảnh đại diện<br>3. Làm mới màn xác nhận ảnh mới được áp dụng | File ảnh = 2097152 bytes (đúng biên). | Ảnh được chấp nhận, lưu ngay, toast 「アカウント画像を変更しました」, bots.bot_image cập nhật và màn hiển thị ảnh mới. | Đạt | | LOCAL | pipeline | 2026-08-25 | | | Studio #12823 (NEW-3) · `ui`/`auto`/`local-only` · REQ-003, REQ-004 · note Studio: "Điều kiện chặn > 1048576*2 nên đúng 2097152 phải PASS." · auto pass 16433ms, actual: toast success + bot_image cập nhật |
| TC-FUNC004-02 | FUNC-004 | Boundary | Biên dung lượng: ảnh 2MB - 1 byte vẫn được upload thành công trên màn mới | OA đăng nhập, đã chọn bot và mở /admin/setting-bot/{id}. Chuẩn bị file ảnh hợp lệ có dung lượng đúng 2097151 bytes (2MB - 1 byte). | 1. Chọn file ảnh đúng 2097151 bytes tại vùng avatar<br>2. Quan sát thông báo và ảnh đại diện sau khi chọn file<br>3. Làm mới màn để xác nhận ảnh mới vẫn được áp dụng | File ảnh hợp lệ = 2097151 bytes (2MB - 1 byte). | Ảnh không bị chặn bởi validation dung lượng, được upload/lưu thành công; hiển thị toast 「アカウント画像を変更しました」, bots.bot_image được cập nhật và màn hiển thị avatar mới sau khi reload. | Đạt | | LOCAL | haodtb (manual) | 2026-08-26 | | | ⭐ **TC DUY NHẤT do người viết** — Studio #12879 (NEW-13), `provenance.source = human`, `actor = haodtb@mcp`, `client_ref = task202-boundary-2mb-minus-1-new` · `ui`/`auto`/`local-only` · **`requirement_keys` rỗng** (chưa gắn REQ) · note Studio: "Boundary dưới ngưỡng: 2097151 bytes phải PASS." · manual pass **không kèm evidence** |
| TC-FUNC004-03 | FUNC-004 | Boundary | Biên dung lượng: ảnh 2MB + 1 byte bị từ chối trên màn mới | OA đăng nhập, đã chọn bot, mở /admin/setting-bot/{id}. Ảnh 2097153 bytes. | 1. Chọn file ảnh 2097153 bytes<br>2. Quan sát toast và trạng thái ảnh | File ảnh = 2097153 bytes. | Toast lỗi 「2MB以下のをアップしてください。」; ảnh không được lưu, giữ ảnh cũ. | Đạt | | LOCAL | pipeline | 2026-08-25 | | | Studio #12824 (NEW-4) · `ui`/`auto`/`local-only` · REQ-003, REQ-001 · note Studio: "Cặp biên với TC 2097152." · auto pass 6206ms, actual: toast error + `update_requests=0` |
| TC-FUNC001-02 | FUNC-001 | Normal | Luồng thành công: chọn ảnh ≤2MB trên bot-edit cũ, bấm 「保存」 lưu ảnh đại diện | OA đăng nhập, mở /admin/bot-edit?id={id}. Ảnh JPEG ~1MB hợp lệ. | 1. Chọn file ảnh ~1MB → xem preview hiển thị<br>2. Bấm nút 「保存」<br>3. Kiểm tra thông báo lưu và ảnh đại diện của bot | File JPEG ~1MB. | Preview hiển thị; bấm 「保存」 lưu thành công, bots.bot_image cập nhật, ảnh mới hiển thị. Luồng ≤2MB không bị chặn oan. | Đạt | | LOCAL | haodtb (manual) | 2026-08-26 | | | Studio #12849 (NEW-9) · `ui`/`auto`/`local-only` · REQ-007 · note Studio: "Verify DB + màn + thông báo." · ⚠️ **auto run #486 = `error`** — triage: `botChange` gọi `api.line.me` OAuth vô điều kiện với channel credentials giả → luôn 「入力した情報が間違っています」, **save-success bất khả thi trong env test**; chỉ verify được `jsAccepted=true` + `gatePassed=true`, **KHÔNG verify được "lưu thành công"** · artifacts `486/tc-12849/` · manual pass sau đó **không kèm evidence** |
| TC-REGSHARED001-02 | REG-SHARED-001 | Normal | Regression: lưu thay đổi tên bot không kèm ảnh trên màn bot-edit vẫn thành công | OA đăng nhập, mở /admin/bot-edit?id={id}. Bot đang có ảnh đại diện hiện tại và chuẩn bị một tên bot mới hợp lệ. | 1. Không chọn file ảnh mới<br>2. Thay đổi tên bot sang một giá trị hợp lệ<br>3. Bấm 「保存」<br>4. Làm mới màn và kiểm tra tên bot cùng avatar hiện tại | Tên bot mới hợp lệ; không đính kèm file ảnh. | Tên bot được cập nhật thành công. Không xuất hiện lỗi giới hạn 2MB. Avatar hiện tại giữ nguyên, chứng minh validation dung lượng chỉ áp dụng khi có file ảnh. | Đạt | | LOCAL | haodtb (manual) | 2026-08-26 | | | **regression** · Studio #12851 (NEW-11), version 2 · `ui`/`auto`/`local-only` · REQ-007 · note Studio: "Regression cho nhánh save không có image trong BotController@botChange" · ⚠️ **auto run #486 = `error`** (cùng rào LINE OAuth); chỉ verify được `not2mb=true` (không bị 2MB chặn oan), **không verify được lưu thành công** · artifacts `486/tc-12851/` · manual pass **không kèm evidence** · ⚠️ REQ-007 còn nhánh **đổi `channel_secret`** — Studio **không có TC** |
| TC-TOOLKNOW002-02 | TOOL-KNOW-002 ⚠️ | Abnormal | Chọn ảnh vượt cỡ (5MB) trên màn bot-edit cũ — JS cảnh báo và xóa file đã chọn | Đăng nhập OA qua /login-v2; mở màn cũ /admin/bot-edit?id={id} (vào từ danh sách tài khoản). Ảnh JPEG/PNG ~5MB. | 1. Bấm chọn ảnh đại diện và chọn file ~5MB<br>2. Quan sát hộp thoại cảnh báo và ô chọn file sau khi đóng cảnh báo<br>3. Kiểm tra vùng preview ảnh | File JPEG ~5MB (2MB<size≤10MB). | Hiện alert 「2MB以下のをアップしてください。」; sau khi đóng alert ô chọn file bị xóa (hành vi mới ở bot.js); preview không cập nhật ảnh quá cỡ. | Đạt | | LOCAL | pipeline | 2026-08-25 | | | Studio #12847 (NEW-7) · `ui`/`auto`/**`env-safe`** (TC duy nhất không `local-only`) · REQ-005 · note Studio: "Kích hoạt từ browser thật (readURL). Verify ô file rỗng sau reject (điểm mới)." · auto pass 7170ms, actual: `alert=["2MB以下のをアップしてください。"]`, `inputCleared=true`, `previewUnchanged=true` · ⚠️ mã quan điểm `TOOL-KNOW-002` **không có trong checklist-lme.md** |
| TC-FUNC004-04 | FUNC-004 | Boundary | Biên dung lượng: ảnh đúng 2MB trên bot-edit cũ được lưu qua 「保存」 | OA đăng nhập, mở /admin/bot-edit?id={id}. Ảnh đúng 2097152 bytes. | 1. Chọn file ảnh đúng 2097152 bytes → không bị JS chặn, preview hiển thị<br>2. Bấm 「保存」<br>3. Kiểm tra ảnh đại diện đã cập nhật | File ảnh đúng 2097152 bytes. | File đúng 2097152 bytes không bị JS chặn, preview hiển thị bình thường. Sau khi bấm 「保存」, server chấp nhận file, lưu ảnh thành công và avatar bot được cập nhật. | Đạt | | LOCAL | haodtb (manual) | 2026-08-26 | | | Studio #12850 (NEW-10), version 2 · `ui`/`auto`/`local-only` · REQ-005, REQ-007 · note Studio: "Boundary PASS: chỉ kiểm đúng 2MB = 2097152 bytes." · ⚠️ **auto run #486 = `error`** (cùng rào LINE OAuth); chỉ verify được `jsAccepted=true` + `gatePassed=true`, **không verify được lưu thành công** · artifacts `486/tc-12850/` · manual pass **không kèm evidence** · ⚠️ **màn cũ thiếu cặp biên `2MB+1`** ở tầng UI (chỉ có ở tầng API — `TC-TOOLVAL2001-02`) |
| TC-DEPLOYASSET001-01 | DEPLOY-ASSET-001 | Abnormal | Sau release, trình duyệt nạp đúng setting-bot.js/bot.js bản 2MB, không chạy JS 10MB cũ | User đã mở màn Profile bot trước release (cache JS 10MB cũ). Sau đó release bản fix. Không hard-reload. | 1. Trước release: mở /admin/setting-bot để cache setting-bot.js cũ<br>2. Sau release, mở lại màn Profile bot bằng điều hướng bình thường (không Ctrl+F5)<br>3. Chọn ảnh 2MB<size≤10MB và quan sát | Ảnh ~5MB; so sánh trước/sau release. | Sau release, chỉ reload hoặc điều hướng bình thường mà không dùng Ctrl+F5, browser phải sử dụng JS mới. Khi chọn file khoảng 5MB, hệ thống phải chặn với 「2MB以下のをアップしてください。」; không được tiếp tục hành vi cũ cho phép file đến 10MB. | Đạt | | LOCAL ⚠️ | haodtb (manual) | 2026-08-26 | | | 🚨 **KẾT QUẢ KHÔNG CÓ GIÁ TRỊ KẾT LUẬN** — Studio #12852 (NEW-12), version 2 · `ui`/**`manual`**/**`read-only`** · **`env_scope = ["staging"]`** nhưng đánh Đạt ở **`env = local`** · REQ-009 · note Studio: "Manual: **cần release thật để tái hiện cache asset; không kiểm được ở local build đơn lẻ.**" · manual pass **không kèm evidence** · quan điểm `DEPLOY-ASSET-001` là ★ ưu tiên **Cao** trong checklist-lme.md (Catalog D) |
| TC-TOOLVAL2001-01 | TOOL-VAL2-001 ⚠️ | Abnormal | Bypass JS: gửi ảnh 2MB + 1 byte trực tiếp tới server màn mới — phải bị từ chối | Có session OA hợp lệ (cookie + CSRF) của tài khoản sở hữu bot; biết bot_id. Chuẩn bị file ảnh đúng 2097153 bytes (2MB + 1 byte). | 1. Dùng session hợp lệ gửi trực tiếp POST /admin/ajax/setting-bot/update với multipart chứa field image = file 2097153 bytes và bot_id tương ứng, bỏ qua validation JS trên browser<br>2. Đọc response JSON<br>3. Kiểm tra ảnh đại diện của bot sau request | multipart/form-data: image=&lt;file 2097153 bytes&gt;, bot_id=&lt;hashid bot&gt;. | Response success=false với message 「2MB以下のをアップしてください。」; ảnh KHÔNG được lưu, bots.bot_image không đổi và không sinh file mới. | Đạt | | LOCAL | pipeline | 2026-08-25 | | | **TC server-side (bypass FE)** · Studio #12822 (NEW-2), version 2 · **`api`**/`auto`/`local-only` · REQ-002 · spec_ids: TICKET-39040, EP-SETBOT-UPDATE, SRC-REGRESSION-014, SRC-REGRESSION-010 · auto pass 133ms, actual: `resp={"success":false,"message":"2MB以下のをアップしてください。"}`, bot_image giữ sentinel · ⚠️ mã quan điểm `TOOL-VAL2-001` **không có trong checklist-lme.md** |
| TC-TOOLVAL2001-02 | TOOL-VAL2-001 ⚠️ | Abnormal | Bypass JS: gửi ảnh 2MB + 1 byte qua màn bot-edit cũ — server phải từ chối | Session OA hợp lệ (cookie + CSRF) sở hữu bot; biết id bot. Chuẩn bị file ảnh đúng 2097153 bytes (2MB + 1 byte). | 1. Gửi trực tiếp POST /admin/bot-save với multipart chứa image = file 2097153 bytes và các field bắt buộc như form màn cũ, bỏ qua validation JS<br>2. Đọc response<br>3. Kiểm tra bots.bot_image và thư mục media sau request | multipart mô phỏng form bot-edit: image=&lt;file 2097153 bytes&gt;. | Server từ chối file 2097153 bytes theo giới hạn 2MB và hiển thị/trả message 「2MB以下のをアップしてください。」; bots.bot_image giữ nguyên và không sinh file ảnh mới. | Đạt | | LOCAL | pipeline | 2026-08-25 | | | **TC server-side (bypass FE) — verify điểm fix mới của màn cũ** · Studio #12848 (NEW-8), version 2 · **`api`**/`auto`/`local-only` · REQ-006 · spec_ids: TICKET-39040, SRC-REGRESSION-013, EP-02, SRC-REGRESSION-010 · auto pass 79ms, actual: `resp={"success":false,"message":"2MB以下のをアップしてください。"}` |

---

## Đối chiếu mã quan điểm Studio ↔ `framework/checklist-lme.md`

| Mã quan điểm Studio | Số TC | Có trong `checklist-lme.md`? | Ghi chú |
|---|---|---|---|
| `FUNC-001` | 2 | ✅ Có — *Luồng chính hoàn tất đúng đặc tả* · ưu tiên **Cao** · Catalog C | |
| `FUNC-004` | 4 | ✅ Có — *Giới hạn trên/dưới về số ký tự, số lượng* · ưu tiên **Cao** · Catalog A, C | |
| `REG-SHARED-001` | 2 | ✅ Có — *Shared code / logic* · ưu tiên **Cao** · Catalog D (dòng 408) | |
| `DEPLOY-ASSET-001` | 1 | ✅ Có — *Version asset (JS/CSS/font/icon)* ★ · ưu tiên **Cao** · Catalog D | |
| `TOOL-KNOW-002` | 2 | ❌ **KHÔNG có** | Không có trong `checklist-lme.md` **lẫn** `catalog-lme.md`. `/review-tc` không map được coverage |
| `TOOL-VAL2-001` | 2 | ❌ **KHÔNG có** | Không có trong `checklist-lme.md` **lẫn** `catalog-lme.md`. `/review-tc` không map được coverage |

> **4/13 TC (31%)** gắn mã quan điểm ngoài bộ 80 quan điểm LME. Leader cần quyết: map lại sang mã chuẩn (VD `SEC-*` / `DATA-*` / `FUNC-*` cho validate server-side bypass FE) hay bổ sung mã mới vào `framework/checklist-lme.md`.

## Requirements Studio (từ `task_get_context`)

| REQ | Tiêu đề | Category | Risk | TC cover |
|---|---|---|---|---|
| REQ-001 | Màn mới `/admin/setting-bot` chặn ảnh >2MB có thông báo lỗi | validation | **High** | TC-TOOLKNOW002-01, TC-FUNC004-03 |
| REQ-002 | Server màn mới từ chối ảnh >2MB khi bypass JS | api | **High** | TC-TOOLVAL2001-01 |
| REQ-003 | Biên 2MB đúng 2097152 bytes | validation | Medium | TC-FUNC004-01, TC-FUNC004-03 |
| REQ-004 | Luồng lưu ảnh ≤2MB không đổi | ui | Medium | TC-FUNC001-01, TC-FUNC004-01 |
| REQ-005 | Màn cũ `/admin/bot-edit` chặn ảnh >2MB ở JS + clear input | validation | **High** | TC-TOOLKNOW002-02, TC-FUNC004-04 |
| REQ-006 | Server màn cũ (`botChange`) từ chối ảnh >2MB khi bypass JS | api | **High** | TC-TOOLVAL2001-02 |
| REQ-007 | Nhánh dùng chung của `botChange` không bị chặn oan (không ảnh / đổi tên / **đổi channel_secret**) | validation | Medium | TC-FUNC001-02, TC-REGSHARED001-02, TC-FUNC004-04 — ⚠️ **nhánh `channel_secret` chưa có TC** |
| REQ-008 | Xóa ảnh trên màn mới không bị chặn oan | ui | Low | TC-REGSHARED001-01 |
| REQ-009 | Asset JS mới được nạp sau release | ui | Low | TC-DEPLOYASSET001-01 — ⚠️ chạy sai env |

## Coverage Studio tự báo (`source = investigate`)

`total 13 · covered 0 · partial 11 · none 2` — **không ref nào đạt mức `covered`**.

| Ref chưa phủ (`level = none`) | Nội dung | Rủi ro |
|---|---|---|
| `BR-12` | Upload path `media/images/{adminId}/{botId}/bot/`; nếu `url_image = '/images/camera.png'` → xóa ảnh | Logic upload **dùng chung** với đường fix — 0 TC |
| `BR-13` | Upload resize max 2048px (giữ aspect ratio) | Ảnh ≤2MB nhưng **kích thước pixel lớn** (VD 6000×4000) → nhánh resize; 0 TC |

---

## Member tự check trước khi submit

> ⚠️ TCs này **không do member người viết** — checklist dưới đây **chưa được ai tick**. Giữ nguyên để Leader đối chiếu khi review.

### Coverage check
- [ ] Đã đọc kỹ `01-bug-task.md`
- [ ] Đã đọc kỹ `02-spec-reference.md` (nếu có)
- [ ] Đã đọc kỹ `03-dev-impact.md`, hiểu 4 mục
- [ ] **Mỗi impact** trong 4.1 / 4.2 / 4.3 có **ít nhất 1 TC** verify
- [ ] Có **ít nhất 1 TC** verify trực tiếp bug fix (reproduce flow KH)
- [ ] Có **ít nhất 1 TC** verify tính năng cũ không hỏng cho mỗi tính năng trong 4.3 (ghi "regression" ở Ghi chú)
- [ ] Có **ít nhất 1 Abnormal + 1 Boundary** cho mỗi data quan trọng trong 4.2
- [ ] Mọi TC có `Mã quan điểm liên kết`, steps rõ ràng, `Kết quả mong đợi` đo lường được
- [ ] `Tiêu đề test case` chứa **keyword** giúp Leader nhận ra impact TC đó cover

### Base quan điểm test LME (2 tầng)

| Mã quan điểm | Ưu tiên | ◯/× | Catalog đã tra | TC cover | Lý do nếu × |
|---|---|---|---|---|---|
| `<chưa duyệt — Studio không sinh bảng này; `test_viewpoint_selection` = null>` | | | | | |

- [ ] Đã duyệt **toàn bộ** tầng 1 từ trên xuống, không bỏ nhóm nào
- [ ] Mỗi quan điểm ◯ **đã mở đúng catalog** ở tầng 2 và **duyệt hết** khối tương ứng
- [ ] Mọi quan điểm ◯ ưu tiên **Cao** có đủ 3 loại case Normal + Abnormal + Boundary (**RULE-01**)
- [ ] Mọi × đều có lý do; × ở quan điểm **Cao** đã báo Leader duyệt (**RULE-03**)
- [ ] TC có output ra ngoài → `Kết quả mong đợi` đi tới **output cuối trên thiết bị thật** (**RULE-06**)
- [ ] TC CRUD verify đủ **3 tầng** DB + màn hình + output (**RULE-07**)
- [ ] Task chạm **media / domain / job / loadbalance / bill tiền** → có TC ghi `Môi trường test = PRODUCTION` (**RULE-08**)
- [ ] Task chạm đối tượng đã từng version-up → test **cả nhánh cũ và mới** (**RULE-09**)
- [ ] Mỗi TC đã ghi **loại evidence bắt buộc** ở Ghi chú (**RULE-02**)
- [ ] Mọi TC có `Trạng thái đánh giá spec`

<!-- TCs read-only: chép nguyên văn từ MCP LME TEST STUDIO task_id=202. KHÔNG sửa title/precondition/steps/expected ở file này — sửa trên Studio (testcase_update) rồi fetch lại. -->
