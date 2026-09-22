<!-- sync-tcs: url=<Google Sheet URL của sheet TC human/master> | sheet=<tên tab> | anchor=Main Function -->
<!-- source: MCP LME TEST STUDIO — task_id=193, ticket 38511, testcase_list (8 TC), fetch lúc 2026-09-19. Redmine KHÔNG có Link TCs human. -->

# 04 — TC List (snapshot từ MCP LME TEST STUDIO)

> ⚠️ **Read-only** — chép nguyên văn từ Studio task #193. Muốn sửa TC thì sửa trên Studio (`testcase_update`) rồi fetch lại.
> `TC No.` giữ **ID hiển thị trên tool** (`NEW-xx`) để Leader tra ngược; mã theo quan điểm ghi ở cột `Ghi chú`.

## Thông tin

| Trường | Giá trị |
|---|---|
| Studio task | #193 · type `fix-bug` · feature `affiliate-register` · branch `ai_fixbug_38511` · round 1 |
| Trạng thái task | status `done-ai` · aiResult **`fail`** · reviewState `leader` · openBugs 1 |
| Tác giả TC | **7/8 do AI sinh** (`author=AI`, `created_job_id=577`, NEW-1…NEW-8) · **1/8 do người viết qua MCP** (NEW-9, `vinth@mcp`, provenance `human`) |
| Trạng thái TC | 8/8 `draft` |
| Lần chạy gần nhất | run #1718 · 2026-09-19 05:35 · env **STAGING** · `source=ai` (pipeline AI), by `quyend` |
| Kết quả | **3 pass · 1 fail · 4 skip · 0 chưa chạy** |
| Link TC gốc | Studio task #193 (không có Sheet human) |

### ⚠️ Cảnh báo cho Leader

1. **TC fail chưa raise ticket**: `NEW-4` (mã hashid rác → phải trả HTTP 404, không render form) — `bug_tickets` rỗng, dù task ghi `openBugs = 1`.
2. **4 TC skip — chính là các TC verify fix**: `NEW-1` (owner role 2), `NEW-2` (owner role -1), `NEW-3` (regression role 0/1), `NEW-9` (luồng đầy đủ từ ASP管理). → Fix **chưa được verify** trên staging; chỉ các TC đối chứng âm/phụ (NEW-5, NEW-7, NEW-8) pass.
3. **Môi trường**: run gần nhất ở staging; `envAuto` còn 1 run ở local. dev / prd chưa chạy. Bug không thuộc nhóm RULE-08 (media / domain / job / bill) nên không bắt buộc production.
4. `NEW-6` **không còn** trong danh sách (đánh số nhảy NEW-5 → NEW-7) — có thể đã bị xóa trên Studio.
5. `NEW-9` khai `exec_mode = manual` nhưng `last_exec.source = ai` (skip).

### Mã quan điểm Studio không map được vào `framework/checklist-lme.md`

| Mã Studio | TC | Tình trạng |
|---|---|---|
| `TOOL-KNOW-002` | NEW-1, NEW-9 | Không có trong checklist (mã nội bộ của Studio) |
| `TOOL-NEGCTRL-001` | NEW-4, NEW-5 | Không có trong checklist (mã nội bộ của Studio) |
| `RULE-09` | NEW-2 | Là **RULE** (Cũ & mới song song), không phải mã quan điểm |
| `RULE-07` | NEW-8 | Là **RULE** (Verify 3 tầng), không phải mã quan điểm |

→ 4/6 mã không phải quan điểm hợp lệ — `/review-tc` sẽ không map được coverage theo quan điểm cho 6/8 TC. Mã hợp lệ: `COMPAT-LEGACY-001` (NEW-3), `OUT-TRUTH-001` (NEW-7).

### Phân bố

| Chiều | Phân bố |
|---|---|
| `case_type` | Normal 5 (NEW-1, 2, 3, 8, 9) · Abnormal 3 (NEW-4, 5, 7) · **Boundary 0** |
| `tc_group` | ui 8 |
| `exec_mode` | auto 7 · manual 1 (NEW-9) |
| `env_tag` | read-only 7 · local-only 1 (NEW-8) |
| `screen` | Màn đăng ký affiliater 7 · ASP Management → link → màn đăng ký 1 (NEW-9) |
| `requirement_keys` | REQ-001: NEW-1, 2, 3, 9 · REQ-002: NEW-4, 5 · REQ-003: NEW-7, 9 · REQ-004: NEW-8 |

### Requirements trên Studio

| Key | Tiêu đề | Risk |
|---|---|---|
| REQ-001 | Màn đăng ký affiliater mở được cho chủ bot mọi role (-1, 0, 1, 2) | High |
| REQ-002 | Guard 404 giữ nguyên với mã / user không hợp lệ | Medium |
| REQ-003 | Trạng thái nhận thành viên hiển thị đúng (bật → form; tắt/chưa có setting → thông báo tạm dừng) | Medium |
| REQ-004 | Regression luồng tạo affiliater (POST /ajax/create_new_aff) không bị fix ảnh hưởng | Low |

`test_viewpoint_selection` = null. Review: state `leader`, round 1.

---

## TC List

| TC No. | Mã quan điểm liên kết | Loại case | Tiêu đề test case | Điều kiện tiền đề | Các bước thực hiện | Dữ liệu test/input | Kết quả mong đợi | Kết quả thực thi | Evidence thực tế | Môi trường test | Người thực hiện | Ngày thực hiện | Số ticket bug | Trạng thái đánh giá spec | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| NEW-1 | TOOL-KNOW-002 | Normal | Chủ bot role 2 (staff) mở được màn đăng ký affiliater (tái hiện & verify fix #38511) | Có một chủ bot (bản ghi users) role = 2 (staff), user_setting_aff của user này có is_register_new_affiliate = 1. Lấy admin_id = hashid encode của user.id để dựng URL /affiliate/{admin_id}/regist. | 1. Mở trình duyệt, truy cập URL /affiliate/{admin_id}/regist với admin_id là mã hashid của chủ bot role 2<br>2. Quan sát trang trả về (tiêu đề 「ASP管理 紹介者（登録）」 và tiêu đề khối 「アフィリエイター登録」) | admin_id = hashid(user.id) của chủ bot role = 2 | Màn đăng ký affiliater hiển thị, không redirect 404. Hiển thị tiêu đề 「アフィリエイター登録」, ba ô 「お名前」「メールアドレス」「パスワード」 và nút 「アカウント登録」 do is_register_new_affiliate = 1. Không hiển thị thông báo tạm dừng. Trước fix cùng thao tác này trả 404. | Chưa test |  | STAGING | quyend (AI pipeline) | 2026-09-19 |  |  | Studio #12450 (NEW-1) · raw status `skip` · ui / auto / read-only · env_scope all · REQ-001 · TICKET-38511, EP-regist, commit:c31b07792a · v2 · Note: Đây là case tái hiện + verify fix bug (TOOL-KNOW-002). GET read-only, không ghi DB. Kỹ thuật: đường 404 cũ do validator exists_admin yêu cầu role IN (0,1); fix đã bỏ điều kiện role tại AffiliateController@regist:33-35. |
| NEW-2 | RULE-09 | Normal | Chủ bot role -1 (admin nội bộ) mở được màn đăng ký affiliater | Có một chủ bot (users) role = -1, user_setting_aff có is_register_new_affiliate = 1. admin_id = hashid(user.id). | 1. Mở trình duyệt truy cập /affiliate/{admin_id}/regist với admin_id của chủ bot role -1<br>2. Quan sát trang trả về | admin_id = hashid(user.id) của chủ bot role = -1 | Màn đăng ký affiliater hiển thị (không 404), thấy tiêu đề 「アフィリエイター登録」 và form nhập. Trước fix trả 404. | Chưa test |  | STAGING | quyend (AI pipeline) | 2026-09-19 |  |  | Studio #12451 (NEW-2) · raw status `skip` · ui / auto / read-only · env_scope all · REQ-001 · TICKET-38511, EP-regist, commit:c31b07792a · ⚠️ mã RULE-09 không phải quan điểm · Note: Case fix-target thứ hai (role âm). GET read-only. |
| NEW-3 | COMPAT-LEGACY-001 | Normal | Chủ bot role 0/1 (nhánh cũ) vẫn mở được màn đăng ký affiliater — regression | Có chủ bot role = 0 (user free) và một chủ bot role = 1 (user paid), mỗi user có user_setting_aff.is_register_new_affiliate = 1. admin_id = hashid(user.id) tương ứng. | 1. Mở trình duyệt truy cập /affiliate/{admin_id}/regist với admin_id của chủ bot role 0<br>2. Quan sát trang trả về<br>3. Lặp lại với admin_id của chủ bot role 1 | Biến thể: admin_id = hashid(user role 0); admin_id = hashid(user role 1) | Cả hai role 0 và 1 đều mở được màn đăng ký (thấy 「アフィリエイター登録」 + form), giữ nguyên hành vi như trước fix (không bị fix phá). | Chưa test |  | STAGING | quyend (AI pipeline) | 2026-09-19 |  |  | Studio #12452 (NEW-3) · raw status `skip` · ui / auto / read-only · env_scope all · REQ-001 · TICKET-38511, EP-regist, SRC-REGRESSION-006 · regression · Note: Backward compatibility (COMPAT-LEGACY-001 / RULE-09): xác nhận nhánh legacy không bị regression. Gộp 2 role vào 1 TC qua data_input vì cùng root. |
| NEW-8 | RULE-07 | Normal | Regression: submit form đăng ký hợp lệ vẫn tạo affiliater thành công | Chủ bot tồn tại, user_setting_aff.is_register_new_affiliate = 1, màn đăng ký mở được. Chuẩn bị email chưa tồn tại trong affiliaters của chủ bot này (định danh riêng để không phụ thuộc data run khác). | 1. Mở trình duyệt truy cập /affiliate/{admin_id}/regist của chủ bot đang bật nhận thành viên<br>2. Nhập 「お名前」, 「メールアドレス」 (email mới, duy nhất) và 「パスワード」 (6-30 ký tự) hợp lệ<br>3. Bấm nút 「アカウント登録」 (gọi JS submitRegister trên browser)<br>4. Quan sát phản hồi trên màn và kiểm bản ghi trong bảng affiliaters | username='Tester QA'; email='qa+38511-<unique>@example.com'; password='abc123456' | Request POST /ajax/create_new_aff trả thành công (HTTP 200/status true); tạo đúng 1 bản ghi affiliaters với admin_id bằng id của chủ bot và email đã nhập; giao diện hiển thị kết quả đăng ký thành công. Không tạo trùng bản ghi. Không bắt buộc kiểm auto-login vì hành vi này không nằm trong phạm vi ảnh hưởng của bản sửa. | Đạt |  | STAGING | quyend (AI pipeline) | 2026-09-19 |  |  | Studio #12457 (NEW-8) · raw status `pass` · ui / auto / local-only · env_scope all · REQ-004 · TICKET-38511, EP-createNewAff, SRC-REGRESSION-008 · v2 · regression · ⚠️ mã RULE-07 không phải quan điểm · Note: Regression nhẹ cho createNewAff. Testcase có ghi DB nên chỉ chạy local/dev/staging, không chạy production. Phải bấm nút thật trên browser để đi qua JS submitRegister; không tự dựng payload gọi thẳng endpoint. |
| NEW-4 | TOOL-NEGCTRL-001 | Abnormal | Mã hashid không hợp lệ (giải mã rỗng) không vào được màn đăng ký | Không cần dữ liệu đặc biệt. | 1. Mở trình duyệt truy cập /affiliate/{admin_id}/regist với admin_id là chuỗi rác không decode được thành id (vd 'khong-hop-le', chuỗi ngẫu nhiên)<br>2. Quan sát trang trả về | admin_id = 'khongHopLe123' (Hashids::decode ra mảng rỗng) | HTTP response/status là 404 và KHÔNG render form đăng ký affiliater. Nếu trả HTTP 200, trang trắng hoặc lỗi 500 thì Fail và ghi nhận bug. | Không đạt |  | STAGING | quyend (AI pipeline) | 2026-09-19 | ⚠️ chưa raise |  | Studio #12453 (NEW-4) · raw status `fail` · ui / auto / read-only · env_scope all · REQ-002 · TICKET-38511, EP-regist, SRC-REGRESSION-007 · v2 · Note: Đối chứng âm cho guard hashid. Oracle phải xác định được HTTP status; không chấp nhận trang trắng là Pass vì REQ-002 yêu cầu mã không hợp lệ bị chặn bằng 404. |
| NEW-5 | TOOL-NEGCTRL-001 | Abnormal | Mã hashid hợp lệ nhưng user không tồn tại trong DB trả 404 | Xác định một id KHÔNG tồn tại trong bảng users (vd id rất lớn chưa dùng), lấy admin_id = hashid(id) đó. | 1. Mở trình duyệt truy cập /affiliate/{admin_id}/regist với admin_id = hashid của một id không có trong bảng users<br>2. Quan sát trang trả về | admin_id = hashid(id không tồn tại, vd 99999999) | Validator exists_admin thất bại (count == 0) -> redirect màn 404. Không hiển thị form đăng ký. | Đạt |  | STAGING | quyend (AI pipeline) | 2026-09-19 |  |  | Studio #12454 (NEW-5) · raw status `pass` · ui / auto / read-only · env_scope all · REQ-002 · TICKET-38511, EP-regist, SRC-REGRESSION-010 · Note: Guard user tồn tại vẫn được giữ sau fix (chỉ bỏ điều kiện role). Đối chứng âm cho REQ-001. |
| NEW-7 | OUT-TRUTH-001 | Abnormal | Chủ bot đang tạm dừng nhận thành viên hiển thị thông báo dừng, không có form | Chủ bot tồn tại (role bất kỳ), user_setting_aff.is_register_new_affiliate = 0 (hoặc không có bản ghi user_setting_aff). admin_id = hashid(user.id). | 1. Mở trình duyệt truy cập /affiliate/{admin_id}/regist của chủ bot đang tắt nhận thành viên (hoặc chưa có user_setting_aff)<br>2. Quan sát nội dung khối form | Biến thể: is_register_new_affiliate = 0; và trường hợp user_setting_aff = null | Màn vẫn mở (không 404) nhưng hiển thị thông báo 「現在、新規アフィリエイターの登録を停止しています。」; KHÔNG có 3 ô nhập và không có nút đăng ký. | Đạt |  | STAGING | quyend (AI pipeline) | 2026-09-19 |  |  | Studio #12456 (NEW-7) · raw status `pass` · ui / auto / read-only · env_scope all · REQ-003 · TICKET-38511, EP-regist, source:member_add.blade.php · Note: Nhánh @else của member_add.blade.php:168. userSettingAff null cũng rơi vào nhánh này. Trạng thái tạm dừng phải đúng sau khi guard được nới (OUT-TRUTH-001). |
| NEW-9 | TOOL-KNOW-002 | Normal | Chọn owner role 2 tại ASP Management, copy link và mở màn đăng ký thành công | Đăng nhập tài khoản quản trị có quyền mở ASP Management. Trong danh sách owner có một user tồn tại với role = 2; user này có user_setting_aff.is_register_new_affiliate = 1. | 1. Mở màn ASP Management.<br>2. Chọn user owner có role = 2.<br>3. Copy URL hướng dẫn affiliater được tạo cho owner vừa chọn.<br>4. Mở URL login vừa copy trong trình duyệt.<br>5. Tại màn login affiliater, bấm liên kết mở màn đăng ký.<br>6. Kiểm tra URL và nội dung màn đăng ký. | Owner role = 2, is_register_new_affiliate = 1. | URL login và URL đăng ký dùng đúng hashid của owner role 2 vừa chọn, không lấy owner đã chọn trước đó. Màn 「ASP管理 紹介者（登録）」 mở thành công, không trả 404; hiển thị tiêu đề 「アフィリエイター登録」, ba ô nhập và nút 「アカウント登録」. | Chưa test |  | STAGING | quyend (AI pipeline) | 2026-09-19 |  |  | Studio #18913 (NEW-9) · raw status `skip` · ui / **manual** / read-only · env_scope all · priority High · REQ-001, REQ-003 · TICKET-38511, EP-regist, commit:c31b07792a, source:AffiliateManagementController::index · tác giả người (vinth@mcp) · client_ref review193-asp-management-owner-role2-link-20260919 · Note: Đi đúng chuỗi tái hiện trong ticket: chọn owner ở ASP Management → copy link login → mở link → chuyển sang màn đăng ký. Case này kiểm luôn điểm tích hợp AffiliateManagementController::index mà các case truy cập URL trực tiếp chưa bao phủ. |
