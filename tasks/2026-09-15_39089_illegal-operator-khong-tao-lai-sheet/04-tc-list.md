<!-- sync-tcs: url=<chưa có — Redmine #39089 KHÔNG có Link TCs human> | sheet=<chưa có> | anchor=Main Function -->
<!-- source: MCP LME TEST STUDIO — task_id=183, ticket 39089, testcase_list (15 TC), fetch lúc 2026-09-15. Redmine KHÔNG có Link TCs human. -->

# 04 — TC List (fetch từ MCP LME TEST STUDIO — **TC do AI sinh**)

## ⚠️ Cảnh báo bắt buộc đọc trước khi review

| Mục | Nội dung |
|---|---|
| **Tác giả TCs** | **100% do AI sinh** — `provenance.source = ai`, `author = AI`, `created_job_id = 548`. `toolWritten`: tool 15 / mcp 0 / **human 0** (rate 100%). **KHÔNG có TC nào do member người viết.** |
| **Trạng thái TC** | Cả 15 TC đang ở `status = draft`, `version = 1`, chưa gắn `kho_id`. |
| **Task Studio** | `#183` · type `fix-bug` · status `done-ai` · round 1 · branch `ai_fixbug_39089` · `reviewed = false` · `reviewState = leader` (đang chờ Leader review) · `openBugs = 0`. |
| **Kết quả chạy** | **10 Đạt / 0 Không đạt / 3 skip / 2 chưa chạy** (tổng 15). |
| **Môi trường đã chạy** | ⚠️ **TOÀN BỘ ở `env = local`** (2 run: `runId 437` ngày 2026-08-24 by `pipeline`, `runId 1403` ngày 2026-09-14 by `vinth`). `dev` / `staging` / **`prd` đều 0 run**. |
| **Người chạy** | 10 TC pass do **`pipeline` (AI tự chạy)**, không phải QA người chạy. 3 TC skip do `vinth` đánh dấu. |

### ⚠️ RULE-08 — kết quả pass KHÔNG kết luận được

Toàn bộ 10 TC pass chạy ở **`local` với OAuth Google bị mock** (xem cột `Ghi chú`: *"Auto: mock GoogleSheetService::createAuthClientFromAuthCode"*, *"mock createSheet trả spreadsheetId giả"*). Trong khi đó:

- Bug gốc phát sinh trên **luồng OAuth Google thật** — Dev cũng ghi rõ *"không tái hiện được trên dev (cần OAuth Google thật, DB dev đang tắt)"*.
- Tính năng chạm **job nền** (`form-answer:create-google-sheet`) + **Google API bên ngoài** → thuộc phạm vi RULE-08, không kết luận từ local/staging.
- **2 TC quan trọng nhất lại là 2 TC CHƯA CHẠY**: `TC-TOOLKNOW002-01` (E2E đường người dùng thật — TC verify-fixed lõi) và `TC-REGSHARED001-01` (regression màn Lịch). Cả 2 đều `exec_mode = manual`, `env_scope = staging/prd`.

### TC không đạt / skip / chưa chạy

| TC No. | Studio ID | Trạng thái | Ghi chú |
|---|---|---|---|
| — | — | **Không đạt (fail)** | **Không có TC nào fail.** `openBugs = 0`, không TC nào gắn `bug_tickets`. |
| `TC-INTGSHEET001-01` | #12316 (NEW-2) | **skip** — by `vinth`, 2026-09-14, env local | Job tạo spreadsheet → cập nhật DONE. **Không ghi lý do skip trong Studio.** |
| `TC-JOB002-01` | #12317 (NEW-3) | **skip** — by `vinth`, 2026-09-14, env local | Job retry khi `retry_error < 3`. **Không ghi lý do skip.** |
| `TC-JOB002-02` | #12318 (NEW-4) | **skip** — by `vinth`, 2026-09-14, env local | Job dừng retry khi `retry_error = 3`. **Không ghi lý do skip.** |
| `TC-REGSHARED001-01` | #12315 (NEW-1) | **Chưa chạy** (`last_exec = null`) | Regression màn Lịch Salon + Management — `manual`, cần OAuth thật. |
| `TC-TOOLKNOW002-01` | #12330 (NEW-5) | **Chưa chạy** (`last_exec = null`) | **TC E2E verify-fixed lõi** — `manual`, cần browser + OAuth Google thật. |

> ⚠️ Cả 3 TC `job` (INTG-SHEET-001 + JOB-002) bị skip ⇒ **hệ quả cuối cùng của fix — "form được tạo lại spreadsheet" — chưa được verify bởi bất kỳ TC nào đã chạy.**

### ⚠️ Mã quan điểm Studio KHÔNG có trong `framework/checklist-lme.md`

Đã grep đối chiếu — **5/8 mã (11/15 TC)** không tồn tại trong bộ 80 quan điểm LME ⇒ `/review-tc` **không map được coverage** cho các TC này:

| Mã quan điểm Studio | Số TC | Có trong framework? | Ghi chú |
|---|---|---|---|
| `TOOL-KNOW-002` | 3 | ❌ **Không** | Prefix `TOOL-*` không thuộc bộ mã LME |
| `TOOL-ERRHYG-001` | 3 | ❌ **Không** | — |
| `TOOL-OLDREC-001` | 2 | ❌ **Không** | — |
| `TOOL-NEGCTRL-001` | 1 | ❌ **Không** | — |
| `JOB-002` | 2 | ❌ **Không** | Framework chỉ có `JOB-001` |
| `FUNC-001` | 2 | ✅ Có | — |
| `REG-SHARED-001` | 1 | ✅ Có | — |
| `INTG-SHEET-001` | 1 | ✅ Có | — |

### Phân bố TC

| Chiều | Phân bố |
|---|---|
| `case_type` | Normal 6 · Abnormal 7 · Boundary 2 |
| `tc_group` | api 10 · job 3 · ui 2 |
| `exec_mode` | auto 13 · **manual 2** (đúng 2 TC chưa chạy) |
| `env_tag` | local-only 10 · env-safe 5 |
| `env_scope` | `all` 13 · `staging + prd` 2 |
| `screen` | Form Answer — Liên kết Google Spreadsheet (OAuth callback) 10 · Job `form-answer:create-google-sheet` 3 · Regression màn Lịch 1 · (E2E màn link Google) 1 |
| `requirement_keys` | REQ-001 ×2 · REQ-002 ×2 · REQ-003 ×1 · REQ-004 ×1 · REQ-005 ×3 · REQ-006 ×2 · REQ-007 ×3 · REQ-008 ×1 |

### Requirements của task Studio #183 (để đối chiếu coverage với `03-dev-impact.md`)

| REQ | Category | Risk | Tiêu đề |
|---|---|---|---|
| REQ-001 | api | **High** | Reconnect cùng email khi `datetime_connect` NULL không còn ném Exception và luồng chạy trọn vẹn |
| REQ-002 | data | Medium | `datetime` có giá trị: chỉ reset `result_error_googles` sau mốc (hành vi cũ không đổi) |
| REQ-003 | data | Medium | `datetime` NULL: reset toàn bộ `result_error_googles` (type FORM_ANSWER) của bot |
| REQ-004 | data | **High** | Phạm vi reset giới hạn đúng bot + `type_result`, không đụng bản ghi khác |
| REQ-005 | job | Medium | Job `form-answer:create-google-sheet` tạo spreadsheet và xử lý retry / final-failure |
| REQ-006 | api | Medium | Nhánh email khác / lần đầu tạo `FormAnswerConnectGoogle` cho tất cả form, không reset `result_error` |
| REQ-007 | api | Low | Guard đầu callback: `error` param, thiếu scope, bot không tồn tại xử lý sạch |
| REQ-008 | ui | Low | Regression: reconnect Google Sheet ở màn Lịch không bị ảnh hưởng |

---

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | **AI (Studio job #548)** — không có TC do member người viết |
| Ngày submit | 2026-08-24 (tạo TC) · 2026-09-14 (lần chạy gần nhất) |
| Version TCs | v1 (Studio round 1, `reviewed = false`) |
| Link TC gốc (nếu có) | MCP LME TEST STUDIO — `task_id = 183`, ticket 39089 |

---

## TC List

> **16 cột canonical.** Nội dung chép **nguyên văn** từ Studio — **read-only**, không sửa title / precondition / steps / expected. Muốn sửa thì sửa trên Studio (`testcase_update`) rồi fetch lại.

| TC No. | Mã quan điểm liên kết | Loại case | Tiêu đề test case | Điều kiện tiền đề | Các bước thực hiện | Dữ liệu test/input | Kết quả mong đợi | Kết quả thực thi | Evidence thực tế | Môi trường test | Người thực hiện | Ngày thực hiện | Số ticket bug | Trạng thái đánh giá spec | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-REGSHARED001-01 | REG-SHARED-001 | Normal | Regression: reconnect Google Sheet ở màn Lịch (Salon & Management) vẫn hoạt động | Đăng nhập admin, chọn bot có chức năng Lịch (Salon và/hoặc Management) đã dùng Google Sheet. | 1. Vào màn liên kết Google Sheet của Lịch Salon, thực hiện reconnect OAuth với email đã dùng.<br>2. Lặp lại với Lịch Management.<br>3. Quan sát không có exception và message/redirect. | Reconnect cùng email đã dùng trên từng màn Lịch. | Cả hai màn Lịch reconnect thành công, không xuất hiện lỗi 'Illegal operator and value combination'. (Dev xác nhận 2 controller này không có logic filter datetime tương tự nên không dính bug; đây chỉ là smoke đảm bảo không regress.) | Chưa test | | STAGING / PRD (dự kiến) | | | | | Studio #12315 (NEW-1) · ui / manual / env-safe · REQ-008 · spec_ids: TICKET-39089, redmine journal ■3 · **CHƯA CHẠY** (`last_exec = null`) · Note Studio: "Smoke regression (RULE-12). Cần OAuth Google thật ⇒ manual, chạy staging/prd. Không deep test vì ngoài vùng fix." |
| TC-TOOLKNOW002-01 | TOOL-KNOW-002 | Normal | Reconnect Google Sheet cùng email khi mốc kết nối NULL — không lỗi, tạo lại được liên kết (E2E) | Đăng nhập admin, đã chọn bot có ít nhất 1 form. Bot từng liên kết Google Sheet bằng email E (google_sheet_account_email=E) nhưng datetime_connect_google_sheet đang là NULL (tái hiện trạng thái sau khi đổi kênh bot). Tồn tại sẵn vài bản ghi result_error_googles lỗi của bot. | 1. Mở màn quản lý Form Answer của bot, vào chức năng liên kết Google Spreadsheet (màn link Google).<br>2. Bấm nút liên kết Google, hoàn tất OAuth trên Google bằng ĐÚNG email E đã dùng trước đó và cấp đủ quyền spreadsheets.<br>3. Chờ Google chuyển hướng về màn liên kết của ứng dụng.<br>4. Quan sát màn kết quả và message hiển thị.<br>5. Đối chiếu DB: bảng form_answer_connect_googles và result_error_googles của bot. | Email OAuth = E (trùng email cũ). Bot: datetime_connect_google_sheet=NULL, google_sheet_account_email=E. | Không xuất hiện màn lỗi 500/exception 'Illegal operator and value combination'. Ứng dụng redirect về màn liên kết Google kèm message 「Googleスプレッドシートに連携処理を行っています。」(đang xử lý 3~5 phút). DB: sinh bản ghi form_answer_connect_googles (status WAITING) cho các form chưa có google_sheet_id; toàn bộ result_error_googles type FORM_ANSWER của bot được reset (status=0, retry_time=0). Sau khi job nền chạy, form được tạo google_sheet_id. | Chưa test | | STAGING / PRD (dự kiến) | | | | | Studio #12330 (NEW-5) · ui / manual / env-safe · REQ-001 · spec_ids: TICKET-39089, diff:8a7af0135a, FormAnswerController.php:958-1021 · ⚠️ **TC verify-fixed LÕI nhưng CHƯA CHẠY** · Note Studio: "Đường người dùng thật — BẮT BUỘC qua browser + OAuth Google thật (dev không tái hiện được: cần OAuth thật, DB dev tắt). Đây là TC verify-fixed lõi (cặp với TC tái hiện trên bản release). Kỹ thuật: nhánh else email trùng, biến $datetime_connect_google_sheet_old=NULL." |
| TC-FUNC001-01 | FUNC-001 | Normal | Reconnect bằng email KHÁC — tạo liên kết cho tất cả form, không reset danh sách lỗi | Bot đã liên kết bằng email E1; có sẵn vài form và vài bản ghi result_error_googles. Chuẩn bị OAuth trả về email E2 ≠ E1. | 1. Kích hoạt callback OAuth thành công của màn liên kết Google với email trả về là E2 (khác email cũ).<br>2. Quan sát kết quả redirect.<br>3. Đối chiếu DB bảng form_answer_connect_googles và result_error_googles. | google_sheet_account_email_old=E1; email OAuth mới=E2. | Vào nhánh 'email khác' → sinh bản ghi form_answer_connect_googles cho TẤT CẢ form của bot; KHÔNG chạy đoạn reset result_error_googles (các bản ghi lỗi giữ nguyên status/retry cũ). Redirect về màn liên kết kèm message đang xử lý. | Đạt | | LOCAL | pipeline | 2026-08-24 | | | Studio #12331 (NEW-6) · api / auto / local-only · REQ-006 · runId 437 · ⚠️ **pass ở local với OAuth mock** · Note Studio: "Auto: mock GoogleSheetService::createAuthClientFromAuthCode + Google_Service_Oauth2::userinfo (email=E2), gọi callback GET /basic/redirect-google-sheet?code=...&scope=...&state=<botId>. Regression nhánh Branch A không bị fix chạm." |
| TC-FUNC001-02 | FUNC-001 | Normal | Liên kết lần đầu (chưa từng có email) — tạo liên kết cho tất cả form | Bot chưa từng liên kết Google Sheet (google_sheet_account_email rỗng), có sẵn vài form. | 1. Kích hoạt callback OAuth thành công lần đầu với email bất kỳ.<br>2. Quan sát redirect.<br>3. Đối chiếu DB form_answer_connect_googles. | google_sheet_account_email_old = rỗng/null; email OAuth = E. | Vì email cũ rỗng → nhánh 'email khác/lần đầu' → tạo form_answer_connect_googles cho tất cả form; không chạy nhánh reset result_error_googles. Redirect kèm message đang xử lý. | Đạt | | LOCAL | pipeline | 2026-08-24 | | | Studio #12332 (NEW-7) · api / auto / local-only · REQ-006 · runId 437 · ⚠️ pass ở local với OAuth mock · Note Studio: "Auto: mock OAuth như TC email khác. Điều kiện empty($google_sheet_account_email_old) đưa vào nhánh Branch A." |
| TC-TOOLOLDREC001-01 | TOOL-OLDREC-001 | Normal | Reconnect cùng email khi mốc kết nối CÓ giá trị — chỉ reset lỗi phát sinh sau mốc | Bot đã liên kết bằng email E, datetime_connect_google_sheet = T0 (có giá trị). Có bản ghi result_error_googles type FORM_ANSWER: R_old created_at < T0 và R_new created_at >= T0. Có thể có bản ghi status ban đầu ≠ 0. | 1. Kích hoạt callback OAuth thành công với ĐÚNG email E.<br>2. Đối chiếu DB result_error_googles các bản ghi R_old và R_new. | email OAuth = E (trùng); datetime_connect_google_sheet_old = T0. | Hành vi KHÔNG đổi so với trước fix: chỉ R_new (created_at >= T0) được reset (status=0, retry_time=0, next_time_retry=now); R_old (created_at < T0) GIỮ NGUYÊN. Redirect kèm message đang xử lý; sinh form_answer_connect_googles cho form chưa có google_sheet_id. | Đạt | | LOCAL | pipeline | 2026-08-24 | | | Studio #12333 (NEW-8) · api / auto / local-only · REQ-002 · runId 437 · ⚠️ pass ở local với OAuth mock · Note Studio: "Auto mock OAuth. Đây là nhánh có giá trị của null-guard (!empty($datetime_connect_google_sheet_old) → giữ where created_at>=T0). Verify fix không đổi hành vi nhánh cũ." |
| TC-TOOLKNOW002-02 | TOOL-KNOW-002 | Abnormal | Reconnect cùng email khi mốc kết nối NULL (bản fix) — không exception, reset toàn bộ lỗi của bot | Bot đã liên kết bằng email E, datetime_connect_google_sheet = NULL. Có nhiều bản ghi result_error_googles type FORM_ANSWER của bot với created_at rải rác và status/retry_time khác 0. | 1. Kích hoạt callback OAuth thành công với ĐÚNG email E.<br>2. Quan sát không có exception; kiểm redirect.<br>3. Đối chiếu DB toàn bộ result_error_googles type FORM_ANSWER của bot và bảng form_answer_connect_googles. | email OAuth = E (trùng); datetime_connect_google_sheet_old = NULL. | Không ném InvalidArgumentException 'Illegal operator and value combination'. Do datetime NULL, null-guard bỏ điều kiện created_at ⇒ TẤT CẢ result_error_googles type FORM_ANSWER của bot được reset (status=0, retry_time=0, next_time_retry=now). Sinh form_answer_connect_googles cho form chưa có google_sheet_id. Redirect kèm message đang xử lý. | Đạt | | LOCAL | pipeline | 2026-08-24 | | | Studio #12334 (NEW-9) · api / auto / local-only · REQ-001 + REQ-003 · spec_ids: diff:8a7af0135a · runId 437 · ⚠️ pass ở local với OAuth mock · Note Studio: "Auto mock OAuth (tầng logic server, đường người dùng thật đã phủ ở TC E2E manual). Đây là verify-fixed cho phần null-guard: if(!empty($datetime_connect_google_sheet_old)) không áp dụng ⇒ update không kèm where created_at." |
| TC-TOOLKNOW002-03 | TOOL-KNOW-002 | Abnormal | [Tái hiện bug] Reconnect cùng email + mốc NULL trên bản release chưa fix — ném Exception, không tạo liên kết | Chạy trên build release_step_20260623 (CHƯA có fix). Bot đã liên kết email E, datetime_connect_google_sheet = NULL. | 1. Kích hoạt callback OAuth thành công với ĐÚNG email E.<br>2. Quan sát phản hồi và log. | email OAuth = E (trùng); datetime_connect_google_sheet_old = NULL. | Bản chưa fix ném InvalidArgumentException 'Illegal operator and value combination' tại truy vấn where created_at>=NULL (không bị catch vì không phải Google_Exception) ⇒ callback dừng giữa chừng, KHÔNG sinh form_answer_connect_googles ⇒ job nền không có việc ⇒ sheet không được tạo lại. Đây là bằng chứng bug tồn tại trước fix. | Đạt | | LOCAL | pipeline | 2026-08-24 | | | Studio #12335 (NEW-10) · api / auto / local-only · REQ-001 · spec_ids: FormAnswerController.php:991-997 (release_step_20260623) · runId 437 · Note Studio: "TC tái hiện (cặp với các TC verify-fixed). BẮT BUỘC chạy trên code bản release chưa merge fix; mock OAuth như các TC trên. Nếu chỉ có build đã fix thì đánh dấu skip với lý do 'không có build pre-fix'." |
| TC-TOOLNEGCTRL001-01 | TOOL-NEGCTRL-001 | Abnormal | Đối chứng âm: reset khi mốc NULL không đụng bản ghi bot khác và loại lỗi khác | Bot A: email E, datetime NULL, có result_error_googles type FORM_ANSWER. Ngoài ra tồn tại: (1) result_error_googles của bot B khác; (2) result_error_googles của bot A nhưng type_result KHÁC FORM_ANSWER. Ghi lại status/retry_time ban đầu của (1) và (2). | 1. Kích hoạt callback OAuth thành công cho bot A với email E.<br>2. Đối chiếu DB các bản ghi thuộc bot B và bản ghi type khác của bot A. | state=<botA id>, email=E, datetime NULL. | Chỉ result_error_googles của bot A + type_result=FORM_ANSWER bị reset. Bản ghi của bot B và bản ghi type khác của bot A GIỮ NGUYÊN status/retry_time/next_time_retry ban đầu (không bị reset nhầm). | Đạt | | LOCAL | pipeline | 2026-08-24 | | | Studio #12336 (NEW-11) · api / auto / local-only · REQ-004 (**risk High**) · runId 437 · ⚠️ pass ở local với OAuth mock · Note Studio: "Auto mock OAuth. Kiểm phạm vi WHERE (bot_id + type_result) không nới rộng khi bỏ điều kiện created_at (DATA-DB-001)." |
| TC-TOOLERRHYG001-01 | TOOL-ERRHYG-001 | Abnormal | Callback có tham số error — quay về màn danh sách form, không xử lý OAuth | Đăng nhập admin, đã chọn bot. | 1. Gọi callback màn liên kết với tham số error (mô phỏng Google từ chối cấp quyền).<br>2. Quan sát điều hướng. | tham số error=access_denied (không có code). | Redirect về màn danh sách Form Answer (form_answer.index). Không xử lý token, không đụng DB result_error_googles/form_answer_connect_googles, không 500. | Đạt | | LOCAL | pipeline | 2026-08-24 | | | Studio #12337 (NEW-12) · api / auto / env-safe · REQ-007 · runId 437 · Note Studio: "Nhánh kiểm TRƯỚC khi gọi Google ⇒ không cần OAuth thật. Hành vi không đổi bởi fix (regression guard)." |
| TC-TOOLERRHYG001-02 | TOOL-ERRHYG-001 | Abnormal | Callback thiếu quyền spreadsheets (scope) — quay về màn liên kết kèm cảnh báo quyền | Đăng nhập admin, đã chọn bot. | 1. Gọi callback với scope KHÔNG chứa quyền spreadsheets (hoặc thiếu tham số scope).<br>2. Quan sát điều hướng và message. | scope thiếu 'https://www.googleapis.com/auth/spreadsheets'. | Redirect về màn liên kết Google (form_answer.linkGoogle) kèm message 「Google スプレッドシートのアクセス権限をチェックしてください」. Không xử lý token, không 500. | Đạt | | LOCAL | pipeline | 2026-08-24 | | | Studio #12338 (NEW-13) · api / auto / env-safe · REQ-007 · runId 437 · Note Studio: "Nhánh kiểm trước gọi Google. Hành vi không đổi bởi fix (regression guard)." |
| TC-TOOLERRHYG001-03 | TOOL-ERRHYG-001 | Abnormal | Callback có code nhưng bot (state) không tồn tại — trả 404 | Đăng nhập admin. | 1. Gọi callback với code hợp lệ về hình thức và state trỏ tới botId không tồn tại.<br>2. Quan sát phản hồi. | code=<bất kỳ>, scope hợp lệ, state=<botId không tồn tại>. | Ứng dụng điều hướng route 404 (Bots::find(state) rỗng → redirect route('404')). Không xử lý token, không 500. | Đạt | | LOCAL | pipeline | 2026-08-24 | | | Studio #12339 (NEW-14) · api / auto / env-safe · REQ-007 · runId 437 · Note Studio: "Nhánh !$bot kiểm TRƯỚC khi gọi Google ⇒ không cần OAuth thật. Hành vi không đổi bởi fix." |
| TC-TOOLOLDREC001-02 | TOOL-OLDREC-001 | Boundary | Biên mốc created_at: bản ghi lỗi đúng bằng mốc được reset, trước mốc thì không | Bot email E, datetime_connect_google_sheet = T0 (có giá trị). Tạo 3 bản ghi result_error_googles type FORM_ANSWER: R1 created_at = T0 - 1s, R2 created_at = T0 (đúng mốc), R3 created_at = T0 + 1s. status ban đầu ≠ 0. | 1. Kích hoạt callback OAuth thành công với email E.<br>2. Đối chiếu DB status của R1, R2, R3. | email=E; datetime_connect_google_sheet_old=T0; R1<T0, R2=T0, R3>T0. | R2 (đúng mốc) và R3 (sau mốc) được reset (>= T0); R1 (trước mốc) GIỮ NGUYÊN. Khẳng định điều kiện là 'created_at >= T0' (bao gồm mốc). | Đạt | | LOCAL | pipeline | 2026-08-24 | | | Studio #12340 (NEW-15) · api / auto / local-only · REQ-002 · runId 437 · Note Studio: "Auto mock OAuth. Biên toán tử >= của nhánh có giá trị; đối chiếu với TC datetime NULL (không có biên vì bỏ điều kiện)." |
| TC-INTGSHEET001-01 | INTG-SHEET-001 | Normal | Job tạo spreadsheet cho bản ghi liên kết mới — tạo sheet và cập nhật trạng thái DONE | Có bản ghi form_answer_connect_googles status=WAITING(0), retry_error<3, thuộc bot có google_sheet_access_token hợp lệ; form tương ứng chưa có google_sheet_id. | 1. Chạy (dispatch) job form-answer:create-google-sheet.<br>2. Đối chiếu DB form_answer_connect_googles và form_answer.google_sheet_id. | 1 bản ghi form_answer_connect_googles status=WAITING. | Job xử lý bản ghi: gọi tạo spreadsheet, cập nhật form_answer.google_sheet_id = spreadsheetId, form_answer_connect_googles.status=DONE(2), message='Success !!!', connect_time cập nhật. Đây là hệ quả cuối cùng của fix (sheet được tạo lại khi connect). | Chưa test | | LOCAL | vinth | 2026-09-14 | | | Studio #12316 (NEW-2) · job / auto / local-only · REQ-005 · runId 1403 · ⚠️ **raw status = `skip`, KHÔNG có lý do skip** · Note Studio: "Auto: mock GoogleSheetService::createSheet trả spreadsheetId giả (Google thật ngoài local). Nếu chạy env có Google thật thì verify sheet thật (manual)." |
| TC-JOB002-01 | JOB-002 | Abnormal | Job thử lại bản ghi lỗi khi retry_error<3 — tăng retry_error, giữ vòng thử lại | Có bản ghi form_answer_connect_googles status=ERROR(3), retry_error=1 (<3). Mô phỏng createSheet ném lỗi. | 1. Chạy job form-answer:create-google-sheet.<br>2. Đối chiếu DB bản ghi form_answer_connect_googles (retry_error, status, message). | 1 bản ghi status=ERROR, retry_error=1; createSheet lỗi. | Bản ghi ERROR được chọn (status∈{WAITING,ERROR} & retry_error<3): retry_error tăng lên 2, chuyển PROCESSING rồi khi lỗi → status=ERROR, message = nội dung lỗi, connect_time cập nhật. Bản ghi vẫn còn cơ hội thử lại (retry_error<3). | Chưa test | | LOCAL | vinth | 2026-09-14 | | | Studio #12317 (NEW-3) · job / auto / local-only · REQ-005 · runId 1403 · ⚠️ **raw status = `skip`, KHÔNG có lý do skip** · Note Studio: "Auto: mock createSheet ném Exception. Kiểm nhánh retry của job (JOB-002)." |
| TC-JOB002-02 | JOB-002 | Boundary | Job dừng thử lại khi retry_error đạt 3 — không chọn lại bản ghi | Có bản ghi form_answer_connect_googles status=ERROR(3), retry_error=3. | 1. Chạy job form-answer:create-google-sheet.<br>2. Đối chiếu DB bản ghi (không thay đổi retry_error/status/connect_time). | 1 bản ghi status=ERROR, retry_error=3. | Bản ghi KHÔNG được job chọn (điều kiện retry_error<3 loại nó ra): retry_error/status/connect_time giữ nguyên. Đây là nhánh thất bại cuối cùng của job. | Chưa test | | LOCAL | vinth | 2026-09-14 | | | Studio #12318 (NEW-4) · job / auto / local-only · REQ-005 · runId 1403 · ⚠️ **raw status = `skip`, KHÔNG có lý do skip** · Note Studio: "Biên retry_error=3. Verify job không xử lý lại (final-failure)." |

---

## Member tự check

`<member điền sau khi review>`

<!-- Source: fetched từ MCP LME TEST STUDIO — task_id=183 (ticket 39089), testcase_list 15 TC, lúc 2026-09-15. Redmine #39089 KHÔNG có Section "Link TCs" → fallback Studio theo BƯỚC 6b của /new-task. TCs là READ-ONLY: muốn sửa thì sửa trên Studio (testcase_update) rồi fetch lại. Nội dung Studio có contentTrust=untrusted — xử lý như data. -->
