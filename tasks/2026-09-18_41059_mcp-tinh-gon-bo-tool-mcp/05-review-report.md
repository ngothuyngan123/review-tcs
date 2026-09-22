# 05 — Review Report

> Draft cho Leader verify. Chỉ ghi phần THIẾU + việc phải làm.

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | (1) Studio task #310 (ticket 41059, round 1, branch `improve/mcp_2026_09_16`) |
| Tổng số TC review | 110 |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

**Kết luận**: `4/16 vùng ảnh hưởng đủ TC có kết quả pass (D1-config local · TestController · danh sách quyền token · create_tag names[]) · 7 GAP · 6 RISK`

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G1 | F3 / T1 — model template chuyển `actions → ActionRef`: **FormButton · ImageTapZone · FormTemplateData · TextUrlSetting** (gắn action vào nút form template, tap zone ảnh, URL trong text template) | `dev-impact` | `NEW-98` (fail — chỉ ghi chung "nút bấm của template") | `GAP` — 0 TC cho tap zone ảnh, cho URL trong text template, cho nút form template; 0 TC xác nhận action **chạy thật** khi friend bấm trên LINE app (RULE-06) | `[BLOCKER]` |
| G2 | T1 — gắn `action_id` vào **welcome** (`WelcomeSettingMessageBuilder`) và **scenario step** (`StepMessageRepository.findActionIdByStepId`) | `dev-impact` | không có | `GAP` — Dev kê rõ ở 4.3 nhưng không TC nào gắn action vào welcome / step | `[MAJOR]` |
| G3 | T1 — `update_action` "check propagate" | `dev-impact` | `NEW-82` (fail), `NEW-98` (fail) | `RISK` — `NEW-82` chỉ kiểm sửa chính bản ghi action; `NEW-98` để expected mở ("phản ánh nội dung mới **hoặc** giữ bản sao") → không đo được. Chưa có TC khẳng định hành vi propagate trên từng nơi tham chiếu | `[MAJOR]` |
| G4 | T3 — `update_*_template` move `folder_id` + tham số `category` (spec §2/§4) | `diff code` | `NEW-46`, `NEW-47`, `NEW-48`, `NEW-49` (đều `error`) | `GAP` — Studio `dev_impact`: **`update_template` bị DISABLED**, move/category nằm ở `update_<loại>_template`. Cả 4 TC gọi tool không tồn tại → 0 TC hợp lệ cho move folder theo từng loại + `category` ở `create_*_template` | `[BLOCKER]` |
| G5 | Mục 3 Dev — `TextDataValidator` **bỏ check inline action** | `diff code` | không có (`NEW-57` chỉ cho broadcast) | `GAP` — bỏ validate là **nới lỏng**; chưa TC nào kiểm text template / URL setting truyền object action nội tuyến có bị từ chối hay bị lưu lọt | `[MAJOR]` |
| G6 | `send_message` — 3 ràng buộc phụ `shorten_url↔text`, `edited_content↔template_id`, `message↔media_items` | `diff code` | `NEW-23` (pass — chỉ kiểm nhiều nhánh cùng lúc), `NEW-29` (skip — chỉ default `shorten_url`) | `GAP` — chưa TC nào truyền **tham số phụ sai nhánh** (vd `shorten_url` kèm `template_id`) | `[MAJOR]` |
| G7 | `get_file_params` — nhận diện ảnh theo mime `image/*` **trước**, rồi **fallback đuôi file** | `diff code` | `NEW-30`, `NEW-31`, `NEW-34` (pass — chỉ nhánh mime) | `GAP` — nhánh fallback theo đuôi (mime chung chung + đuôi `.png`/`.webp`) chưa test | `[MAJOR]` |
| G8 | Spec §4 — `create_broadcast` "nhúng guide + **validation JIT**" (nguồn ảnh, zero-invention, send-timing) | `diff code` | `NEW-11` (fail — chỉ đọc description) | `GAP` — chưa TC nào gọi `create_broadcast` với input vi phạm để kiểm validation có chặn thật | `[MAJOR]` |
| G9 | F4 — `CategoryRepository.findActiveByBotIdAndKind` (nguồn của `list_folder`) | `dev-impact` | `NEW-42` (fail) | `RISK` — chưa kiểm folder **đã xoá / inactive** có bị loại khỏi `list_folder` không | `[MAJOR]` |
| G10 | D1 — `mcp.tools.disabled` trên **stag/dev6/prod** | `dev-impact` | `NEW-6`, `NEW-7` (pass, local), `NEW-8` (chưa chạy) | `RISK` — mới xác nhận ở local; cấu hình thật trên 3 env chưa ai đọc | `[MAJOR]` |
| G11 | T2 / T4 / T5 — broadcast · scenario step · autoreply · welcome · friend info · send_message · linect relay · chữ ký endpoint | `dev-impact` | 37 TC `skip` (`NEW-18/19/20/24/27/28/102` · `NEW-53/54/55/59/101` · `NEW-68/69/70/71` · `NEW-87/88/89/90` · `NEW-92/93` · `NEW-95/96` · `NEW-63/65` · `NEW-66/67` …) | `RISK` — có TC nhưng **chưa chạy** (Studio `dev_impact`: cần branch linect/web để E2E). Không đề xuất TC mới — cần deploy đủ PHP + linect rồi chạy lại | `[MAJOR]` |
| G12 | T1 / T3 / T4 — folder · filter · action · danh sách tool | `dev-impact` | `NEW-1/2/3`, `NEW-36→45`, `NEW-75→80`, `NEW-82/83/98/104` (fail) | `RISK` — TC có nhưng **toàn bộ fail**, chưa có bug ticket → xem §4 I2. Không đề xuất TC mới | `[MAJOR]` |
| G13 | T6 — deploy PHP → linect → MCP, **job linect** tách 3 job trên production | `dev-impact` | `NEW-16` (fail, local) | `RISK` — chỉ có case deploy sai thứ tự ở local; chưa có TC chạy luồng broadcast mới trên production (RULE-08) | `[MAJOR]` |

> G11 · G12: không đề xuất TC — chạy lại / raise bug là đủ.

---

## 2. Thiếu so với quan điểm test

**Kết luận**: `16 quan điểm Trigger khớp task · 7 chưa cover đủ`

| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q1 | `DATA-DB-001` | Cao | `RISK` — task có UPDATE ở `update_folder` / `update_filter` / `update_broadcast` / `update_action` nhưng **không TC nào kiểm `WHERE` scope trên 2 tài khoản trùng tên** (RULE-07). `NEW-40`/`NEW-77` fail, `NEW-63/65` skip, `NEW-64` chưa chạy | `[BLOCKER]` |
| Q2 | `DATA-MIG-001` / `COMPAT-LEGACY-001` | Cao | `GAP` — dữ liệu cũ lưu **action nội tuyến** chỉ được cover bởi `NEW-100` mang mã lạ `TOOL-OLDREC-001` (skip) → tính là chưa cover. Template group tạo từ thời tên `park` chưa được đọc/sửa lại bằng `*_group_template` (`NEW-51` skip) | `[BLOCKER]` |
| Q3 | `DATA-REF-001` | Cao | `RISK` — move template (đang được broadcast / step tham chiếu) và action dùng chung nhiều đối tượng: `NEW-83`, `NEW-98` fail, expected `NEW-98` không đo được; chưa TC kiểm nơi tham chiếu sau khi move | `[MAJOR]` |
| Q4 | `PERM-003` | Cao | `RISK` — 1 tài khoản nhiều bot: `NEW-26` (template bot khác, pass) · `NEW-58`/`NEW-84` (action bot khác, skip). Folder / filter / scenario step dùng ID của bot khác **cùng tài khoản** chưa test | `[MAJOR]` |
| Q5 | `MSG-004` | Cao | `RISK` — `NEW-21` chưa chạy; chưa có TC xem trên LINE app thật (iOS + Android) cho template có nút gắn `action_id` | `[MAJOR]` |
| Q6 | `DEPLOY-LIVE-001` | Cao | `RISK` — chỉ có `NEW-16` (Abnormal, fail). Thiếu Normal + Boundary: client đã kết nối **trước** deploy (tool list cũ còn cache) rồi gọi tiếp sau deploy (RULE-01) | `[MAJOR]` |
| Q7 | `ENV-003` / `JOB-001` | Cao | `RISK` — task chạm job nền (linect bỏ DB-direct broadcast) + media (`send_message` media, `get_file_params`); 102/110 TC chạy LOCAL, `NEW-8` chỉ đọc config. 0 TC chạy production (RULE-08) | `[MAJOR]` |

> Đã loại khỏi phạm vi: `DATA-BACKUP-001` (Dev ghi "Không đổi DB schema" → không thêm/đổi bảng), `PAY-*`, `LIFF-ENTRY-001` (không phát sinh URL mới cho LINE user).

---

## 3. TC trùng lặp nội dung

| Nhóm trùng | TC giữ lại | TC đề nghị xóa / gộp | Loại trùng | 4 yếu tố trùng nhau | Severity |
|---|---|---|---|---|---|
| DUP-1 | `NEW-104` | `NEW-106` → **gộp** `tech_note` (xác nhận broadcast + filter_v2 + schedule sinh qua PHP) vào `NEW-104` rồi xoá | `DUP-EXACT` | `FUNC-SEQ-001` × Normal × chuỗi `list_tags → create_action → create/update_broadcast (10:09 25/10/2026 + tag VIP) → gắn action_id → đọc lại` × cùng tiền đề (bot có tag VIP) | `[MINOR]` |
| DUP-2 | `NEW-107` | `NEW-105` | `DUP-EXACT` | `OUT-TRUTH-001` × Normal × cùng prompt "tạo broadcast 10:09 25/10/2026 cho tag VIP + gắn action sau gửi" × không guide → chấm theo chuỗi tool + tham số | `[MINOR]` |
| DUP-3 | `NEW-1` | `NEW-2` (tùy chọn) | `DUP-SUBSET` | Danh sách tool khớp đúng 83 tên §6 ⇒ đã bao gồm "12 tool bị bỏ không còn". Giữ `NEW-2` nếu muốn báo lỗi theo từng tên | `[NIT]` |

- **Gate đã chạy**: giả định xoá `NEW-106`, `NEW-105` → `FUNC-SEQ-001` còn `NEW-98`, `NEW-104`; `OUT-TRUTH-001` còn `NEW-11`, `NEW-80`, `NEW-107` → coverage §1 / §2 không đổi.
- Không có `DUP-INFLATE` / `DUP-CONFLICT`.
- Xoá thật do human làm trên Studio (`testcase_delete`).

---

## 4. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I1 | `[BLOCKER]` | Toàn bộ task #310 | Chỉ **29/110 TC pass (26%)**; 31 fail · 5 error · 37 skip · 8 chưa chạy | Deploy đủ PHP + linect theo đúng thứ tự rồi chạy lại toàn bộ; không kết luận "đã test" với tỷ lệ này |
| I2 | `[BLOCKER]` | 36 TC fail/error: `NEW-1/2/3/9/11/14/16/32/33/36→45/46→49/56/72/75→80/82/83/98/104`, `NEW-12` | **Không TC nào gắn bug ticket** (`bug_tickets` rỗng hết) dù task báo `openBugs=2`. Note của `NEW-1`, `NEW-2` tự ghi "fail thật, cần bug" | Raise bug (hoặc gắn 2 bug đang mở) cho từng cụm fail: danh sách tool (thừa `guide_filter_*`, thiếu `create/update_action`, `create/update_filter`, `*_folder`), folder, filter, action, phân quyền bot (`NEW-14`). Cụm template (`NEW-46→49`) xem I6 |
| I3 | `[MAJOR]` | Toàn bộ | **RULE-08 / ENV-003**: 102/110 TC chạy `LOCAL`, 0 TC chạy staging/production, trong khi task chạm job nền (linect) + media | Xem Q7, TC `TC-ENV003-01` · `TC-JOB001-01` ở §5 |
| I4 | `[MAJOR]` | Toàn bộ | **RULE-02**: cột `Evidence thực tế` rỗng 110/110 — kết quả pass chỉ là tự khai của pipeline | Đính kèm log request/response (tool call) hoặc ảnh DB/màn web cho các TC pass |
| I5 | `[MAJOR]` | 45 TC mang mã lạ: `API-001` (15) · `TOOL-ERRHYG-001` (10) · `TOOL-NEGCTRL-001` (7) · `API-CONTRACT-001` (6) · `RULE-12` (3) · `TOOL-SPECFIRST-001` (2) · `TOOL-OLDREC-001` (1) · `RULE-TOOL-029` (1) | Không có trong `checklist-lme.md` → không tính là cover. Đặc biệt `NEW-18/19/20` (Normal gửi tin) mang `API-001` nên `MSG-USER-001` / `FUNC-001` bị hụt Normal | Đổi mã trên Studio: `NEW-18/19/20` → `MSG-USER-001`; `NEW-100` → `DATA-MIG-001`; `NEW-3/22/23/32/38/41/49/59/73/79` → `OUT-TRUTH-001` hoặc `FUNC-002`; `NEW-10/103/9` (`RULE-12` là mã RULE, không phải quan điểm) → `REG-SHARED-001` |
| I6 | `[MAJOR]` | `NEW-46`, `NEW-47`, `NEW-48`, `NEW-49` | Gọi `update_template` — tool này **DISABLED** trong code (Studio `dev_impact`), nên cả 4 đều `error` chứ không phải lỗi sản phẩm | Viết lại theo `update_<loại>_template` (text / image / location / form / group) sau khi §6 #1 chốt; đề xuất thay ở §5 `TC-FUNC001-06/07/08` |
| I7 | `[MAJOR]` | `NEW-98` | Expected không đo được: "phản ánh nội dung mới **hoặc** giữ bản sao … hành vi phải nhất quán" — pass/fail tùy người chấm | Chốt hành vi propagate (§6 #6) rồi sửa expected thành 1 kết quả cụ thể |
| I8 | `[MAJOR]` | `03-dev-impact.md` | Auto-fill từ Redmine, checkbox "Tester verify auto-fill chính xác" chưa tick | Tester đọc lại journal #136848 rồi tick |
| I9 | `[MINOR]` | `NEW-104`, `NEW-105` | `screen` = null, `spec_ids` rỗng → không trace được về spec | Điền `screen = MCP – Kịch bản gọi nhiều tool (orchestration)` + `spec_ids` |
| I10 | `[NIT]` | Spec §5 | Postman collection và nộp lại tool list ChatGPT App không có TC | Checklist release thủ công, không cần TC |

---

## 5. TCs đề xuất bổ sung (21)

**Đã đối chiếu trước khi viết** (BƯỚC 5a/5b):

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | `kho-tcs/fa010-mautinnhan-テンプレート.md` · `fa007-settingaddfriend-あいさつメッセージ.md` · `fa009-phathanhtheobuoc-ステップ配信.md` · `fa008-broadcast-メッセージ配信.md` · `fa012-quanlythe-タグ管理.md`. Kho **không có** TC cho tầng MCP tool — chỉ dùng làm vùng regression phía web |
| Vùng regression phát hiện từ kho | `TC-TMT-70` (chuyển folder → màn khác hiện template ở folder mới) · `TC-BC-93` (template button có action URL khi gửi broadcast) · `TC-SAF-04` (trang welcome hiển thị lại đúng action đã lưu) · `TC-SCE-08` (folder scenario hiện ở 8 điểm tham chiếu) |
| Conflict expected vs kho | Không |
| GAP dùng lại TC kho (không viết mới) | Không — kho là TC màn web, không thay được TC gọi tool |
| Xác nhận chống trùng | Đã đối chiếu 110 TC của task #310 + 5 file kho — không TC đề xuất nào trùng. Với Q2, `NEW-100` đã cover dữ liệu cũ (chỉ sai mã) → **không viết lại**, chỉ đề nghị đổi mã (I5); §5 bổ sung phần `NEW-100` chưa có |

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-FUNC001-01 | API | FUNC-001 | MCP – create_action / template | Normal | auto | Tất cả | Gắn action_id vào nút bấm của form template (FormButton) | Bot test; đã deploy PHP (`save-action`, `/mcp/get-action`) + MCP branch `improve/mcp_2026_09_16` | 1. Gọi `create_action` tạo action "gắn tag TAG_41059_BTN", lấy `action_id`<br>2. Gọi `create_form_template` có 1 nút, gắn action bằng `action_id` đó<br>3. Gọi `get_template_detail` template vừa tạo<br>4. Mở template trên màn テンプレート của web admin, xem action của nút | Tag `TAG_41059_BTN`; tên template `FT_41059_<run>` | Bước 2 tạo thành công; bước 3 trả nút có action đọc lại đầy đủ (loại = gắn tag, tag = `TAG_41059_BTN`); màn web hiển thị đúng action đó trên nút | | Lấp G1 · Đánh giá spec: Spec ghi rõ (§4 "Action tách khỏi payload") · Evidence: response tool + ảnh màn template |
| TC-FUNC001-02 | API | FUNC-001 | MCP – create_action / template | Normal | auto | Tất cả | Gắn action_id vào tap zone của image template (ImageTapZone) | Như TC-FUNC001-01 | 1. `create_action` tạo action "gắn tag TAG_41059_TAP", lấy `action_id`<br>2. `get_file_params` cho 1 ảnh PNG, rồi `create_image_template` có 1 tap zone gắn `action_id`<br>3. `get_template_detail` đọc lại<br>4. Xem template trên web admin | Ảnh PNG 1040×1040; tag `TAG_41059_TAP` | Tap zone giữ đúng vùng đã khai và action đọc lại đúng tag `TAG_41059_TAP`; web hiển thị khớp | | Lấp G1 · Đánh giá spec: Spec ghi rõ · Evidence: response tool + ảnh màn template |
| TC-FUNC001-03 | API | FUNC-001 | MCP – create_action / template | Normal | auto | Tất cả | Gắn action_id vào URL trong text template (TextUrlSetting) | Như TC-FUNC001-01 | 1. `create_action` tạo action "gắn tag TAG_41059_URL", lấy `action_id`<br>2. `create_text_template` nội dung có 1 URL, cấu hình action khi click URL bằng `action_id`<br>3. `get_template_detail` đọc lại<br>4. Xem template trên web admin | Nội dung `Xem chi tiết https://example.com/41059`; tag `TAG_41059_URL` | URL giữ nguyên; cấu hình click URL trỏ đúng action (tag `TAG_41059_URL`); web hiển thị khớp | | Lấp G1 · regression — dẫn từ TC-BC-93 · Đánh giá spec: Spec ghi rõ · Evidence: response tool + ảnh màn template |
| TC-MSG004-01 | UI | MSG-004 | MCP – send_message → LINE app | Normal | manual | Tất cả | Friend bấm nút template gắn action_id trên LINE app → action chạy thật | Template ở TC-FUNC001-01 đã tạo; 1 friend test đã kết bạn bot trên máy iOS và 1 máy Android | 1. Gọi `send_message` nhánh `template_id` gửi template đó tới friend test<br>2. Trên LINE app (iOS) bấm nút<br>3. Lặp lại trên Android với friend thứ 2<br>4. Mở 友だち詳細 của 2 friend trên web admin | `template_id` của TC-FUNC001-01 | Tin hiển thị đúng nút trên cả 2 máy; sau khi bấm, 友だち詳細 của cả 2 friend có tag `TAG_41059_BTN` | | Lấp G1 + Q5 · RULE-06 · Đánh giá spec: Spec ghi rõ · Evidence: screenshot LINE iOS + Android + ảnh 友だち詳細 |
| TC-FUNC001-04 | API | FUNC-001 | MCP – update_welcome_message | Normal | auto | Tất cả | Gắn action_id vào tin chào mừng qua update_welcome_message | Bot test đã có tin chào mừng | 1. `create_action` tạo action "gắn tag TAG_41059_WEL", lấy `action_id`<br>2. `update_welcome_message` gắn action bằng `action_id`, không đổi nội dung tin<br>3. `get_welcome_message` đọc lại<br>4. Mở màn あいさつメッセージ tab メッセージ・アクション設定 | Tag `TAG_41059_WEL` | Action đọc lại đúng tag; nội dung tin chào mừng giữ nguyên; màn web hiển thị lại đúng action đã lưu | | Lấp G2 · regression — dẫn từ TC-SAF-04 · Đánh giá spec: Spec ghi rõ (journal 4.3) · Evidence: response tool + ảnh màn |
| TC-FUNC001-05 | API | FUNC-001 | MCP – create/update_scenario_step | Normal | auto | Tất cả | Gắn action_id vào bước kịch bản qua update_scenario_step | Bot test có 1 scenario có 1 step | 1. `create_action` tạo action "gắn tag TAG_41059_STEP", lấy `action_id`<br>2. `update_scenario_step` gắn action bằng `action_id`<br>3. `get_scenario_detail` đọc lại step<br>4. Mở step trên màn ステップ配信 | Tag `TAG_41059_STEP` | Step có đúng action đó khi đọc lại; nội dung tin của step không đổi; màn web khớp | | Lấp G2 · Đánh giá spec: Spec ghi rõ (journal 4.3) · Evidence: response tool + ảnh màn |
| TC-DATAREF001-01 | Data | DATA-REF-001 | MCP – update_action | Normal | auto | Tất cả | Sửa action đang được tag và template dùng chung → từng nơi tham chiếu đúng hành vi đã chốt | 1 action gắn vào 1 tag (`create_tag`) và 1 form template (TC-FUNC001-01) | 1. `update_action` đổi tag đích từ `TAG_A` sang `TAG_B`<br>2. `get_tag_detail` của tag<br>3. `get_template_detail` của template<br>4. Xem 2 đối tượng trên web admin | `TAG_A` → `TAG_B` | Cả 2 nơi tham chiếu cho **cùng** kết quả theo hành vi Dev chốt ở §6 #6 (cùng hiện `TAG_B`, hoặc cùng giữ `TAG_A`); không nơi nào rỗng hoặc lỗi | | Lấp G3 + Q3 · Đánh giá spec: Spec không ghi — chờ chốt §6 #6 · Evidence: response tool 2 đối tượng |
| TC-FUNC001-06 | API | FUNC-001 | MCP – update_*_template | Normal | auto | Tất cả | Chuyển folder cho từng loại template bằng update_<loại>_template | Bot test có folder `F_SRC`, `F_DST` và 5 template (text / image / location / form / group) ở `F_SRC` | 1. Với từng loại, gọi `update_<loại>_template` chỉ truyền `folder_id = F_DST`<br>2. `list_templates` theo `F_SRC` và `F_DST`<br>3. `get_template_detail` từng template | 5 template, 1 folder đích | Cả 5 template sang `F_DST`, biến mất khỏi `F_SRC`; nội dung từng template không đổi | | Lấp G4 · regression — dẫn từ TC-TMT-70 · Đánh giá spec: Spec ghi `update_template` — lệch code, chờ §6 #1 · Evidence: response list trước/sau · Thay cho NEW-46 |
| TC-FUNC001-07 | API | FUNC-001 | MCP – update_*_template | Abnormal | auto | Tất cả | Chuyển template sang folder không tồn tại hoặc folder của loại khác | Như TC-FUNC001-07 | 1. `update_text_template` với `folder_id` không tồn tại<br>2. `update_text_template` với `folder_id` là folder tag<br>3. `get_template_detail` | `folder_id = 99999999`; folder tag bất kỳ | Cả 2 lần bị từ chối với thông báo rõ; template vẫn ở `F_SRC`, nội dung không đổi | | Lấp G4 · Đánh giá spec: Spec không ghi — hỏi Dev · Evidence: response lỗi · Thay cho NEW-49 |
| TC-FUNC001-08 | API | FUNC-001 | MCP – create_*_template | Normal | auto | Tất cả | Tạo template với category scenario / autoreply / broadcast vào đúng nơi | Bot test có 1 scenario, 1 autoreply, 1 broadcast chưa gửi | 1. `create_text_template` với `category = scenario` (kèm step đích)<br>2. Lặp với `category = autoreply`, `category = broadcast`<br>3. Mở từng đối tượng đích trên web admin | 3 lần gọi, nội dung `CAT_41059_<category>` | Mỗi template xuất hiện đúng trong đối tượng của category đã chọn, không lọt vào kho template chung | | Lấp G4 · Đánh giá spec: Spec ghi rõ (§4 improve) · Evidence: ảnh màn 3 đối tượng |
| TC-DATAREF001-02 | Data | DATA-REF-001 | MCP – update_*_template | Normal | manual | Tất cả | Chuyển folder template đang được broadcast và scenario step dùng → nơi tham chiếu không đổi | 1 template đang dùng trong 1 broadcast chưa gửi và 1 scenario step | 1. `update_text_template` chuyển template sang `F_DST`<br>2. Mở broadcast và step đó trên web admin<br>3. Bấm テスト送信 broadcast tới friend test | Template dùng chung | Broadcast và step vẫn hiện đúng nội dung template; tin test nhận đúng trên LINE | | Lấp Q3 · regression — dẫn từ TC-TMT-70 · Đánh giá spec: Spec không ghi · Evidence: ảnh màn + screenshot LINE |
| TC-FUNC002-01 | API | FUNC-002 | MCP – create_text_template | Abnormal | auto | Tất cả | Text template truyền action nội tuyến trong URL setting bị từ chối | Bot test | 1. `create_text_template` có URL, trong phần action của URL truyền **object action** (không phải `action_id`)<br>2. `list_templates` tìm tên template | Object `{type: tag, tag_id: <id>}` | Bị từ chối với thông báo chỉ nhận `action_id`; không có template nào được tạo | | Lấp G5 · Đánh giá spec: Spec ghi rõ (§4 quy tắc mới) · Evidence: response lỗi + list |
| TC-FUNC002-02 | API | FUNC-002 | MCP – send_message | Abnormal | auto | Tất cả | send_message truyền tham số phụ sai nhánh bị chặn, không gửi tin | Friend test thuộc bot | 1. Nhánh `template_id` kèm `shorten_url = true`<br>2. Nhánh text kèm `edited_content`<br>3. Nhánh text kèm `message` nhưng không có `media_items` (nếu `message` chỉ đi với media)<br>4. Xem 1:1チャット của friend | 3 bộ tham số trên | Cả 3 lần bị từ chối với thông báo nêu tham số sai nhánh; friend không nhận tin nào | | Lấp G6 · Đánh giá spec: Spec không ghi — lấy từ Studio dev_impact, hỏi Dev xác nhận 3 ràng buộc · Evidence: response + ảnh chat |
| TC-FUNC004-01 | API | FUNC-004 | MCP – get_file_params | Boundary | auto | Tất cả | get_file_params nhận diện ảnh bằng đuôi file khi mime không phải image/* | Có URL file ảnh thật trả mime `application/octet-stream` | 1. Gọi `get_file_params` với file `.png` mime `application/octet-stream`<br>2. Lặp với `.webp`<br>3. Lặp với file `.txt` mime `application/octet-stream` | 3 URL file | `.png`, `.webp` → trả kích thước ảnh đúng; `.txt` → xử lý như file thường (echo tham số) hoặc báo không hỗ trợ, không lỗi hệ thống | | Lấp G7 · Đánh giá spec: Spec không ghi (fallback theo đuôi chỉ có trong code) · Evidence: response 3 lần |
| TC-OUTTRUTH001-01 | API | OUT-TRUTH-001 | MCP – create_broadcast | Abnormal | auto | Tất cả | create_broadcast với input vi phạm quy tắc đã nhúng từ guide bị chặn | Bot test | 1. `create_broadcast` với giờ gửi ở quá khứ<br>2. `create_broadcast` với ảnh có URL **không** lấy từ `get_file_params`<br>3. `list_broadcasts` | Giờ gửi = hôm qua; URL ảnh ngoài | Cả 2 lần bị chặn với thông báo nêu lý do; không broadcast nào được tạo | | Lấp G8 · Đánh giá spec: Spec không ghi chi tiết rule "validation JIT" — hỏi Dev danh sách rule · Evidence: response lỗi + list |
| TC-LIST001-01 | UI | LIST-001 | MCP – list_folder | Boundary | auto | Tất cả | list_folder không trả folder đã xoá và folder của bot khác | Bot A có folder tag `FD_DEL` (đã xoá trên web) và `FD_OK`; bot B có folder tag cùng tên `FD_OK` | 1. `list_folder` `type = tag` cho bot A<br>2. Lặp với `type = scenario`, `friend_info` | — | Chỉ trả `FD_OK` của bot A; không có `FD_DEL`, không có folder của bot B | | Lấp G9 · Đánh giá spec: Spec không ghi · Evidence: response list |
| TC-DATADB001-01 | Data | DATA-DB-001 | MCP – update_folder / update_filter / update_broadcast | Normal | manual | Tất cả | Update qua tool ở bot A không đụng bản ghi trùng tên ở bot B | 2 tài khoản, mỗi tài khoản 1 bot; cùng tạo folder `FD_SAME`, scenario có filter, broadcast `BC_SAME` | 1. Token tài khoản A: `update_folder` đổi tên `FD_SAME`<br>2. `update_filter` target scenario thay điều kiện<br>3. `update_broadcast` đổi tiêu đề `BC_SAME`<br>4. Query DB 2 bot trước/sau + mở web admin bot B | Tên trùng ở 2 bot | Chỉ bản ghi bot A đổi; bot B giữ nguyên tên, điều kiện lọc, tiêu đề; không phát sinh bản ghi mới | | Lấp Q1 · RULE-07 · Đánh giá spec: Spec không ghi · Evidence: query DB trước/sau 2 bot |
| TC-PERM003-01 | API | PERM-003 | MCP – folder / filter / scenario step | Abnormal | auto | Tất cả | Dùng ID của bot khác cùng tài khoản bị chặn | 1 tài khoản có bot 1, bot 2 | 1. `bot_id = bot1`, `update_folder` với `folder_id` của bot 2<br>2. `update_filter` với scenario của bot 2<br>3. `update_scenario_step` với step của bot 2<br>4. Mở web admin bot 2 | ID thuộc bot 2 | Cả 3 lần bị từ chối; dữ liệu bot 2 không đổi | | Lấp Q4 · Đánh giá spec: Spec không ghi · Evidence: response lỗi + ảnh màn bot 2 |
| TC-DEPLOYLIVE001-01 | API | DEPLOY-LIVE-001 | MCP – tool list sau deploy | Boundary | manual | staging | Client đã kết nối trước deploy gọi tiếp tool cũ và tool mới sau deploy | Client MCP (ChatGPT/Claude) kết nối và đã tải tool list bản cũ | 1. Giữ phiên, deploy bản mới<br>2. Không reconnect, gọi `edit_broadcast_info`<br>3. Gọi `send_message` với `lme_user_id`<br>4. Refresh tool list, gọi `update_broadcast` | — | Bước 2, 3 trả lỗi rõ (tool không tồn tại / thiếu tham số), không lỗi 500, không tạo dữ liệu dở dang; bước 4 thành công | | Lấp Q6 · Đánh giá spec: Spec không ghi · Evidence: log request/response |
| TC-ENV003-01 | API | ENV-003 | MCP – broadcast qua linect relay PHP | Normal | manual | product | Broadcast tạo qua tool trên production được job broadcast gửi đúng giờ | Production đã deploy PHP → linect → MCP; bot test nội bộ + friend test | 1. `create_broadcast` hẹn giờ +10 phút, lọc theo tag test<br>2. Chờ tới giờ gửi<br>3. Xem tin trên LINE app friend test<br>4. Xem tab 配信履歴 trên web admin | Tag test chỉ gắn cho friend test | Friend test nhận đúng 1 tin đúng giờ; 配信履歴 có bản ghi với số gửi = 1 | | Lấp Q7 + G13 · RULE-08 · Đánh giá spec: Spec ghi rõ (§5) · Evidence: screenshot LINE + ảnh 配信履歴 |
| TC-JOB001-01 | API | JOB-001 | MCP – send_message media / get_file_params | Normal | manual | product | Gửi media qua send_message trên production dùng domain media thật | Production đã deploy; friend test | 1. `get_file_params` cho 1 ảnh, 1 video<br>2. `send_message` nhánh `media_items` gửi 2 file tới friend test<br>3. Xem trên LINE app | Ảnh JPG, video MP4 | `get_file_params` trả kích thước ảnh đúng; friend nhận đủ ảnh + video, mở được | | Lấp Q7 · RULE-08 (media) · Đánh giá spec: Spec ghi rõ (§2) · Evidence: response + screenshot LINE |

> Không đề xuất TC mới cho G10 (chạy `NEW-8`), G11 (chạy lại 37 TC skip), G12 (raise bug cho TC fail), Q2 (đổi mã `NEW-100` → `DATA-MIG-001` và chạy `NEW-51` sau khi seed template group tạo trước refactor — đã đủ Normal; Boundary action cũ trỏ tới tag đã xoá gộp vào `NEW-100` như 1 bộ dữ liệu).

---

## 6. Spec update needed

| # | Section spec | Nội dung cần update | Nguồn mâu thuẫn | Ai chốt |
|---|---|---|---|---|
| 1 | §2 `bulk_move_templates → update_template` · §4 `create_*_template / update_template` | Spec ghi **`update_template`** nhận folder/category; code để `update_template` **DISABLED**, move/category nằm ở `update_<loại>_template` | Spec vs code (Studio `dev_impact`) · `NEW-46→49` error | Dev / Leader |
| 2 | §1 Bỏ hẳn | Spec bỏ `guide_filter_structure`, `guide_filter_grouping`; code **vẫn active** (`McpComponentGuideTool.java:43-46`) | Spec vs code · `NEW-1`, `NEW-2` fail | Dev — bug hay đổi scope |
| 3 | §6 danh sách 83 tool · nhóm Autoreply | `create_autoreply` / `update_autoreply` nằm trong danh sách active, nhưng `mcp.tools.disabled` tắt cả 2 trên **mọi env** (kể cả prod) → tool mới không ra được production. Tổng số tool: spec 83 · Dev ghi 84 | Spec vs D1 · `NEW-1` vs `NEW-6` | PM / Dev |
| 4 | §3 Đổi tên | Thiếu 2 đổi tên có trong code: `list_compliant_statuses → list_handling_statuses`, tham số `lme_user_id → lmessage_friend_id` của `send_message` (breaking cho client cũ); thiếu tool mới `update_conversation_handling_status` ở §4 | Code vs spec (REQ-002 / REQ-005 / REQ-023) | Dev |
| 5 | §6 ghi chú cuối | Ghi chú giữ `get_park_template_detail`, nhưng §6 nhóm Template ghi `get_group_template_detail` (`NEW-52` pass với tên mới) | Mâu thuẫn trong chính spec | Dev |
| 6 | §4 "Action tách khỏi payload" | Chưa nêu: sửa action bằng `update_action` thì các đối tượng đã gắn `action_id` (tag, template, welcome, step, broadcast) **đổi theo hay giữ bản sao**; dữ liệu cũ lưu action nội tuyến có migrate sang `action_id` không | `NEW-98` expected mở · journal "update_action check propagate" | Dev / PO |
| 7 | §2 `create_broadcast` improve | "Validation JIT" chưa liệt kê rule cụ thể (giờ gửi, nguồn ảnh, zero-invention) → không viết được expected | TC-OUTTRUTH001-01 | Dev |
