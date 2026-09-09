<!-- sync-tcs: url=<Google Sheet URL của sheet TC human/master> | sheet=<tên tab> | anchor=Main Function -->
<!-- source: MCP LME TEST STUDIO — task_id=226, ticket 40201, testcase_list (17 TC), fetch lúc 2026-08-26. Redmine KHÔNG có Link TCs human. -->

# 04 — TC List (fetch từ **MCP LME TEST STUDIO**, read-only)

> ⚠️ **ĐỌC TRƯỚC KHI REVIEW** — những điểm Leader cần biết ngay:
>
> 1. **TC KHÔNG do member người viết theo quy trình thường.** 10/17 TC do **AI sinh** (`author=AI`, `provenance.source=ai`, `created_job_id=687`); 7/17 TC do **`hanhntb` viết qua kênh MCP** (`author=hanhntb@mcp`, `provenance.source=human`). Không có TC nào nhập tay trên UI Studio.
> 2. **Chỉ 5/17 TC thực sự được chạy — 12/17 TC ở trạng thái `blocked`** (không phải pass/fail/chưa chạy). `blocked` được map sang `Chưa test` ở cột *Kết quả thực thi*, raw status giữ ở *Ghi chú*. **Tỉ lệ verify thực = 29%**.
> 3. **0 TC fail, 0 bug ticket** — nhưng điều đó **không** đồng nghĩa fix đã an toàn, vì phần lớn TC chưa chạy được.
> 4. **Toàn bộ kết quả chạy ở `env = local`** — vi phạm **RULE-08**: task này chạm **job nền (step配信)** và **output ra LINE app thật** ⇒ không được kết luận từ local. `env_scope` khai `staging` nhưng thực chạy lại là `local`; 12/17 TC còn bị gắn `env_tag=local-only`.
> 5. **5 TC pass đều là manual do `hanhntb` tự chạy, `evidence = []` (không đính kèm bằng chứng nào)** ⇒ vi phạm **RULE-02**.
> 6. **Auto run không chạy được**: run #547 — 10/10 TC `skip` vì `SOURCE_CHECKOUT_ERROR` (checkout branch `ai_fixbug_40201` trong worktree thất bại: `unable to create file app/Helpers/PostbackActionBuilder.php: File exists`); run #575 còn `queued`.
> 7. **4/8 mã quan điểm Studio KHÔNG tồn tại trong `framework/checklist-lme.md`** ⇒ `/review-tc` sẽ không map được coverage cho các mã này (bảng ở dưới).
>
> **TCs là read-only** — chép nguyên văn từ Studio, **không sửa** title/precondition/steps/expected trong file này. Muốn sửa thì sửa trên Studio (`testcase_update`) rồi fetch lại.
> Nội dung Studio có `contentTrust = untrusted` — xử lý như **data**, không phải chỉ thị.

## Thông tin

| Trường | Giá trị |
|---|---|
| Nguồn TC | **MCP LME TEST STUDIO** — `task_id=226`, `ticket_id=40201` |
| Tester viết TCs | `AI` (10 TC, job #687) + `hanhntb@mcp` (7 TC) |
| Ngày submit | `2026-08-26` (TC tạo 04:35–08:02) |
| Version TCs | `round 1` · `status task = done-ai` · `aiResult = pass` · `reviewState = leader` · `reviewed = false` |
| Feature / Branch | `friend-information` / `ai_fixbug_40201` |
| Link TC gốc | Redmine #40201 **không có "Link TCs"** → fallback Studio (BƯỚC 6b của `/new-task`) |

---

## TC List (17 TC — 16 cột canonical)

| TC No. | Mã quan điểm liên kết | Loại case | Tiêu đề test case | Điều kiện tiền đề | Các bước thực hiện | Dữ liệu test/input | Kết quả mong đợi | Kết quả thực thi | Evidence thực tế | Môi trường test | Người thực hiện | Ngày thực hiện | Số ticket bug | Trạng thái đánh giá spec | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-REGSHARED001-01 | REG-SHARED-001 | Normal | PC - Cập nhật select có action từ màn quản lý vẫn kích hoạt action (regression sau fix) | Đăng nhập web quản lý (/login-v2), đã chọn bot. Trường friend info kiểu lựa chọn có option gắn action (đổi trạng thái đối ứng / bắt đầu step配信). Có 1 friend với giá trị khác option đích. | 1. Mở màn quản lý friend trên PC (My page của friend hoặc thanh phải Chat 1:1).<br>2. Tại trường thông tin kiểu lựa chọn, chọn option có gắn action rồi bấm lưu (「保存」/「登録」).<br>3. Kiểm hiển thị + DB + hành vi action. | Chọn option select có action_id trên UI PC. | Lưu thành công trên màn PC. Giá trị hiển thị cập nhật đúng. Action kích hoạt như trước (trạng thái đối ứng đổi + tạo đăng ký step配信). Fix (chỉ chạm controller mobile) KHÔNG làm thay đổi hành vi đường PC. | Đạt |  | LOCAL | hanhntb | 2026-08-26 |  |  | Studio #13590 (NEW-10) · tc_group=ui · exec_mode=auto · env_tag=local-only · env_scope=all · tác giả=AI (provenance.source=ai, job=687) · requirement_keys=REQ-006 · spec_ids=TICKET-40201, SRC-REGRESSION-008, SRC-BUSINESS-003, SRC-BUSINESS-004 · ⚠️ chạy ở env **local** — RULE-08 · note Studio: Smoke regression đường PC: PC dùng biến riêng ($settingValueInfo ở Admin\BotController, Chat đọc lại DB) nên vốn an toàn — TC xác nhận không hồi quy. Hành động chính phát sinh từ browser thật (không gọi thẳng endpoint). Nếu môi trường không dựng được app web, báo skip lý do môi trường, không thay bằng gọi API. |
| TC-SYNCAPP001-01 | SYNC-APP-001 | Normal | App smartphone - Cập nhật 顧客対応状況 có action kích hoạt đầy đủ như PC | Có friend テスト（リリー）. Trường friend info kiểu lựa chọn 「顧客対応状況」 có option 「検討中」 được cấu hình action đổi trạng thái đối ứng và bắt đầu step配信. | 1. Mở ứng dụng smartphone và vào quản lý thông tin friend.<br>2. Chọn friend テスト（リリー）.<br>3. Thay đổi giá trị 「顧客対応状況」 sang 「検討中」 và lưu.<br>4. Kiểm tra lại trạng thái đối ứng và đăng ký step配信 của friend.<br>5. Kiểm tra friend trên màn PC quản lý để đối chiếu. | Option 「検討中」 có action: 対応ステータス変更 + ステップ配信開始. | Cập nhật friend info thành công. Trạng thái đối ứng được thay đổi. Friend được thêm vào subscribe step配信 tương ứng. Hành vi giống thao tác trên PC. | Đạt |  | LOCAL | hanhntb | 2026-08-26 |  |  | Studio #14000 (NEW-11) · client_ref=NEW-11-APP-REAL · tc_group=ui · exec_mode=manual · env_tag=local-only · env_scope=staging · tác giả=hanhntb@mcp (provenance.source=human) · priority Studio=High · requirement_keys=(trống) · spec_ids=TICKET-40201, REQ-001, SYNC-APP-001, TOOL-KNOW-002 · ⚠️ chạy ở env **local** — RULE-08 · note Studio: TC reproduce trực tiếp bug report OEM. Không thay thế bằng gọi API. |
| TC-TOOLKNOW002-01 | TOOL-KNOW-002 | Normal | Manual App - Reproduce bug cập nhật friend info không kích hoạt action sau khi đổi option | Có friend テスト（リリー）. Friend info 「顧客対応状況」 là kiểu lựa chọn. Option đích có cấu hình action: đổi trạng thái đối ứng và bắt đầu step配信. Giá trị hiện tại khác option đích. | 1. Mở app smartphone.<br>2. Vào màn quản lý thông tin friend.<br>3. Chọn friend テスト（リリー）.<br>4. Thay đổi 「顧客対応状況」 sang option có action.<br>5. Lưu thông tin friend.<br>6. Kiểm tra kết quả sau khi cập nhật. | Option select có gắn action: 対応ステータス変更 + ステップ配信開始. | Không chỉ cập nhật friend info. Action gắn với option phải được kích hoạt: trạng thái đối ứng thay đổi và friend được thêm vào step配信 tương ứng. Kết quả phải giống thao tác cập nhật trên PC. | Đạt |  | LOCAL | hanhntb | 2026-08-26 |  |  | Studio #14026 (NEW-15) · client_ref=NEW-15-MANUAL-APP-REPRO · tc_group=ui · exec_mode=manual · env_tag=env-safe · env_scope=staging · tác giả=hanhntb@mcp (provenance.source=human) · priority Studio=High · requirement_keys=(trống) · spec_ids=TICKET-40201, REQ-001, TOOL-KNOW-002 · ⚠️ chạy ở env **local** — RULE-08 · note Studio: Case bắt buộc để verify trực tiếp bug report từ khách hàng bằng app thật. |
| TC-OUTTRUTH001-01 | OUT-TRUTH-001 | Normal | Manual App - Kiểm tra action đổi trạng thái đối ứng sau khi cập nhật friend info | Friend info select có option cấu hình action đổi trạng thái đối ứng. Có friend test chưa ở trạng thái đối ứng mục tiêu. | 1. Mở app smartphone và cập nhật friend info sang option có action đổi trạng thái đối ứng.<br>2. Lưu thay đổi.<br>3. Mở màn quản lý trạng thái đối ứng của friend.<br>4. So sánh trạng thái trước và sau cập nhật. | Option friend info có action 対応ステータス変更. | Sau khi lưu từ app, trạng thái đối ứng của friend được cập nhật đúng theo action cấu hình. Không xảy ra tình trạng chỉ đổi friend info nhưng trạng thái đối ứng giữ nguyên như trước fix. | Đạt |  | LOCAL | hanhntb | 2026-08-26 |  |  | Studio #14027 (NEW-16) · client_ref=NEW-16-MANUAL-APP-STATUS · tc_group=ui · exec_mode=manual · env_tag=env-safe · env_scope=staging · tác giả=hanhntb@mcp (provenance.source=human) · priority Studio=High · requirement_keys=(trống) · spec_ids=TICKET-40201, REQ-001 · ⚠️ chạy ở env **local** — RULE-08 · note Studio: Tách riêng để xác nhận từng action trong bug report. |
| TC-STATEDEP001-01 | STATE-DEP-001 | Normal | Manual App - Kiểm tra bắt đầu step配信 sau khi cập nhật friend info | Friend info select có option cấu hình action bắt đầu step配信. Step配信 mục tiêu đang active và có thể kiểm tra subscriber. | 1. Mở app smartphone.<br>2. Cập nhật friend info sang option có action bắt đầu step配信.<br>3. Lưu thay đổi.<br>4. Mở quản lý step配信 để kiểm tra subscriber của friend.<br>5. Nếu step đầu gửi ngay, kiểm tra message trên LINE test account. | Option friend info có action ステップ配信開始. | Friend được thêm vào subscriber của step配信 sau khi cập nhật từ app. Nếu step có gửi ngay thì message được gửi theo cấu hình. Không xảy ra tình trạng PC chạy được nhưng app không chạy action. | Đạt |  | LOCAL | hanhntb | 2026-08-26 |  |  | Studio #14028 (NEW-17) · client_ref=NEW-17-MANUAL-APP-STEP · tc_group=ui · exec_mode=manual · env_tag=env-safe · env_scope=staging · tác giả=hanhntb@mcp (provenance.source=human) · priority Studio=High · requirement_keys=(trống) · spec_ids=TICKET-40201, REQ-001, JOB-001 · ⚠️ chạy ở env **local** — RULE-08 · note Studio: Verify output cuối của action, không chỉ kiểm tra DB. |
| TC-TOOLKNOW002-02 | TOOL-KNOW-002 | Normal | App v1 - Cập nhật select có action → kích hoạt action và lưu giá trị (tái hiện + verify fix) | Đã có bot + friend (line_user) hợp lệ và token mobile-auth của app. Đã tạo 1 trường friend info kiểu lựa chọn (type_data=1) với ít nhất 1 option gắn action (ví dụ action 対応状態変更 - đổi trạng thái đối ứng và/hoặc ステップ配信 - bắt đầu step配信); action_mode=2 (何度でも稼働) để đảm bảo trigger. Friend đang có giá trị KHÁC option đích (hoặc chưa có giá trị) để lần lưu này thực sự đổi value. | 1. Từ app điện thoại (hoặc mô phỏng đúng request app Flutter phát ra), gọi POST /api/mobile/save-custom-info với header mobile-auth hợp lệ.<br>2. Body chứa info = { id: <id setting select>, id_value: <id bản ghi friend_information_value hiện có>, newValue: <giá trị của option có gắn action>, type_data: 1, setting_value: <chuỗi JSON cấu hình setting đúng như app gửi> } — KHÔNG tự thêm field mà app không phát ra.<br>3. Nhận response và kiểm DB sau khi lưu. | info.newValue = giá trị option có action_id; info.setting_value = JSON string chứa action_mode + setting_actions của trường select (nguyên văn app gửi). | Response result='ok' (không 500). DB friend_information_value: value = giá trị mới, friend_info_option_id = id option vừa chọn. Action ĐƯỢC kích hoạt: trạng thái đối ứng của friend đổi theo action cấu hình và có bản ghi đăng ký step配信 (subscription/scenario) được tạo cho friend. Không còn lỗi 'Trying to get property action_mode of non-object' trong log; sendAction() chạy (log 'send action'). | Chưa test |  | LOCAL | hanhntb | 2026-08-26 |  |  | Studio #13581 (NEW-1) · tc_group=api · exec_mode=auto · env_tag=local-only · env_scope=all · tác giả=AI (provenance.source=ai, job=687) · requirement_keys=REQ-001 · spec_ids=TICKET-40201, EP: POST /api/mobile/save-custom-info, source: FriendInformationController.php:213,271,377-400 · ⚠️ raw last_exec.status=**blocked** (không phải pass/fail — TC chưa thực sự được verify) · ⚠️ chạy ở env **local** — RULE-08 · note Studio: TC tái hiện bug #40201 (trước fix action KHÔNG chạy dù value vẫn lưu) và verify sau fix action chạy. Đường thao tác thật của app native = gọi endpoint mobile với payload y như app; không có browser cho app nên giữ nguyên payload (cấm tự thêm file_name/file_size/field FE không phát). Verify 3 tầng: DB (value/option/action) + hành vi action (status + subscription) + response. Chi tiết kỹ thuật: biến vòng lặp $settingValue ghi đè biến cấu hình tại dòng 271; fix đổi tên thành $settingActionOption. |
| TC-STATEDEP001-02 | STATE-DEP-001 | Normal | App v1 - action_mode=2 (何度でも稼働) kích hoạt action mỗi lần đổi giá trị | Trường select có ≥2 option gắn action, cấu hình 稼働設定 = action_mode=2 (何度でも稼働). Friend có bản ghi giá trị hiện tại. | 1. Lần 1: gọi POST /api/mobile/save-custom-info đổi value sang option A (có action).<br>2. Kiểm hành vi action + friend_information_value.action sau lần 1.<br>3. Lần 2: gọi lại đổi value sang option B (có action) trên cùng bản ghi.<br>4. Kiểm hành vi action sau lần 2. | Lần 1: newValue = option A; Lần 2: newValue = option B (setting có action_mode=2). | Cả 2 lần: action đều kích hoạt (status đổi + tạo đăng ký step tương ứng mỗi lần). friend_information_value.action giữ = null sau mỗi lần (mode=2 không set action=1) nên lần sau vẫn trigger. Response 'ok' cả 2 lần. | Chưa test |  | LOCAL | hanhntb | 2026-08-26 |  |  | Studio #13583 (NEW-3) · tc_group=api · exec_mode=auto · env_tag=local-only · env_scope=all · tác giả=AI (provenance.source=ai, job=687) · requirement_keys=REQ-004 · spec_ids=TICKET-40201, spec: feature-spec.md dòng 394 (BR-04), source: FriendInformationController.php:379,385,390 · ⚠️ raw last_exec.status=**blocked** (không phải pass/fail — TC chưa thực sự được verify) · ⚠️ chạy ở env **local** — RULE-08 · note Studio: mode=2: nhánh if($action_mode==1) không chạy → action giữ null → lần đổi value kế tiếp vẫn thỏa điều kiện trigger. |
| TC-REGSHARED001-02 | REG-SHARED-001 | Normal | App v1 - Cập nhật điểm (point) đạt ngưỡng vẫn kích hoạt action (đối chứng shared block sendAction) | Trường friend info kiểu điểm (type_data=6/point) có setting_actions cấu hình ngưỡng gắn action. Friend có điểm dưới ngưỡng, action=null. | 1. Gọi POST /api/mobile/save-custom-info cập nhật điểm đạt/vượt ngưỡng có action, payload đúng app (type_data=point).<br>2. Kiểm hành vi action + DB. | newValue = giá trị điểm ≥ ngưỡng cấu hình action. | Response 'ok'. Action kích hoạt đúng (block sendAction dùng chung cho point/select vẫn chạy). Giá trị điểm lưu đúng. Xác nhận fix select KHÔNG làm hỏng nhánh point. | Chưa test |  | LOCAL | hanhntb | 2026-08-26 |  |  | Studio #13586 (NEW-6) · tc_group=api · exec_mode=auto · env_tag=local-only · env_scope=all · tác giả=AI (provenance.source=ai, job=687) · requirement_keys=REQ-007 · spec_ids=TICKET-40201, spec: feature-spec.md dòng 235,401 (BR-02/point), source: FriendInformationController.php:380-399 · ⚠️ raw last_exec.status=**blocked** (không phải pass/fail — TC chưa thực sự được verify) · ⚠️ chạy ở env **local** — RULE-08 · note Studio: Point đi qua cùng block sendAction (dòng 380) nhưng KHÔNG chạy vòng lặp select nên vốn không bị bug — dùng làm đối chứng shared/negative control cho phần không đổi. |
| TC-TOOLNEGCTRL001-01 | TOOL-NEGCTRL-001 | Abnormal | App v1 - Option select KHÔNG cấu hình action → lưu giá trị, không kích hoạt, không lỗi 500 (đối chứng âm) | Trường select có option KHÔNG gắn action_id (action_id rỗng). Friend có bản ghi giá trị. | 1. Gọi POST /api/mobile/save-custom-info đổi value sang option không có action, payload đúng app.<br>2. Kiểm DB + response. | newValue = giá trị option không cấu hình action_id. | Response 'ok', không 500. friend_information_value.value + friend_info_option_id cập nhật đúng. KHÔNG kích hoạt action nào (không đổi trạng thái đối ứng, không tạo đăng ký step). friend_information_value.action giữ nguyên. | Chưa test |  | LOCAL | hanhntb | 2026-08-26 |  |  | Studio #13584 (NEW-4) · tc_group=api · exec_mode=auto · env_tag=local-only · env_scope=all · tác giả=AI (provenance.source=ai, job=687) · requirement_keys=REQ-005 · spec_ids=TICKET-40201, source: FriendInformationController.php:383-385 · ⚠️ raw last_exec.status=**blocked** (không phải pass/fail — TC chưa thực sự được verify) · ⚠️ chạy ở env **local** — RULE-08 · note Studio: Đối chứng âm: mutate value hợp lệ nhưng option không có action → không được trigger. Lưu ý ranh giới SRC-BUSINESS-005: nếu setting_value không parse được ($settingValue null) đây là edge chưa guard, NGOÀI phạm vi fix #40201 — chỉ quan sát, không assert pass/fail cho bug này. |
| TC-TOOLNEGCTRL001-02 | TOOL-NEGCTRL-001 | Abnormal | App v1 - Gửi lại đúng giá trị cũ (value không đổi) → không kích hoạt lại action (đối chứng âm) | Friend đã có giá trị = option A (có action). Trường select action_mode=2 để loại yếu tố action=1 chặn. | 1. Gọi POST /api/mobile/save-custom-info với newValue = ĐÚNG giá trị hiện tại (option A) — không đổi value.<br>2. Kiểm hành vi action + response. | newValue = giá trị hiện tại của friend (không thay đổi). | Response 'ok'. Không kích hoạt action mới (sendAction chỉ đặt khi giá trị đổi — sendAction=false khi value không đổi), không tạo thêm đăng ký step. Giá trị DB giữ nguyên. | Chưa test |  | LOCAL | hanhntb | 2026-08-26 |  |  | Studio #13585 (NEW-5) · tc_group=api · exec_mode=auto · env_tag=local-only · env_scope=all · tác giả=AI (provenance.source=ai, job=687) · requirement_keys=REQ-005 · spec_ids=TICKET-40201, source: FriendInformationController.php:265-266,385 · ⚠️ raw last_exec.status=**blocked** (không phải pass/fail — TC chưa thực sự được verify) · ⚠️ chạy ở env **local** — RULE-08 · note Studio: Đối chứng âm nhánh 'value không đổi': cờ $sendAction chỉ bật khi có thay đổi value (dòng ~265-266). Xác nhận không trigger thừa. |
| TC-STATEDEP001-03 | STATE-DEP-001 | Boundary | App v1 - action_mode=1 (一度のみ) chỉ kích hoạt action đúng một lần | Trường select có option gắn action, cấu hình 稼働設定 = action_mode=1 (一度のみ). Friend chưa từng chạy action cho trường này (friend_information_value.action = null). | 1. Lần 1: gọi POST /api/mobile/save-custom-info đổi value sang option A (có action), payload đúng app.<br>2. Kiểm DB + hành vi action sau lần 1.<br>3. Lần 2: gọi lại POST /api/mobile/save-custom-info đổi value sang option B khác (cũng có action) trên cùng bản ghi.<br>4. Kiểm DB + hành vi action sau lần 2. | Lần 1: newValue = giá trị option A; Lần 2: newValue = giá trị option B (đều thuộc setting có action_mode=1). | Sau lần 1: action kích hoạt, friend_information_value.action được set = 1. Sau lần 2: value/friend_info_option_id cập nhật sang option B nhưng action KHÔNG kích hoạt lại (vì action != null), không tạo thêm bản ghi đăng ký step. Response cả 2 lần = 'ok'. | Chưa test |  | LOCAL | hanhntb | 2026-08-26 |  |  | Studio #13582 (NEW-2) · tc_group=api · exec_mode=auto · env_tag=local-only · env_scope=all · tác giả=AI (provenance.source=ai, job=687) · requirement_keys=REQ-003 · spec_ids=TICKET-40201, spec: feature-spec.md dòng 394 (BR-04), source: FriendInformationController.php:379,385,390-396 · ⚠️ raw last_exec.status=**blocked** (không phải pass/fail — TC chưa thực sự được verify) · ⚠️ chạy ở env **local** — RULE-08 · note Studio: Điều kiện trigger: sendAction chỉ chạy khi $friendValue->action == null (dòng 385); mode=1 set action=1 chặn lần sau. |
| TC-TOOLOLDREC001-01 | TOOL-OLDREC-001 | Boundary | App v1 - Bản ghi select cũ (tạo trước fix, action=null) đổi giá trị sau fix → kích hoạt lần đầu | Có bản ghi friend_information_value kiểu select tạo qua app TRƯỚC khi fix: value đã lưu đúng nhưng action = null (vì action chưa từng chạy). Trường có action_mode=1. Dựng tiền điều kiện bằng cách seed bản ghi có action=null (mô phỏng dữ liệu cũ). | 1. Gọi POST /api/mobile/save-custom-info đổi value sang option (khác value cũ) có gắn action, payload đúng app.<br>2. Kiểm hành vi action + friend_information_value.action. | newValue = giá trị option có action, khác với value cũ của bản ghi. | Action kích hoạt lần đầu (action đang null nên thỏa điều kiện trigger), sau đó action=1 (mode=1). Value/option cập nhật đúng. | Chưa test |  | LOCAL | hanhntb | 2026-08-26 |  |  | Studio #13587 (NEW-7) · tc_group=api · exec_mode=auto · env_tag=local-only · env_scope=all · tác giả=AI (provenance.source=ai, job=687) · requirement_keys=REQ-008 · spec_ids=TICKET-40201, spec: feature-spec.md dòng 394 (BR-04), source: FriendInformationController.php:379-395 · ⚠️ raw last_exec.status=**blocked** (không phải pass/fail — TC chưa thực sự được verify) · ⚠️ chạy ở env **local** — RULE-08 · note Studio: CẦN TESTER XÁC NHẬN: hành vi bản ghi cũ trên DB thật chưa verify (ghi ở plan conflict). Nếu gửi lại ĐÚNG value cũ thì sendAction=false → không trigger; chỉ khi ĐỔI value mới trigger. Không tự chốt expected tuyệt đối nếu quan sát khác — báo lại leader. |
| TC-API001-01 | API-001 | Normal | App v2 - Cập nhật select có action → kích hoạt action và lưu giá trị (verify fix saveCustomInfo2) | Đã có bot + friend + token mobile-auth. Trường friend info kiểu lựa chọn (type_data=1) có option gắn action (đổi trạng thái đối ứng / bắt đầu step配信), action_mode=2. Friend có giá trị khác option đích. | 1. Từ app điện thoại (hoặc mô phỏng request app Flutter phát ra), gọi POST /api/mobile/save-custom-info-v2 với header mobile-auth hợp lệ.<br>2. Body info = { id, id_value, newValue: <giá trị option có action>, type_data: 1, setting_value: <JSON string đúng app> } — không tự thêm field FE không phát ra.<br>3. Nhận response và kiểm DB + hành vi action. | info.newValue = giá trị option có action_id; info.setting_value = JSON string cấu hình select (nguyên văn app gửi). | Response 'ok' (không 500). friend_information_value.value + friend_info_option_id lưu đúng. Action kích hoạt: trạng thái đối ứng đổi + tạo bản ghi đăng ký step配信. Không còn exception 'non-object' ở nhánh action. | Chưa test |  | LOCAL | hanhntb | 2026-08-26 |  |  | Studio #13588 (NEW-8) · tc_group=api · exec_mode=auto · env_tag=local-only · env_scope=all · tác giả=AI (provenance.source=ai, job=687) · requirement_keys=REQ-002 · spec_ids=TICKET-40201, EP: POST /api/mobile/save-custom-info-v2, source: FriendInformationController.php:666,724,830-853 · ⚠️ raw last_exec.status=**blocked** (không phải pass/fail — TC chưa thực sự được verify) · ⚠️ chạy ở env **local** — RULE-08 · note Studio: v2 (saveCustomInfo2) chứa cùng bug/fix như v1 (đổi tên biến vòng lặp $settingValue→$settingActionOption tại 3 vị trí, dòng 724/742/796). API-001: viết TC riêng cho endpoint v2, không gộp với v1. |
| TC-REGSHARED001-03 | REG-SHARED-001 | Normal | App v2 - Point đạt ngưỡng vẫn kích hoạt action | Friend info kiểu point có action khi đạt ngưỡng. | 1. Gọi API v2 cập nhật point từ dưới ngưỡng lên giá trị đạt ngưỡng.<br>2. Kiểm tra giá trị lưu và action. | Point value đạt hoặc vượt threshold cấu hình. | Point được lưu đúng và action dùng chung được kích hoạt. Fix select không làm ảnh hưởng nhánh point. | Chưa test |  | LOCAL | hanhntb | 2026-08-26 |  |  | Studio #14003 (NEW-14) · client_ref=NEW-14-V2-POINT · tc_group=api · exec_mode=auto · env_tag=local-only · env_scope=all · tác giả=hanhntb@mcp (provenance.source=human) · priority Studio=Medium · requirement_keys=(trống) · spec_ids=TICKET-40201, REQ-007 · ⚠️ raw last_exec.status=**blocked** (không phải pass/fail — TC chưa thực sự được verify) · ⚠️ chạy ở env **local** — RULE-08 · note Studio: Regression control cho endpoint v2. |
| TC-TOOLNEGCTRL001-03 | TOOL-NEGCTRL-001 | Abnormal | App v2 - Option không cấu hình action → lưu giá trị, không kích hoạt, không lỗi 500 (đối chứng âm) | Trường select v2 có option không gắn action_id. Friend có bản ghi giá trị. | 1. Gọi POST /api/mobile/save-custom-info-v2 đổi value sang option KHÔNG có action, payload đúng app.<br>2. Kiểm DB + response. | newValue = giá trị option không cấu hình action. | Response 'ok', không 500. Value + friend_info_option_id lưu đúng. Không kích hoạt action, action giữ nguyên. | Chưa test |  | LOCAL | hanhntb | 2026-08-26 |  |  | Studio #13589 (NEW-9) · tc_group=api · exec_mode=auto · env_tag=local-only · env_scope=all · tác giả=AI (provenance.source=ai, job=687) · version=2 · requirement_keys=REQ-005 · spec_ids=TICKET-40201, source: FriendInformationController.php:830-839 · ⚠️ raw last_exec.status=**blocked** (không phải pass/fail — TC chưa thực sự được verify) · ⚠️ chạy ở env **local** — RULE-08 · note Studio: Đã tách trường hợp value không đổi thành testcase NEW-13 riêng để tránh gộp 2 mục tiêu khác nhau trong cùng testcase. |
| TC-TOOLNEGCTRL001-04 | TOOL-NEGCTRL-001 | Abnormal | App v2 - Gửi lại đúng giá trị hiện tại không kích hoạt action mới | Friend đang có option A. Option A có action. Cấu hình action_mode=2. | 1. Gọi API v2 cập nhật lại đúng option A đang có.<br>2. Kiểm tra response và kết quả action. | newValue = giá trị hiện tại của friend. | Lưu thành công nhưng không chạy action mới, không tạo thêm đăng ký step配信, không đổi trạng thái đối ứng. | Chưa test |  | LOCAL | hanhntb | 2026-08-26 |  |  | Studio #14002 (NEW-13) · client_ref=NEW-13-V2-SAME-VALUE · tc_group=api · exec_mode=auto · env_tag=local-only · env_scope=all · tác giả=hanhntb@mcp (provenance.source=human) · priority Studio=Medium · requirement_keys=(trống) · spec_ids=TICKET-40201, REQ-005 · ⚠️ raw last_exec.status=**blocked** (không phải pass/fail — TC chưa thực sự được verify) · ⚠️ chạy ở env **local** — RULE-08 · note Studio: Bổ sung nhánh value không đổi còn thiếu trong NEW-9. |
| TC-STATEDEP001-04 | STATE-DEP-001 | Boundary | App v2 - action_mode=1 chỉ kích hoạt action một lần | Trường select có option gắn action và action_mode=1. Friend chưa từng chạy action. | 1. Gọi API v2 cập nhật value sang option A có action.<br>2. Kiểm tra status, step subscription và action state.<br>3. Gọi API v2 lần 2 cập nhật sang option B có action.<br>4. Kiểm tra action lần 2. | Option A/B đều có action, action_mode=1. | Lần đầu action chạy và trạng thái action được đánh dấu đã chạy. Lần sau value cập nhật nhưng action không chạy lại. | Chưa test |  | LOCAL | hanhntb | 2026-08-26 |  |  | Studio #14001 (NEW-12) · client_ref=NEW-12-V2-MODE1 · tc_group=api · exec_mode=auto · env_tag=local-only · env_scope=all · tác giả=hanhntb@mcp (provenance.source=human) · priority Studio=High · requirement_keys=(trống) · spec_ids=TICKET-40201, REQ-002, REQ-003, API-001 · ⚠️ raw last_exec.status=**blocked** (không phải pass/fail — TC chưa thực sự được verify) · ⚠️ chạy ở env **local** — RULE-08 · note Studio: Bổ sung nhánh v2 tương ứng với fix saveCustomInfo2. |

---

## Đối chiếu mã quan điểm Studio ↔ `framework/checklist-lme.md`

| Mã quan điểm (Studio) | Có trong checklist-lme.md? | Số TC | TC No. |
|---|---|---|---|
| `REG-SHARED-001` | ✅ có | 3 | TC-REGSHARED001-01, TC-REGSHARED001-02, TC-REGSHARED001-03 |
| `SYNC-APP-001` | ✅ có | 1 | TC-SYNCAPP001-01 |
| `TOOL-KNOW-002` | ❌ **KHÔNG có** | 2 | TC-TOOLKNOW002-01, TC-TOOLKNOW002-02 |
| `OUT-TRUTH-001` | ✅ có | 1 | TC-OUTTRUTH001-01 |
| `STATE-DEP-001` | ✅ có | 4 | TC-STATEDEP001-01, TC-STATEDEP001-02, TC-STATEDEP001-03, TC-STATEDEP001-04 |
| `TOOL-NEGCTRL-001` | ❌ **KHÔNG có** | 4 | TC-TOOLNEGCTRL001-01, TC-TOOLNEGCTRL001-02, TC-TOOLNEGCTRL001-03, TC-TOOLNEGCTRL001-04 |
| `TOOL-OLDREC-001` | ❌ **KHÔNG có** | 1 | TC-TOOLOLDREC001-01 |
| `API-001` | ❌ **KHÔNG có** | 1 | TC-API001-01 |

> ❌ **4 mã không tồn tại trong tri thức chuẩn của repo**: `TOOL-KNOW-002`, `TOOL-NEGCTRL-001`, `TOOL-OLDREC-001`, `API-001`.
> Đây là mã do Studio/AI tự đặt (tiền tố `TOOL-*` = quy ước nội bộ của tool, `API-001` không có nhóm `API-*` trong checklist).
> ⇒ Khi chạy `/review-tc`: **8/17 TC không map được coverage** sang 80 quan điểm LME. Leader cần quyết định map tay sang mã chuẩn (gợi ý: `FUNC-*` / `DATA-*` / `REG-*` / `INTG-*`) hoặc bổ sung mã vào checklist.

## Trạng thái thực thi

**Tổng hợp**: `blocked=12 · pass=5` — tổng 17 TC · 0 bug ticket được raise.

### 5 TC đã pass (manual, env=local, **không có evidence**)

| TC No. | temp_id | Tiêu đề | Người chạy | Thời điểm |
|---|---|---|---|---|
| TC-REGSHARED001-01 | NEW-10 | PC - Cập nhật select có action từ màn quản lý vẫn kích hoạt action (regression sau fix) | hanhntb | 2026-08-26 07:32 |
| TC-SYNCAPP001-01 | NEW-11 | App smartphone - Cập nhật 顧客対応状況 có action kích hoạt đầy đủ như PC | hanhntb | 2026-08-26 08:07 |
| TC-TOOLKNOW002-01 | NEW-15 | Manual App - Reproduce bug cập nhật friend info không kích hoạt action sau khi đổi option | hanhntb | 2026-08-26 08:09 |
| TC-OUTTRUTH001-01 | NEW-16 | Manual App - Kiểm tra action đổi trạng thái đối ứng sau khi cập nhật friend info | hanhntb | 2026-08-26 08:10 |
| TC-STATEDEP001-01 | NEW-17 | Manual App - Kiểm tra bắt đầu step配信 sau khi cập nhật friend info | hanhntb | 2026-08-26 08:07 |

### 12 TC `blocked` — CHƯA ĐƯỢC VERIFY

| TC No. | temp_id | Tiêu đề | Thời điểm đánh dấu |
|---|---|---|---|
| TC-TOOLKNOW002-02 | NEW-1 | App v1 - Cập nhật select có action → kích hoạt action và lưu giá trị (tái hiện + verify fix) | 2026-08-26 07:36 |
| TC-STATEDEP001-02 | NEW-3 | App v1 - action_mode=2 (何度でも稼働) kích hoạt action mỗi lần đổi giá trị | 2026-08-26 07:36 |
| TC-REGSHARED001-02 | NEW-6 | App v1 - Cập nhật điểm (point) đạt ngưỡng vẫn kích hoạt action (đối chứng shared block sendAction) | 2026-08-26 07:36 |
| TC-TOOLNEGCTRL001-01 | NEW-4 | App v1 - Option select KHÔNG cấu hình action → lưu giá trị, không kích hoạt, không lỗi 500 (đối chứng âm) | 2026-08-26 07:36 |
| TC-TOOLNEGCTRL001-02 | NEW-5 | App v1 - Gửi lại đúng giá trị cũ (value không đổi) → không kích hoạt lại action (đối chứng âm) | 2026-08-26 07:36 |
| TC-STATEDEP001-03 | NEW-2 | App v1 - action_mode=1 (一度のみ) chỉ kích hoạt action đúng một lần | 2026-08-26 07:36 |
| TC-TOOLOLDREC001-01 | NEW-7 | App v1 - Bản ghi select cũ (tạo trước fix, action=null) đổi giá trị sau fix → kích hoạt lần đầu | 2026-08-26 07:36 |
| TC-API001-01 | NEW-8 | App v2 - Cập nhật select có action → kích hoạt action và lưu giá trị (verify fix saveCustomInfo2) | 2026-08-26 07:36 |
| TC-REGSHARED001-03 | NEW-14 | App v2 - Point đạt ngưỡng vẫn kích hoạt action | 2026-08-26 08:07 |
| TC-TOOLNEGCTRL001-03 | NEW-9 | App v2 - Option không cấu hình action → lưu giá trị, không kích hoạt, không lỗi 500 (đối chứng âm) | 2026-08-26 07:36 |
| TC-TOOLNEGCTRL001-04 | NEW-13 | App v2 - Gửi lại đúng giá trị hiện tại không kích hoạt action mới | 2026-08-26 08:07 |
| TC-STATEDEP001-04 | NEW-12 | App v2 - action_mode=1 chỉ kích hoạt action một lần | 2026-08-26 08:07 |

> ⚠️ Toàn bộ 12 TC blocked là **TC kiểm trực tiếp 2 endpoint đã sửa code** (`save-custom-info` v1 + `save-custom-info-v2` v2) và các nhánh `action_mode=1/2`, đối chứng âm, bản ghi cũ, point. **Nói cách khác: phần lõi của fix chưa được kiểm chứng.** 5 TC pass chỉ phủ góc nhìn UI app + regression PC.

## Phân bố

| Chiều | Phân bố |
|---|---|
| `case_type` | Normal=10 · Abnormal=4 · Boundary=3 |
| `tc_group` | api=12 · ui=5 |
| `exec_mode` | auto=13 · manual=4 |
| `provenance.source` | ai=10 · human=7 |
| `env` đã chạy | local=17 |
| `last_exec.status` | blocked=12 · pass=5 |

### Màn hình / endpoint

- `API mobile lưu friend info v1 (POST /api/mobile/save-custom-info)` — 7 TC
- `API mobile lưu friend info v2 (POST /api/mobile/save-custom-info-v2)` — 5 TC
- `App smartphone - Quản lý thông tin friend` — 4 TC
- `PC - Cập nhật friend info kiểu select (My page / Chat 1:1 right bar)` — 1 TC

### Requirements Studio (`task_get_context`) — 8 REQ

| REQ | Tiêu đề | Category | Risk | TC liên kết (qua `requirement_keys`) |
|---|---|---|---|---|
| REQ-001 | App v1: cập nhật select có action kích hoạt action + lưu value | api | **High** | TC-TOOLKNOW002-02 |
| REQ-002 | App v2: cùng hành vi qua `save-custom-info-v2` | api | **High** | TC-API001-01 |
| REQ-003 | `action_mode=1` chỉ kích hoạt một lần | api | Medium | TC-STATEDEP001-03 |
| REQ-004 | `action_mode=2` kích hoạt mỗi lần đổi value | api | Medium | TC-STATEDEP001-02 |
| REQ-005 | Option không có action / value không đổi → không lỗi, không kích hoạt | api | Medium | TC-TOOLNEGCTRL001-01, -02, -03 |
| REQ-006 | Regression đường PC không đổi hành vi sau fix | ui | Medium | TC-REGSHARED001-01 |
| REQ-007 | Point (shared block) vẫn kích hoạt action | api | Low | TC-REGSHARED001-02 |
| REQ-008 | Bản ghi cũ tạo trước fix được kích hoạt đúng | api | Medium | TC-TOOLOLDREC001-01 |

> ⚠️ 7/17 TC có `requirement_keys` **rỗng** (toàn bộ TC do `hanhntb@mcp` tạo) — chỉ gắn REQ qua `spec_ids` dạng chuỗi nên coverage engine của Studio không liên kết được đầy đủ.
> ⚠️ Báo cáo coverage Studio: **0/28 covered, 26 partial, 2 none** — 2 mục `none` là **BR-03** (cấu trúc JSON `setting_value` — format dữ liệu app gửi) và **BR-04** (`action mode và trigger` — *"ảnh hưởng trực tiếp bởi fix"*). BR-04 có 3 TC trỏ tới qua chuỗi `spec: feature-spec.md dòng 394 (BR-04)` nhưng engine không nối được → Leader tự xác nhận.

---

## Member tự check trước khi submit

> ⚠️ Bộ TC này **fetch từ Studio**, không qua quy trình `/write-tc` của repo nên **chưa có bảng duyệt quan điểm 2 tầng**. `/review-tc` sẽ dựng bảng coverage này.

### Coverage check
- [ ] Đã đọc kỹ `01-bug-task.md`
- [ ] Đã đọc kỹ `02-spec-reference.md` (**chưa có** — cần tạo từ `spec-features/admin/friend-information/feature-spec.md`)
- [ ] Đã đọc kỹ `03-dev-impact.md`, hiểu 4 mục
- [ ] **Mỗi impact** trong 4.1 / 4.2 / 4.3 có **ít nhất 1 TC** verify
- [ ] Có **ít nhất 1 TC** verify trực tiếp bug fix (reproduce flow KH)
- [ ] Có **ít nhất 1 TC** verify tính năng cũ không hỏng cho mỗi tính năng trong 4.3 (ghi "regression" ở Ghi chú)
- [ ] Có **ít nhất 1 Abnormal + 1 Boundary** cho mỗi data quan trọng trong 4.2
- [ ] Mọi TC có `Mã quan điểm liên kết`, steps rõ ràng, `Kết quả mong đợi` đo lường được
- [ ] `Tiêu đề test case` chứa **keyword** giúp Leader nhận ra impact TC đó cover

### Base quan điểm test LME (2 tầng)

**Tầng 1 — quan điểm**: [framework/checklist-lme.md](../../framework/checklist-lme.md) (80 quan điểm + 12 RULE).
**Tầng 2 — catalog**: [framework/catalog-lme.md](../../framework/catalog-lme.md).

| Mã quan điểm | Ưu tiên | ◯/× | Catalog đã tra | TC cover | Lý do nếu × |
|---|---|---|---|---|---|
| `<`/review-tc` sẽ dựng bảng này>` | | | | | |

- [ ] Đã duyệt **toàn bộ** tầng 1 từ trên xuống, không bỏ nhóm nào
- [ ] Mỗi quan điểm ◯ **đã mở đúng catalog** ở tầng 2
- [ ] Mọi quan điểm ◯ ưu tiên **Cao** có đủ 3 loại case Normal + Abnormal + Boundary (**RULE-01**)
- [ ] Mọi × đều có lý do; × ở quan điểm **Cao** đã báo Leader duyệt (**RULE-03**)
- [ ] TC có output ra ngoài (LINE app / mobile app) → `Kết quả mong đợi` đi tới **output cuối trên thiết bị thật** (**RULE-06**)
- [ ] TC CRUD verify đủ **3 tầng** DB + màn hình + output (**RULE-07**)
- [ ] Task chạm **job nền (step配信)** → có TC ghi `Môi trường test = PRODUCTION` (**RULE-08**) — ❌ **hiện 17/17 TC chạy ở local**
- [ ] Task chạm đối tượng đã từng version-up → test **cả nhánh cũ và mới** (**RULE-09**) — ⚠️ v1 + v2 cả 2 đều `blocked`
- [ ] Mỗi TC đã ghi **loại evidence bắt buộc** ở Ghi chú (**RULE-02**) — ❌ 5 TC pass đều `evidence = []`
- [ ] Mọi TC có `Trạng thái đánh giá spec` — ❌ **17/17 TC đều trống** (`spec_status = null` trên Studio)

---

<!-- Source: fetched từ MCP LME TEST STUDIO task_id=226 (ticket 40201) bằng testcase_list(limit=100) — 17 TC, lúc 2026-08-26. Redmine #40201 KHÔNG có Section "Link TCs". KHÔNG sửa TCs này nếu chưa confirm với Leader. -->
