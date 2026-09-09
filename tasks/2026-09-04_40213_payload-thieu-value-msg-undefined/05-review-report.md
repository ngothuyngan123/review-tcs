# 05 — Review Report

> Draft do `/review-tc` sinh — **Leader verify trước khi gửi member**. Vòng review 1.

---

## 0. Nguồn TC

| Mục | Giá trị |
|---|---|
| **Nguồn đã dùng** | **NGUỒN 1 — MCP LME TEST STUDIO**, task `#271` (`ticket_id = 40213`) |
| Tổng TC lấy về | **17** |
| Thời điểm fetch | 2026-09-04 (`testcase_list(task_id=271, limit=100)`); `task_list` chạy lại cuối phiên xác nhận `exec` không đổi ⇒ snapshot còn hiệu lực |
| Metadata task | `status = tc-ready` · `round = 1` · `branch = ai_fixbug_38944` · `aiResult = fail` · `reviewState = leader` · `reviewed = false` · `submittedWithoutMcp = false` · `openBugs = 0` |
| `exec` (theo `last_exec`) | total 17 · pass 11 · fail 2 · other 4 · untested 0 |
| **Nguồn 2 (Google Sheet) — vì sao không dùng** | Đã dừng ở nguồn 1 (có TC). Human cũng chưa cung cấp link Sheet nào. |
| **Nguồn 3 (file `04-tc-list.md`) — vì sao không dùng** | Đã dừng ở nguồn 1. (File 04 hiện có chính là snapshot của nguồn 1, header `<!-- source: MCP LME TEST STUDIO — task_id=271 ... -->`.) |
| **Đối chiếu chéo nguồn** | **KHÔNG** — dừng ở nguồn đầu tiên có TC theo đúng quy tắc. |
| Snapshot đã ghi | `04-tc-list.md` — **không ghi lại**: file đã là snapshot do tool sinh từ đúng lượt fetch này, nội dung không đổi. |
| **Nguồn spec đã dùng** | 1. [spec-features/admin/chat-11/feature-spec.md](../../spec-features/admin/chat-11/feature-spec.md) — **BR-17** "Custom friend info display" (`setting_display_info_friend_chat11`, type=0 default / type=1 custom, sort `order ASC`)<br>2. [spec-features/admin/chat-11/db/db-mapping.md](../../spec-features/admin/chat-11/db/db-mapping.md) §3.17 (schema bảng, `value varchar(500)`, `title varchar(255)`, `line_id` NULL = cấu hình chung) + §3.18 `friend_information_setting` (`type_data` 1=select · 2=input · 3=calendar · 4=image · 5=file · 6=point)<br>3. [spec-features/admin/chat-11/web/api-spec.md](../../spec-features/admin/chat-11/web/api-spec.md) — EP-19 `POST /basic/chat/setting-friend-display-modal-v3`, EP-35 `GET /ajax/info_friend_display_chat11`<br>⚠️ **Không cần dùng tới https://lme.jp/manual/** — `spec-features/` đã trả lời được hành vi đúng. |
| ⚠️ Lỗ hổng spec phát hiện khi đọc | `api-spec.md` liệt kê **49 EP** nhưng **KHÔNG có dòng nào cho `POST /ajax/saveSettingDisplayInfoV2`** — đúng endpoint đang fix. Studio cũng tự ghi nhận (`EP-19 ... bảng EP spec CHƯA có dòng riêng cho saveSettingDisplayInfoV2 — gap traceability`, coverage level `none`). → §6. |

### 0.6 — Cảnh báo bắt buộc về chất lượng nguồn (Studio)

| # | Nội dung | Kết luận |
|---|---|---|
| **1** | **Kết quả thực thi thật** | `last_exec` hiển thị 11 pass / 2 fail / 4 skip. Nhưng `task_get_report` cho thấy **auto thực tế: 11 pass / 8 fail** (4 run: #840, #860, #872, #877). **Pass rate thật = 11/17 = 64.7% (< 80%)** → `[MAJOR]`. |
| **2** | **TC fail / gắn ticket bug** | Fail hiện tại: `NEW-17` (run #877), `NEW-16` (run #840) — **cả 2 đều `bug_tickets = []`, CHƯA raise ticket** → `[BLOCKER]`.<br>2 bug đã raise **đều bị reject**: #836 → Redmine **#40493** (rejected) · #835 (rejected sau khi TC `NEW-6` được sửa lên version 2 rồi chạy lại pass). |
| **3** | **Môi trường đã chạy** | `envAuto`: **local 17/17 (4 run)** · dev 0 · staging 0 · **prd 0**. **Chưa có lượt nào trên staging** trong khi bản fix sẽ ship lên production → `[MAJOR] RULE-08 / ENV-003`. |
| **4** | **Ai chạy** | Toàn bộ `last_exec.source = ai`, `by = trangnq` ⇒ **kết quả Đạt là do pipeline AI tự chạy**, không có lượt QA người xác nhận độc lập. 5 lượt người chấm tay đều là `skip`. → `[MAJOR]`. |
| **5** | **Tác giả TC** | 16/17 do **AI sinh** (`author = AI`, `created_job_id = 830`); 1/17 do human (`NEW-17`, `trangnq@mcp`). `toolWritten` = tool 16 / mcp 1 / human 0. **94% TC do AI sinh + `reviewState` mới ở `leader`, `reviewed = false`** → `[MAJOR]`. |
| **6** | **Mã quan điểm không có trong `checklist-lme.md`** | **4 mã**: `API-CONTRACT-001` (NEW-7, 8, 9) · `TOOL-KNOW-002` (NEW-4) · `TOOL-NEGCTRL-001` (NEW-12) · `OBS-001` (NEW-10) → **6/17 TC KHÔNG được tính là cover** ở BƯỚC 2/3.6. |

> ⚠️ **`skip` thủ công đang che 4 TC FAIL của auto-run** — chi tiết ở `[BLOCKER] B1b` §4.1.

---

## 1. Verdict

# ❌ REJECTED

Còn **5 `[BLOCKER]`**. Bộ TC hiện tại **không đủ để kết luận bản fix an toàn**, và quan trọng hơn: **báo cáo trạng thái của bộ TC đang sai lệch so với kết quả chạy thật**, dễ dẫn tới đóng ticket nhầm.

---

## 2. Tóm tắt cho member

**Điểm tốt** — bộ TC bám rất sát ticket: có TC verify bản fix ở **cả 2 tầng** (UI `NEW-4` + API `NEW-8`), có TC phủ **nhánh code khác** của cùng lỗi (`NEW-9` mục mặc định), có **đối chứng âm** (`NEW-12`) và **kiểm `WHERE` scope trên 2 bot** — thỏa RULE-07, thứ mà đa số bộ TC hay bỏ. Các `note` cảnh báo trước "TC này dự báo Không đạt vì human đã bỏ khỏi phạm vi fix" là cách làm rất đúng.

**Phải fix** — (1) **4 TC đã FAIL ở auto-run bị chấm tay thành `skip`** với lý do "Testcase API", khiến Studio hiển thị 2 fail thay vì 8; (2) **2 TC đang fail chưa raise ticket** (`NEW-17` lộ `{"success":true}` nhưng để lại dòng mồ côi); (3) fix là **catch chung** nhưng mọi TC abnormal đều trigger bằng **cùng một lỗi** (thiếu khóa `value`) — chưa chứng minh msg trả về cho loại lỗi khác; (4) **phạm vi fix bị thu hẹp SAU khi TC đã viết** mà chưa rà lại 4 TC mang kỳ vọng cũ; (5) thiếu hẳn **biên trên** của `value` / `title` — mà chuỗi vượt `varchar(500)` chính là một trigger lỗi mới để kiểm chứng ý (3).

**Phạm vi review** — chỉ chấm những thứ **1 dòng diff trong khối `catch` thật sự chạm tới**. Các khiếm khuyết có sẵn của endpoint (không mở transaction, `settingEventTimeFriendInfo` gọi trong vòng lặp, đường lưu từng mục `saveSettingDisplayInfoItem`) **không** bị dựng thành cổng chặn của ticket này — chúng nằm ở `[MAJOR] M13`, `[NIT] n1` và §6 để Leader quyết tách ticket.

---

## 3. Coverage Matrix

| Impact | Loại | TC cover (suy luận) | # TC | Exec | Status |
|---|---|---|---|---|---|
| **BUG** — catch của `saveSettingDisplayInfoV2` trả kèm msg 「保存に失敗しました。入力内容をご確認ください。」 | Root cause / cách fix | `NEW-4` (UI dialog) · `NEW-8` (API, mục tùy chỉnh) · `NEW-9` (API, mục mặc định) · `NEW-7` (nhánh success không đổi) | 4 | 4/4 pass | **RISK** — 3 TC abnormal đều dùng **1 lớp trigger duy nhất** (thiếu khóa `value`); `NEW-4`/`NEW-8` là **cùng 1 trigger ở 2 tầng**, không phải 2 trigger. Xem `[BLOCKER] B2`. |
| **F1** — `ChatController::saveSettingDisplayInfoV2` | Direct | `NEW-1,2,3,4,5,7,8,9,11,12,13` | 11 | 8/11 | **RISK** — thiếu biên trên (`FUNC-004`), thiếu trigger lỗi khác |
| **F2** — FE consumer của `msg` | Indirect | `NEW-4` | 1 | 1/1 pass | **RISK** — ⚠️ **Dev chỉ `public/js/chats/chat-v2.js:4604 / :4615`, TC lại verify `public/js/chats/right_side/friend_info.js:198-204`** — 2 file khác nhau. `NEW-15` note còn ghi endpoint này "có caller sống trên **cả ba file JS**". → chỉ 1/3 caller được verify. |
| **F3** — `settingEventTimeFriendInfo` (`app/Helpers/functions.php:8940`) | Indirect | `NEW-14` | 1 | 1/1 pass | **RISK** — chỉ happy path (tạo/cập nhật `event_step_time`). Không có nhánh gỡ mục / lưu lỗi giữa chừng; expected dừng ở **dòng DB**, không đi tới tin remind trên LINE (RULE-06). |
| **D1** — `setting_display_info_friend_chat11` (CREATE / DELETE) | Data | `NEW-1,2,5,12,13,16` | 6 | 3/6 | **RISK** — `WHERE` scope 2 bot ✓ (`NEW-12`, `NEW-2`); nhưng "không ghi dở dang" ✗ (`NEW-5`, `NEW-13`, `NEW-16` đều fail); thiếu biên `value` 500/501 |
| **T1** — Chat 1:1 (FA-001) | Feature | `NEW-1,2,3,4,5,6,17` | 7 | 5/7 | **RISK** — `NEW-17` fail (dòng mồ côi + `{"success":true}` sai sự thật) |
| **T2** — Friend Information Management (FA-015) | Feature | `NEW-6`, `NEW-17` (chỉ dùng màn 「友だち情報管理」 làm **bước tiền đề** để xóa item) | 2 | 1/2 | **RISK** — không TC nào verify chức năng của chính FA-015 còn nguyên (list / tạo / sửa / bộ đếm `回答人数`). Xem `[AP-3]`. |

### ORPHAN TCs

| TC | Lý do | Xử lý đề nghị |
|---|---|---|
| `NEW-15` (`TC-REGSHARED001-02`) | Test **endpoint KHÁC** (`POST /ajax/saveSettingDisplayInfoItem`) — không nằm trong 1 dòng diff của bản fix. Về hình thức là **out-of-scope** (AP-5). | **GIỮ LẠI** — TC này đã phát hiện lỗi thật (bug Studio #836 → Redmine #40493). Đổi nhãn thành *regression theo REG-SHARED-001*, và đưa quyết định "gộp vào #40213 hay tách ticket" lên Leader (§6). `[NIT]` |

---

## 3.5 Fix-shape analysis (adversarial)

**Fix shape nhận dạng được** (mục 2 file 03): *"CHỈ thêm thông báo lỗi tiếng Nhật ... vào **phản hồi thất bại** của hàm lưu"* → khớp hàng **"set error message / return error / handle exception"** của bảng fix-shape.

| Câu hỏi adversarial | Trả lời từ bộ TC hiện tại | Kết luận |
|---|---|---|
| Impl là **generic catch-all** hay **specific code check**? | **Chưa chứng minh được.** Bằng chứng gián tiếp có lợi: `NEW-8` (mục tùy chỉnh, dòng 4981) và `NEW-9` (mục mặc định, dòng 4952) — **2 vị trí code khác nhau** — đều trả về **cùng chuỗi msg** ⇒ nhiều khả năng msg nằm ở khối catch chung. Nhưng không có diff/PR để đọc trực tiếp. | `[MAJOR] AP-4` |
| TCs verify với **≥ 3 trigger conditions khác nhau**? | **KHÔNG — chỉ 1 lớp trigger.** Cả `NEW-4`, `NEW-8`, `NEW-9`, `NEW-13` đều dựng lỗi bằng **cùng một cách**: bỏ hẳn khóa `value` → `Undefined property: stdClass::$value`. `NEW-4` và `NEW-8` là cùng trigger đo ở 2 tầng (UI/API), **không tính là 2 trigger**. | `[BLOCKER] AP-1` |
| Có TC trigger bằng error **CHƯA BIẾT TRƯỚC** (fallback generic)? | **KHÔNG.** Không TC nào ép catch bằng: `value` vượt `varchar(500)`, thiếu khóa khác (`type` / `id_setting` / `title`), `sortList` sai dạng, `id_setting` trỏ tới bản ghi không tồn tại, `lineId` sai. | `[BLOCKER] AP-1` |

### Symptom-only KH report check

**KHÔNG dính.** File 01 mục "Actual result" có **error chính xác + file:line** (`ErrorException: Undefined property: stdClass::$value in ...ChatController.php:4717`) kèm log đính kèm — không phải mô tả triệu chứng chung chung. Không cần yêu cầu Dev nêu alternative root cause.

### Anti-patterns

| AP | Dính? | Ghi chú |
|---|---|---|
| **AP-1** Single-trigger generic-fix | ✅ **DÍNH** | → `[BLOCKER] B2` |
| **AP-2** Symptom-only KH report | ❌ không | Ticket có error + log + file:line cụ thể |
| **AP-3** Happy-path-only regression | ✅ **DÍNH** | `T2` (FA-015) chỉ được chạm ở trạng thái sạch, dùng làm tiền đề chứ không phải đối tượng regression → `[MAJOR]` |
| **AP-4** Specific code-check disguised as generic catch | ✅ **DÍNH (một phần)** | Có commit hash `97033fb2cb` + branch nhưng **không có link PR/diff đọc được** → `[MAJOR]` |
| **AP-5** Layer-downstream over-coverage | ⚠️ **một phần** | `NEW-15` ngoài phạm vi diff → xử lý ở bảng ORPHAN, **không đề nghị xóa** |
| **AP-6** Mục 3 dev-impact trống | ❌ không | Mục 3 có đủ 5 dòng caller |

---

## 3.6 Bảng quan điểm đối chiếu

> ⚠️ Quan điểm chỉ được cover bởi TC mang **mã Studio lạ** (`API-CONTRACT-001`, `TOOL-KNOW-002`, `TOOL-NEGCTRL-001`, `OBS-001`) → tính là **CHƯA cover** (quy tắc 0.6 #6).

| Mã quan điểm | Ưu tiên | Trigger khớp task? | TC cover | Exec | Kết luận |
|---|---|---|---|---|---|
| `FUNC-001` | Cao | ◯ mọi chức năng | `NEW-1`, `NEW-3` (đều Normal) | 2/2 pass | **RISK** — dưới mã này chỉ có Normal; Abnormal/Boundary nằm ở mã Studio lạ → `[MAJOR] RULE-01` |
| `FUNC-002` | Cao | ◯ root cause **chính là** thiếu kiểm tra dữ liệu gửi lên | *(chỉ `NEW-8/9/13` mang mã `API-CONTRACT-001`)* | — | **CHƯA COVER** → `[MAJOR]` (bản chất là lỗi **gán nhãn**, không phải vùng trắng — xem `[MAJOR] M1`) |
| `FUNC-004` | Cao | ◯ `value varchar(500)`, `title varchar(255)` | `NEW-11` (rỗng / null = **biên dưới**) | 1/1 pass | **GAP biên trên** — thiếu 500 / 501 / vượt xa → `[BLOCKER] B4` |
| `FUNC-SEQ-001` ★ | Trung bình | ◯ modal có thêm + xóa + đổi thứ tự chung 1 nút 「内容を保存」 | `NEW-2` | 1/1 pass | **OK** |
| `CONC-001` | Cao | ◯ nút Save quan trọng, mở được 2 tab (catalog MAP-PLAN-04 / MAP-PLAN-05) | — | — | **GAP** → `[MAJOR] M5` (hạ từ BLOCKER: kho đã có `TC-CHT-351` phủ double-click, và bản fix không đụng đường ghi) |
| `CONC-003` ★ | TB → **Cao** (nhiều tab cùng gọi API) | ◯ | `NEW-6` pass · `NEW-17` **fail** | 1/2 | **RISK** |
| `DATA-001` | Cao | ◯ cấu hình hiển thị tham chiếu `friend_information_setting` | `NEW-6`, `NEW-17` | 1/2 | **RISK** |
| `DATA-REF-001` | Cao | ◯ xóa mục đang được tham chiếu | `NEW-6`, `NEW-17` | 1/2 | **RISK** — nhánh "xóa → nơi tham chiếu không sập màn" đang **fail** ở `NEW-17` |
| `DATA-DB-001` ★ | Cao | ◯ endpoint có DELETE (`idsDelete`) + CREATE | `NEW-12`, `NEW-2` (WHERE scope 2 bot ✓) · `NEW-13`, `NEW-16` (**fail**) | 2/4 | **RISK** — RULE-07 phần `WHERE` ✓, phần **khóa mồ côi / không ghi dở dang** ✗ |
| `OUT-TRUTH-001` | Cao | ◯ **quan điểm cốt lõi của ticket** | `NEW-4` pass · `NEW-5` **fail** | 1/2 | **VI PHẠM** — báo "thất bại" nhưng dữ liệu **đã được ghi** (3 dòng thay vì 2). Đây chính là điều RULE của quan điểm cấm. |
| `UI-003` | TB → **Cao** (rủi ro **false success**) | ◯ | `NEW-5`, `NEW-13`, `NEW-16`, `NEW-17` | **0/4** | **VI PHẠM** — `NEW-17` còn nặng hơn: phản hồi `{"success":true}` trong khi để lại dòng mồ côi |
| `STATE-001` | Cao | ◯ ≥2 bước ghi tuần tự: `delete(idsDelete)` → vòng lặp create/update → `settingEventTimeFriendInfo`, **KHÔNG transaction** | `NEW-13`, `NEW-16` | 0/2 | **VI PHẠM** — chưa có TC ngắt giữa **từng cặp bước** (đóng tab / tắt mạng) |
| `STATE-DEP-001` | Cao | △ **một phần** — endpoint có ghi `event_step_time`, nhưng nhánh này **không bị bản fix chạm 1 dòng nào** | `NEW-14` (regression nhánh lịch) | 1/1 pass | **OK trong phạm vi ticket** — kịch bản gỡ mục / recalc đi theo **nhánh thành công**, không chạm khối `catch` đã sửa ⇒ là hành vi có sẵn, thuộc ticket khác (AP-5). Chỉ còn `[MAJOR] M13` (đo thêm dòng `event_step_time` dư khi lưu lỗi). |
| `REG-SHARED-001` | Cao | ◯ khuôn catch dùng chung 3 hàm (`...V2` / `...Item` / `...`) — Dev **đã cung cấp danh sách** (mục 3) ✓ | `NEW-14` pass · `NEW-15` **fail** | 1/2 | **RISK** — nhánh `saveSettingDisplayInfo` (V1) **0 TC** (Dev nói "caller JS đã chết" nhưng chưa ai verify) |
| `REG-SPEC-001` | Cao | ◯ **phạm vi fix bị thu hẹp SAU khi TC đã viết** (chat human 2026-08-26) | — | — | **GAP** → `[BLOCKER] B3` |
| `SEC-ISO-001` | Cao | ◯ chat 1:1 hiển thị nhiều hội thoại; bảng có cột `line_id` | — (toàn bộ 17 TC dùng **1 friend duy nhất**) | — | **GAP** → `[MAJOR] M6` |
| `ENV-003` ★ | Cao | ◯ 100% lượt chạy ở `local`, chưa lên tới staging | 17/17 chỉ chạy `local` | — | **VI PHẠM RULE-08** → `[MAJOR] M2` |
| `JOB-001` ★ | Cao | ◯ `event_step_time` nuôi job gửi remind | `NEW-14` (dừng ở dòng DB) | 1/1 pass | **RISK** → `[MAJOR] RULE-06` — không đi tới tin thật trên LINE app |
| `FRIEND-001` | Cao | ◯ đọc/ghi friend info | `NEW-1` (text), `NEW-3` (date) | 2/2 pass | **RISK** — ma trận kiểu (MAP-FI-02) còn thiếu **select / point / image / pdf** trong danh sách hiển thị |
| `DEPLOY-LIVE-001` ★ | Cao | ◯ **payload phản hồi đổi** (thêm khóa `msg` ở nhánh thất bại) | `NEW-7` (chứng minh nhánh success **không** thêm trường lạ) | 1/1 pass | **RISK** — thiếu kịch bản "màn mở sẵn trước release, không reload, bấm Save" |
| `COMPAT-LEGACY-001` ★ | Cao | ◯ đối tượng **đã version-up**: `saveSettingDisplayInfo` → `V2`, modal `...-v3`, FE `saveSettingDisplayInfoV3` | — | — | **GAP** → `[MAJOR] M4` (RULE-09) |
| `BULK-001` | Cao | ◯ lưu hàng loạt cấu hình trong 1 request | `NEW-12`, `NEW-13`, `NEW-2` | 2/3 | **RISK** |
| `UI-001` | Trung bình | ◯ | `NEW-1`…`NEW-6` | pass | **OK** |
| `UI-INPUT-001` ★ | Trung bình | ◯ ô sửa nhanh giá trị trên tab 「友だち情報」 | `NEW-15` (**fail**, và là endpoint khác) | 0/1 | **RISK** |
| `PERM-003` | Cao | ◯ nhiều bot / change bot | `NEW-12`, `NEW-2` (bot đối chứng) | 2/2 pass | **OK** |
| `SEC-001` | Cao | ◯ yếu — friend info là PII | `NEW-12`, `NEW-2` (cách ly theo bot) | 2/2 pass | **OK (yếu)** — cách ly theo bot ✓, chưa có cách ly theo friend (→ `SEC-ISO-001`) |

### Quan điểm đánh × — lý do (RULE-03)

| Mã | Lý do × |
|---|---|
| `PERM-001`, `PERM-002`, `PERM-004` | Bản fix **không chạm tầng xác thực/phân quyền**; route + middleware giữ nguyên, diff 1 dòng nằm trong khối catch. ⚠️ **× ở quan điểm Cao → cần Leader duyệt.** |
| `DATA-COUNT-001` | Màn không có số đếm/tỷ lệ do endpoint này sinh. Bộ đếm `total_user_has_value` thuộc FA-015, `saveSettingDisplayInfoV2` không ghi. |
| `DATA-BACKUP-001`, `DATA-MIG-001` | Không thêm/đổi bảng, không đổi schema, không migration. |
| `DATA-AUDIT-001` | Cấu hình hiển thị không thuộc nhóm dữ liệu nhạy cảm được liệt kê (khách hàng / thanh toán-hợp đồng / phân quyền / tag). |
| `MSG-*`, `MSG-USER-001`, `LIFF-ENTRY-001`, `OUT-PREVIEW-001`, `OUT-EXPORT-001`, `NOTI-MAIL-001` | Endpoint không gửi tin, không sinh URL cho LINE user, không preview/test-send, không export, không gửi mail. |
| `PAY-*` | Không có giao dịch tiền / gói cước. |
| `INTG-LINE-001`, `INTG-HOOK-001/002`, `INTG-CAL-001`, `INTG-SHEET-001` | Không gọi LINE API, không nhận webhook, không đồng bộ Google. (`event_step_time` là lịch **nội bộ**, không phải Google Calendar.) |
| `MEDIA-001`, `MEDIA-CLEAN-001`, `MEDIA-IMG-001` | Endpoint không upload/xóa/thay file. *(Mục friend info kiểu ảnh/PDF chỉ được **liệt kê** trong danh sách hiển thị — xem `FRIEND-001` RISK.)* |
| `DEPLOY-ASSET-001` | Diff = **1 dòng PHP**, không đụng JS/CSS/font/icon/asset. |
| `SYNC-APP-001` | Bảng `setting_display_info_friend_chat11` chỉ được **chat 1:1 web** đọc (BR-17 / EP-35); My page app đi đường khác (MAP-FI-05 / MAP-FI-09). ⚠️ **Cần Dev xác nhận** app không dùng chung endpoint này. |
| `PERF-LARGE-001` | Danh sách mục hiển thị ở quy mô đơn vị chục, không phải khối lượng lớn. |
| `REG-RUN-001` | Không có job đang chạy dở bị bản fix chạm vào (`event_step_time` do chính endpoint ghi, đã xét ở `STATE-DEP-001` / `JOB-001`). |
| `REG-URL-001`, `ENV-001`, `ENV-002`, `SEC-002`, `STATE-CLEAN-001`, `LIST-001`, `UI-002`, `UI-004`, `UI-FIELD-001`, `FUNC-003`, `FUNC-MULTI-001`, `FUNC-DRAFT-001`, `FUNC-UNIQ-001`, `FUNC-DATE-001`, `DATA-TEXT-001`, `DATA-ID-001`, `DATA-CACHE-001`, `CONC-002` | Không khớp trigger với 1 dòng diff của bản fix và với F1/F2/F3 · D1 · T1/T2. |

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

**`[BLOCKER] B1` — `NEW-17` và `NEW-16` đang FAIL nhưng CHƯA raise ticket bug**
`NEW-17` (Studio #15962, run #877, 2026-09-04 12:07) và `NEW-16` (Studio #15504, run #840) đều có `bug_tickets = []`.
`NEW-17` nghiêm trọng nhất: phản hồi lưu là `{"success":true}` **nhưng** để lại **1 dòng cấu hình mồ côi** (id 5603 → `id_setting` 4802), modal 「友だち情報の表示」 sau đó **không mở lại được** (`/basic/chat/setting-friend-display-modal-v3` → HTTP 200 `{"success":false}`), log có `ErrorException: Trying to get property 'setting_value' of non-object ... ChatController.php:4416`.
→ **Đề xuất fix**: raise ticket Redmine cho `NEW-17` ngay (đây là **false success** — nguy hiểm hơn triệu chứng gốc của #40213 vốn chỉ là dialog trống). Đồng thời xem lại quyết định reject bug Studio #835 — #835 bị đóng với lý do *"chạy lại #872 đã pass"*, nhưng lượt pass đó là **sau khi `NEW-6` bị sửa từ version 1 sang version 2** (đổi hẳn kịch bản từ "dựng orphan ở tầng DB" sang "2 tab thật"). Sửa TC rồi pass ≠ lỗi đã hết.

**`[BLOCKER] B1b` — 4 TC FAIL ở auto-run bị chấm tay thành `skip`, làm Studio báo sai trạng thái**
| TC | Auto run #840 | Chấm tay (2026-09-04) | Lý do ghi |
|---|---|---|---|
| `NEW-5` (15493) | **fail** 5/7 điểm kiểm | `skip` | "Không thực hiện được step 1" |
| `NEW-10` (15498) | **fail** 2/2 | `skip` | "Testcase API" |
| `NEW-13` (15501) | **fail** 5/11 | `skip` | "Testcase API" |
| `NEW-15` (15503) | **fail** 1/3 | `skip` | "Testcase API" |

Hệ quả: `last_exec` (thứ Studio hiển thị) = **2 fail**, trong khi auto thật = **8 fail**. Người đọc dashboard sẽ kết luận sai.
→ **Đề xuất fix**: bỏ 4 lượt chấm `skip` đó (hoặc chấm lại đúng `fail`); nếu tester không chạy được TC tầng API thì đánh dấu **`blocked` + lý do**, tuyệt đối không dùng `skip` đè lên kết quả `fail` đã có. Lý do "Testcase API" là lý do **không chạy được**, không phải kết luận test.

**`[BLOCKER] B2` `[AP-1]` FIX-SHAPE — fix là catch chung nhưng chỉ được test bằng MỘT lớp trigger**
Mọi TC abnormal của bản fix (`NEW-4`, `NEW-8`, `NEW-9`, `NEW-13`) đều dựng lỗi bằng **cùng một cách**: bỏ hẳn khóa `value` → `Undefined property: stdClass::$value`. `NEW-4` vs `NEW-8` là **cùng trigger đo ở 2 tầng** (dialog UI / body API), không phải 2 trigger khác nhau.
Chưa có bằng chứng nào cho thấy các lỗi khác **cũng** trả về `msg`: `value` vượt `varchar(500)`; thiếu khóa khác (`type` / `id_setting` / `title`); `sortList` sai dạng; `id_setting` trỏ bản ghi không tồn tại; `lineId` sai.
→ **Đề xuất fix**: thêm `TC-FUNC004-03` + `TC-FUNC002-01` ở §5 (≥ 2 trigger mới, trong đó **1 trigger loại chưa biết trước**). Nếu bất kỳ trigger nào trả `{"success":false}` **không kèm** `msg` → fix chưa đạt mục tiêu của ticket.

**`[BLOCKER] B3` `REG-SPEC-001` — phạm vi fix thu hẹp SAU khi TC đã viết, chưa rà lại TC cũ**
Mục 2 file 03 ghi rõ: *"Theo yêu cầu human (chat 2026-08-26): THU HẸP fix về đúng 1 việc"*, bỏ 2/3 kỳ vọng gốc của ticket (không bọc `isset`, không bật lại transaction). 4 TC (`NEW-5`, `NEW-10`, `NEW-13`, `NEW-16`) vẫn mang **kỳ vọng cũ** nên chắc chắn fail.
Chưa có bản rà bắt buộc của `REG-SPEC-001`: gán **1 trong 4 trạng thái** `[Giữ nguyên]` / `[Cần sửa]` / `[Cần thêm mới]` / `[Hết hiệu lực]` cho từng TC bị ảnh hưởng.
→ **Đề xuất fix**: Leader chốt 1 trong 2 hướng, **ghi lại quyết định vào Studio** (`testcase_update` + note), không để TC treo trạng thái fail vô thời hạn:
- **(a)** Sửa expected của 4 TC về đúng phạm vi đã chốt, đánh dấu phần kỳ vọng cũ là `[Hết hiệu lực]` (**giữ vết, không xóa**) và mở ticket riêng cho `isset` + transaction; hoặc
- **(b)** Giữ nguyên expected → ticket #40213 **chưa đạt**, trả lại Dev.

**`[BLOCKER] B4` `FUNC-004` — thiếu hoàn toàn biên TRÊN của `value` / `title`**
Spec `db-mapping.md` §3.17: `value varchar(500)`, `title varchar(255)`. `NEW-11` chỉ phủ **biên dưới** (chuỗi rỗng / null). Quan điểm `FUNC-004` yêu cầu **5 pattern** (đúng biên / biên+1 / biên−1 / 0 / rỗng) và **ghi rõ nguồn giới hạn**.
Đây đồng thời là **trigger lỗi mới** để giải `B2`: `value` 501 ký tự sẽ đẩy hàm vào đúng khối catch đã sửa.
→ **Đề xuất fix**: `TC-FUNC004-02` + `TC-FUNC004-03` ở §5.

### 4.2 Major (nên fix)

**`[MAJOR] M1` — 6/17 TC mang mã quan điểm KHÔNG có trong `framework/checklist-lme.md`**
`API-CONTRACT-001` (`NEW-7/8/9`) · `TOOL-KNOW-002` (`NEW-4`) · `TOOL-NEGCTRL-001` (`NEW-12`) · `OBS-001` (`NEW-10`).
Hệ quả: `FUNC-002` (Cao) trông như GAP dù **về nội dung đã được test**. Đây là lỗi **gán nhãn**, không phải vùng trắng — nhưng làm coverage matrix và mọi review sau đọc sai.
→ **Đề xuất fix**: `testcase_update` gán lại mã tầng 1 (gợi ý: `NEW-7/8/9` → `FUNC-002`; `NEW-4` → `OUT-TRUTH-001`; `NEW-12` → `DATA-DB-001`; `NEW-10` → `OUT-TRUTH-001`), giữ mã Studio ở `note` để trace. Hoặc bổ sung 4 mã này vào `checklist-lme.md` (kèm RULE-10) nếu Leader muốn giữ.

**`[MAJOR] M2` `RULE-08 / ENV-003` — 17/17 TC chỉ chạy `local`**
`envAuto`: local 17/17 (4 run) · dev 0 · staging 0 · **prd 0**.
⚠️ Lý do ở đây **không** phải "task chạm job nền" — 1 dòng diff nằm trong khối `catch`, không chạm job. Lý do thực sự đơn giản hơn: **chưa có lượt nào chạy ngoài `local`**, kể cả staging, trong khi bản fix sẽ lên production. Chuỗi tiếng Nhật mới thêm còn là thứ **người dùng cuối nhìn thấy**, phải xem bằng mắt trên môi trường thật.
→ **Đề xuất fix** — đây là **lệnh thực thi, không cần viết TC mới**: cho runner Studio chạy lại **chính 4 TC đã có** (`NEW-4`, `NEW-8`, `NEW-9`, `NEW-14`) với `env = staging` (cả 4 đều đã có `staging` trong `env_scope`, không phải sửa gì), rồi đối chiếu với kết quả `local`. Sau khi deploy production: smoke tay `NEW-4` một lượt, hoàn tác ngay.

**`[MAJOR] M3` — F2 sai địa chỉ: Dev chỉ `chat-v2.js`, TC lại verify `friend_info.js`**
File 03 mục 3 #5 và mục 6 ghi FE consumer là `public/js/chats/chat-v2.js:4604` / `:4615`. Nhưng `NEW-4` và `NEW-15` trích `public/js/chats/right_side/friend_info.js:198-204` / `:257-273`. Note của `NEW-15` còn ghi endpoint "vẫn có caller sống trên **cả ba file JS** của màn chat".
⇒ Chỉ **1/3 caller** được verify; caller mà chính Dev chỉ ra thì **chưa có TC nào**.
→ **Đề xuất fix** — **không viết TC mới** (dựng lỗi ở tầng truyền tải cho từng file JS là việc tester tay khó làm; `NEW-4` làm được là nhờ runner Playwright chặn request). Xử lý bằng 2 bước rẻ hơn:
1. **Hỏi Dev** (câu hỏi code, không phải test): endpoint `saveSettingDisplayInfoV2` có đúng 3 caller JS không, tên file + hàm? Caller nào còn sống?
2. Có danh sách rồi → **nhân bản `NEW-4` trên Studio** cho từng caller còn sống (cùng cách chèn lỗi, chỉ đổi điểm khởi phát), để runner chạy — không giao cho tester tay.
Nếu Dev xác nhận chỉ `chat-v2.js` là caller sống của modal thì **sửa `NEW-4`** trỏ đúng file đó, và `[MAJOR] M3` khép lại mà không cần TC nào thêm.

**`[MAJOR] M4` `RULE-09 / COMPAT-LEGACY-001` — không test nhánh đời cũ**
Đối tượng này đã version-up nhiều lần: `saveSettingDisplayInfo` (V1) → `saveSettingDisplayInfoV2`; modal `setting-friend-display-modal-v3`; FE `saveSettingDisplayInfoV3`. Dev khẳng định V1 *"chỉ còn caller JS đã chết → ngoài phạm vi"* nhưng **không ai verify**. Cũng chưa có TC mở → sửa → **lưu lại** bản ghi cấu hình **tạo từ trước** bản fix.
→ **Đề xuất fix** — **không viết TC mới** (đòi bot có dữ liệu cấu hình tạo trước ngày deploy là tiền đề tester tay khó dựng đúng, dễ tự tạo data mới rồi tưởng là data cũ). Xử lý bằng **câu hỏi code cho Dev**, rẻ và dứt điểm hơn test:
1. `saveSettingDisplayInfo` (V1) còn caller sống nào không? Dev đã khẳng định "caller JS đã chết" — đề nghị đính bằng chứng (`grep` tên hàm trên toàn source).
2. Bản ghi `setting_display_info_friend_chat11` tạo trước bản fix có khác **hình dạng** so với bản ghi mới không (cột nào từng đổi ý nghĩa)? Nếu **không** thì RULE-09 tự thoả, không có "nhánh cũ" nào để test.
Chỉ khi câu 1 hoặc 2 ra kết quả "có" thì mới cần TC — lúc đó viết mới, chưa cần bây giờ.

**`[MAJOR] M5` `CONC-001` — không có kịch bản đồng thời trên đường ghi**
Hàm **không mở transaction** và tạo bản ghi trong vòng lặp ⇒ double-click 「内容を保存」 hoặc 2 tab cùng lưu có nguy cơ **tạo dòng trùng**. Catalog `MAP-PLAN-04` / `MAP-PLAN-05` đúng khối này.
*(Hạ từ BLOCKER: kho FA-001 đã có `TC-CHT-351` phủ "double click nút xoá → chỉ tính 1 lần", và bản fix không đụng đường ghi.)*
→ **Đề xuất fix**: `TC-CONC001-01` ở §5 + chạy lại `TC-CHT-351` của kho.

**`[MAJOR] M6` `SEC-ISO-001` — toàn bộ 17 TC chạy trên MỘT friend duy nhất**
Chat 1:1 hiển thị nhiều hội thoại; bảng có cột `line_id` mà spec ghi *"NULL = cấu hình chung"* ⇒ tồn tại nhánh `line_id` khác NULL. Không TC nào mở friend thứ 2 để xác nhận cấu hình áp đúng phạm vi, cũng không TC nào chạm nhánh `line_id` per-friend.
→ **Đề xuất fix**: `TC-SECISO001-01` ở §5 + hỏi Dev endpoint này có bao giờ ghi `line_id` khác NULL không (§6).

**`[MAJOR] M7` `RULE-06` — `NEW-14` dừng ở dòng DB, không tới output cuối**
Expected của `NEW-14` chỉ tới *"bảng thời điểm gửi sự kiện có bản ghi được tạo mới hoặc cập nhật"*. Output cuối của nhánh này là **tin remind thật gửi tới LINE app** của friend.
→ **Đề xuất fix**: bổ sung bước + expected cho `NEW-14` (không đẻ TC mới): chờ tới mốc lịch → xác nhận tin nhận được trên LINE app thật, kèm screenshot.

**`[MAJOR] M8` `[AP-3]` — T2 (FA-015) chỉ được dùng làm tiền đề, không phải đối tượng regression**
`NEW-6` / `NEW-17` chỉ vào màn 「友だち情報管理」 để **xóa** 1 item, ở trạng thái dữ liệu sạch. Không TC nào verify FA-015 còn nguyên vẹn sau fix (list / tạo / sửa / bộ đếm `回答人数`). Dev cũng **để trống cột "Nguy cơ regression"** cho cả T1 và T2.
→ **Đề xuất fix**: yêu cầu Dev điền mức High/Medium/Low cho T1, T2; nếu T2 = High thì đây là `[BLOCKER]` theo `severity-levels.md`.

**`[MAJOR] M9` `[AP-4]` — không có link PR/diff để verify fix shape**
File 03 có commit `97033fb2cb` + branch `ai_fixbug_38944` nhưng không có link PR/diff đọc được. Không thể tự kiểm `msg` nằm ở **catch chung** hay ở **từng nhánh cụ thể**.
→ **Đề xuất fix**: yêu cầu Dev đính diff 1 dòng (`git show 97033fb2cb`) vào ticket.

**`[MAJOR] M10` — checkbox "Tester verify auto-fill chính xác" CHƯA tick ở cả `01` và `03`**
Cả 2 file có `Auto-filled: 2026-09-04 by /new-task` nhưng checkbox verify còn trống ⇒ F/D/T có thể thiếu hoặc map sai.
Cụ thể đã thấy 2 chỗ cần tester sửa: mục **4.2 mâu thuẫn mục 2** về transaction (xem cảnh báo đầu file 03), và **F2 sai file JS** (`M3`).
→ **Đề xuất fix**: tester đọc lại journal Redmine, sửa 2 điểm trên, rồi tick.

**`[MAJOR] M11` — kết quả Đạt hoàn toàn do pipeline AI tự chạy (0.6 #4 + #5)**
16/17 TC do AI sinh, 100% lượt exec `source = ai`, `reviewState` mới ở `leader`, `reviewed = false`. Không có lượt QA người chạy độc lập cho nhóm rủi ro cao (`NEW-4`, `NEW-8`, `NEW-9`).
→ **Đề xuất fix**: QA người chạy tay tối thiểu `NEW-4` (dialog tiếng Nhật) + `NEW-8` trên staging, đính evidence riêng.

**`[MAJOR] M12` `FRIEND-001` — thiếu ma trận kiểu friend info (MAP-FI-02)**
Danh sách hiển thị mới được test với kiểu **text** (`NEW-1`) và **date** (`NEW-3`). Còn thiếu **select / point / image / pdf**. Đáng chú ý: bug gốc ở ticket #40213 tái hiện bằng đúng mục kiểu **選択肢 (`type_data = 1`)** kèm `valueOption` — nhưng **không TC nào ghim kiểu này**.
→ **Đề xuất fix**: bổ sung `Dữ liệu test` của `NEW-8` để ghim đúng mục 選択肢 có `valueOption` như bước tái hiện của ticket (sửa TC, không đẻ TC mới).

**`[MAJOR] M13` — chưa đo phạm vi ghi dở dang ở bảng `event_step_time` (bổ sung vào `NEW-13`, KHÔNG viết TC mới)**
`saveSettingDisplayInfoV2` gọi `settingEventTimeFriendInfo` **bên trong vòng lặp**. Vì hàm không mở transaction (đã xác nhận qua `NEW-13` / `NEW-16`), khi exception rơi vào phần tử sau, mục kiểu 年月日 phía trước có thể **đã kịp ghi lịch gửi** trong khi dòng cấu hình hiển thị lại ở trạng thái không nhất quán ⇒ tin remind gửi cho một mục người vận hành không thấy trên tab.
⚠️ **Phạm vi**: đây **không** phải lỗi do bản fix gây ra và **không** phải cổng chặn của #40213 — code nhánh lịch không đổi 1 dòng nào. Nó chỉ **mở rộng phép đo** cho chính khiếm khuyết ghi dở dang mà human đã cố ý để ngoài phạm vi (`[BLOCKER] B3` + §6 mục 2), giúp Leader biết thiệt hại tới đâu trước khi chốt.
→ **Đề xuất fix** (rẻ, chạy được ngay trên môi trường đang có, **không** cần production, **không** cần chờ tới mốc remind): thêm 2 bước vào `NEW-13` — ghi lại số dòng `event_step_time` của friend kiểm thử **trước** khi gửi request lỗi, và đếm lại **sau**; đưa mục kiểu 年月日 vào danh sách gửi lên ở vị trí **trước** phần tử lỗi. Expected: chênh lệch = 0, hoặc ghi rõ số dòng dư thực tế để Leader quyết.

### 4.3 Minor (có thể fix sau)

- **`[MINOR] m1`** — `NEW-2` **mô tả sai thao tác UI**: bước 3 ghi *"đổi thứ tự ... bằng nút di chuyển lên/xuống trong modal"*, nhưng kết quả run #840 ghi rõ `MISMATCH testcase↔UI: modal không có nút di chuyển lên/xuống; thứ tự chỉ đổi được bằng kéo thả (draggable)`. Kho FA-001 `TC-CHT-351` cũng ghi kéo thả. → `testcase_update` sửa lại bước 3.
- **`[MINOR] m2`** — Toàn bộ 17 TC có `spec_status = null` ⇒ cột "Trạng thái đánh giá spec" trống. Với `NEW-5` / `NEW-13` / `NEW-16` (kỳ vọng lấy từ ticket, spec **không** quy định) phải là `Spec không ghi` + ghi rõ đã hỏi ai.
- **`[MINOR] m3`** — `NEW-16` `env_tag = read-only` nhưng steps của nó **tự chạy lại 2 kịch bản lỗi** (bằng chứng run #840: *"đã chạy: (a) mục tùy chỉnh thiếu value ... (b) phần tử lỗi ở cuối + idsDelete=[5896]"*) ⇒ nhãn `read-only` sai, TC này có ghi dữ liệu.
- **`[MINOR] m4`** — `NEW-17` có `requirement_keys = []` (TC human thêm sau, chưa gắn REQ). Nên gắn `REQ-003` + `REQ-009`.

### 4.4 Nit (gợi ý)

- **`[NIT] n1`** — `NEW-15` nằm ngoài diff của bản fix (endpoint khác). **Giữ lại** vì đã tìm ra lỗi thật; chỉ nên đổi nhãn thành *regression REG-SHARED-001* cho đúng bản chất (xem ORPHAN §3).
- **`[NIT] n2`** — §4 của `checklist-lme.md` (CHAT-01 — nhóm "chưa đủ bằng chứng") có liên quan màn chat 1:1, nhưng theo **RULE-11** chỉ nêu ở mức gợi ý, không dùng để chặn.
- **`[NIT] n3`** — `NEW-1` đặt tên field test là `TC40213_text_...` trong khi bước tái hiện của ticket dùng mục 選択肢; nên đổi tên fixture cho khớp ngữ cảnh bug (liên quan `M12`).

---

## 4.5 TC trùng lặp nội dung

Đã rà **toàn bộ 17 TC** theo 4 yếu tố (`mã quan điểm` × `loại case` × `đối tượng + thao tác` × `tiền đề tương đương`).

| Nhóm trùng | TC giữ lại | TC đề nghị xóa/gộp | Loại trùng | 4 yếu tố trùng nhau | Severity |
|---|---|---|---|---|---|
| Khẳng định "lưu thất bại không để lại bản ghi" | **`NEW-13`** (`TC-DATADB001-01`) — có ma trận dữ liệu giàu nhất (xóa A + tạo D + lỗi ở cuối), chấm được từng điểm | `NEW-16` (`TC-DATADB001-02`) — **GỘP, KHÔNG XÓA** | `DUP-SUBSET` (một phần) | Cùng `DATA-DB-001` · cùng đối tượng `setting_display_info_friend_chat11` · `NEW-16` **tự chạy lại đúng 2 kịch bản lỗi của `NEW-8` + `NEW-13`** rồi đếm lại ⇒ phần "tổng số bản ghi sau = trước" là **tập con** của assertion `NEW-13`. | `[MINOR]` |

**Gate trước khi đề nghị xóa** — đã chạy lại BƯỚC 2 + 3.6 trên tập giả định đã bỏ `NEW-16`: mất **duy nhất** chiều *"số bản ghi mồ côi không tăng"* (không TC nào khác đo). ⇒ **đổi đề xuất từ "xóa" sang "gộp"**: giữ `NEW-13`, chuyển bước đếm mồ côi của `NEW-16` thành 2 bước cuối của `NEW-13`.

**Đã kiểm và KHÔNG phải trùng** (ghi lại để lần review sau khỏi rà lại):
- `NEW-6` vs `NEW-17` — cùng `CONC-003` / cùng Abnormal / cùng kịch bản 2 tab, **nhưng khác nhánh code**: `NEW-6` mục đang ở 「表示中の項目」 (đi nhánh update), `NEW-17` mục đang ở 「非表示項目」 (đi nhánh `create()`). Tách đúng — và chính nhánh `create()` mới là nhánh **fail**.
- `NEW-4` vs `NEW-8` — cùng trigger nhưng **khác tầng quan sát** (dialog FE / body API). Cả 2 đều cần. *(Lưu ý: vì cùng trigger nên **không** được đếm là 2 trigger khi giải `B2`.)*
- `NEW-1` vs `NEW-3` — cùng `FUNC-001` / Normal nhưng khác **kiểu dữ liệu** field (text / date) và `NEW-3` kiểm thêm định dạng hiển thị ngày.
- `NEW-12` vs `NEW-2` — `NEW-2` kiểm bot đối chứng như 1 assertion phụ; `NEW-12` là **đối chứng âm** ở biên dưới (danh sách rỗng). Khác `loại case` (Normal / Boundary).
- `NEW-5` vs `NEW-13` vs `NEW-16` — `NEW-5` khác mã quan điểm (`OUT-TRUTH-001`) và khác tầng quan sát (tab + modal trên UI), không gộp với 2 TC còn lại.

---

## 5. TCs đề xuất bổ sung

> ✅ **Đã đối chiếu 17 TC ở BƯỚC 0 + [kho-tcs/fa001-chat11-11チャット.md](../../kho-tcs/fa001-chat11-11チャット.md) (nhóm "Rightbar — 友だち情報", 8 TC) + [kho-tcs/fa015-quanlythongtinbanbe-友だち情報管理.md](../../kho-tcs/fa015-quanlythongtinbanbe-友だち情報管理.md) — không TC đề xuất nào trùng.**
>
> **Dùng lại TC có sẵn trong kho, KHÔNG viết mới:**
> - `GAP CONC-001 (một phần)`: dùng lại **`TC-CHT-351`** — *"Sắp xếp và xoá mục thông tin đang hiển thị"* (đã có bước *"Double click nút xoá: chỉ tính 1 lần"*). Cần chỉnh: đổi đối tượng double-click từ **nút xoá** sang **nút 「内容を保存」**, và thêm kiểm số dòng trong bảng cấu hình sau thao tác.
> - `GAP STATE-CLEAN (đường hủy)`: dùng lại **`TC-CHT-350`** — *"Thêm mục nhưng đóng modal bằng X — không lưu"*. Chạy lại nguyên trạng làm regression cho bản fix (đường không-lưu không được sinh msg lỗi).
> - `GAP hội thoại NHÓM`: dùng lại **`TC-CHT-381`** — *"Nhóm — ẩn các mục không áp dụng ở cột phải"* (tab 「友だち情報」 bị ẩn với hội thoại nhóm). Cần chỉnh: thêm bước xác nhận **không** gọi được `saveSettingDisplayInfoV2` với hội thoại nhóm.
>
> ⚠️ Kho **chưa có** TC nào cho endpoint lưu cấu hình hiển thị ở tầng API ⇒ 5 TC dưới đây là mới hoàn toàn, không đụng kho.
> ⚠️ **Không phát hiện conflict expected** giữa TC đề xuất và TC kho.

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-FUNC004-02 | UI | FUNC-004 | Cấu hình mục hiển thị (Chat 1:1) | Boundary | manual | staging | Giá trị mục thông tin dài **đúng 500 ký tự** vẫn lưu được qua modal 「友だち情報の表示」 | - Đăng nhập admin, chọn bot A<br>- Bot A có mục thông tin bạn bè kiểu ký tự tên `TC40213_len`<br>- Friend F1 trong danh sách hội thoại | 1. Mở Chat 1:1 → chọn F1 → tab 「友だち情報」<br>2. Sửa nhanh giá trị mục `TC40213_len` thành chuỗi **đúng 500 ký tự** → lưu<br>3. Mở modal 「友だち情報の表示」<br>4. Bấm 「内容を保存」<br>5. Quan sát có hộp thoại nào bật lên không<br>6. Tải lại trang, mở lại tab 「友だち情報」 và đọc giá trị | Chuỗi 500 ký tự `a` (đếm bằng công cụ đếm ký tự trước khi dán) | - Không có hộp thoại lỗi nào bật lên<br>- Modal đóng lại bình thường<br>- Sau khi tải lại, mục `TC40213_len` vẫn hiển thị và giá trị đủ 500 ký tự, không bị cắt cụt | | Lấp GAP-B4 / cover impact D1 · Nguồn limit: `db-mapping.md` §3.17 `value varchar(500)` · Đánh giá spec: Spec ghi rõ (schema) · Evidence: screenshot tab + ảnh chụp giá trị sau reload |
| TC-FUNC004-03 | UI | FUNC-004 | Cấu hình mục hiển thị (Chat 1:1) | Boundary | manual | staging | Giá trị **501 ký tự** (vượt biên) phải hiện thông báo tiếng Nhật, không hiện 「undefined」, không trắng màn | - Như TC-FUNC004-02<br>- Đã ghi lại số mục đang hiển thị trên tab trước khi thao tác | 1. Mở Chat 1:1 → chọn F1 → tab 「友だち情報」, **ghi lại số mục đang hiển thị**<br>2. Sửa nhanh giá trị mục `TC40213_len` thành chuỗi **501 ký tự** → lưu<br>3. Mở modal 「友だち情報の表示」<br>4. Đưa thêm 1 mục bất kỳ từ 「非表示項目」 sang 「表示中の項目」<br>5. Bấm 「内容を保存」<br>6. Ghi lại **nguyên văn** nội dung hộp thoại bật lên<br>7. Tải lại trang, đếm lại số mục trên tab và trong 「表示中の項目」 | Chuỗi 501 ký tự `a` | - Nếu hệ thống chặn được: hộp thoại hiện đúng câu 「保存に失敗しました。入力内容をご確認ください。」<br>- **Tuyệt đối không** hiện 「undefined」, hộp thoại trống, màn trắng hay lỗi 500<br>- Ghi lại số mục sau khi tải lại so với bước 1 để đo mức ghi dở dang | | **Lấp GAP-B4 + là trigger MỚI cho GAP-B2** (lỗi khác `Undefined property`) · Nguồn limit: `varchar(500)` · Đánh giá spec: **Spec không ghi** (chưa quy định hành vi khi vượt biên) — đã ghi vào §6 để hỏi Dev · Evidence: screenshot hộp thoại + ảnh chụp số mục trước/sau |
| TC-FUNC002-01 | API | FUNC-002 | API lưu cấu hình hiển thị | Abnormal | auto | staging | Payload thiếu khóa **KHÁC** `value` cũng phải trả thông báo lỗi đọc được (chứng minh catch là catch-all) | - Có phiên đăng nhập admin + ngữ cảnh bot kiểm thử<br>- Đã ghi lại request mẫu do chính modal phát ra khi lưu thành công | 1. Lấy request mẫu đã ghi từ màn hình<br>2. Lượt 1: **bỏ hẳn khóa `id_setting`** của một phần tử, giữ nguyên mọi khóa khác → gửi<br>3. Lượt 2: đặt `id_setting` trỏ tới một mục **không tồn tại** (id chưa từng có) → gửi<br>4. Lượt 3: gửi `sortList` sai dạng (chuỗi thay vì đối tượng) → gửi<br>5. Mỗi lượt: đọc mã trạng thái + **nguyên văn** thân phản hồi | Lượt 1: bỏ khóa `id_setting` · Lượt 2: `id_setting` = 999999999 · Lượt 3: `sortList` = `"abc"` | Cả 3 lượt: mã trạng thái **200** (không 4xx/5xx), và **nếu** phản hồi có cờ thành công = false thì **bắt buộc** có trường thông báo đọc được, khác rỗng, khác chuỗi `undefined` — giống hệt hành vi đã đạt ở `NEW-8` | | **Lấp GAP-B2 (AP-1)** — đây là TC "trigger chưa biết trước" · cover impact BUG + F1 · Đánh giá spec: Spec không ghi (đã đưa vào §6) · Evidence: nguyên văn body của **cả 3** lượt |
| TC-CONC001-01 | UI | CONC-001 | Cấu hình mục hiển thị (Chat 1:1) | Abnormal | manual | staging | Bấm 「内容を保存」 đồng thời từ 2 tab — không được tạo dòng cấu hình trùng | - Đăng nhập admin, chọn bot A trên **2 tab trình duyệt cùng phiên**<br>- Cả 2 tab đang mở Chat 1:1 → cùng friend F1 → modal 「友だち情報の表示」<br>- Đã ghi lại danh sách mục đang hiển thị trước khi thao tác | 1. Tab 1 và Tab 2 cùng đưa **cùng một mục** từ 「非表示項目」 sang 「表示中の項目」<br>2. Bấm 「内容を保存」 ở Tab 1, rồi bấm ngay ở Tab 2 (trong vòng 1 giây, không chờ Tab 1 xong)<br>3. Quan sát hộp thoại ở cả 2 tab<br>4. Tải lại trang, mở lại tab 「友だち情報」 và modal, đếm số lần mục đó xuất hiện<br>5. Lặp lại bước 1–4 nhưng thay bằng **double-click nhanh** nút 「内容を保存」 trên 1 tab | Cùng 1 mục thông tin, 2 tab, khoảng cách bấm < 1 giây | - Mục đó xuất hiện **đúng 1 lần** trên tab 「友だち情報」 và **đúng 1 lần** trong 「表示中の項目」<br>- Không có mục nào bị nhân đôi trong danh sách<br>- Nếu có xung đột, hệ thống phải **báo lỗi rõ ràng**, không âm thầm ghi 2 lần | | Lấp GAP-M5 / cover impact D1 · Dẫn từ `TC-CHT-351` (kho FA-001, phần double-click) · Liên quan: hàm **không mở transaction** nên đây là rủi ro thật · Evidence: ảnh chụp danh sách mục sau thao tác (đếm được số lần xuất hiện) |
| TC-SECISO001-01 | UI | SEC-ISO-001 | Cấu hình mục hiển thị (Chat 1:1) | Abnormal | manual | staging | Đổi cấu hình hiển thị khi đang mở friend A — kiểm chéo trên friend B | - Đăng nhập admin, chọn bot A<br>- Bot A có **≥ 2 friend** trong danh sách hội thoại: F1 và F2<br>- Cả F1 và F2 đều có giá trị cho mục `TC40213_iso`<br>- Đã ghi lại danh sách mục hiển thị của **cả F1 và F2** trước khi thao tác | 1. Mở Chat 1:1 → chọn **F1** → tab 「友だち情報」, ghi lại danh sách mục<br>2. Chuyển sang **F2** → tab 「友だち情報」, ghi lại danh sách mục<br>3. Quay lại F1, mở modal 「友だち情報の表示」, thêm mục `TC40213_iso` → 「内容を保存」<br>4. Không tải lại trang, chuyển nhanh sang F2 rồi quay lại F1 vài lần<br>5. Đọc danh sách mục hiển thị của F1 và của F2<br>6. Tải lại trang và đọc lại cả 2 | 2 friend F1, F2 của cùng bot A; 1 mục `TC40213_iso` | - Ghi rõ hành vi quan sát: cấu hình sau khi lưu áp cho **cả bot** (mọi friend) hay chỉ cho F1<br>- Dù là hành vi nào, **F1 và F2 phải nhất quán** trước và sau khi tải lại trang<br>- Chuyển qua lại nhanh giữa F1 và F2 **không** được làm danh sách mục của friend này hiển thị nhầm sang friend kia | | Lấp GAP-M6 / cover impact D1 + T1 · Bảng có cột `line_id` (`db-mapping.md` §3.17: NULL = cấu hình chung) nhưng **chưa ai xác nhận endpoint có ghi `line_id` không** → §6 · Đánh giá spec: Spec không ghi · Evidence: screenshot tab của **cả 2 friend**, trước và sau |

---

## 6. Spec update needed

| # | Vấn đề | Nguồn | Đề nghị |
|---|---|---|---|
| **1** | **`api-spec.md` thiếu hẳn endpoint đang fix.** File liệt kê 49 EP cho màn Chat 1:1, có EP-19 (`setting-friend-display-modal-v3` — load modal) và EP-35 (`info_friend_display_chat11` — đọc cấu hình), **nhưng không có dòng nào cho `POST /ajax/saveSettingDisplayInfoV2`**. Studio cũng tự ghi nhận gap này (`coverage level = none`). | `spec-features/admin/chat-11/web/api-spec.md` · Studio `task_get_report.coverage` | Bổ sung EP cho `saveSettingDisplayInfoV2` **kèm hợp đồng phản hồi**: nhánh thành công `{success:true}` **không** có `msg`; nhánh thất bại `{success:false, msg:"保存に失敗しました。入力内容をご確認ください。"}` với **HTTP 200** (giữ 200 là chủ ý của Dev vì nhánh xử lý lỗi phía FE là no-op — bẫy đã ghi ở #40051). |
| **2** | **Không có chuẩn để chấm "lưu thất bại có được để lại dữ liệu dở dang không".** Ticket #40213 kỳ vọng **KHÔNG**; code hiện tại **CÓ** (đã đo được: 3 → 5 bản ghi ở `NEW-16`); human quyết định để ngoài phạm vi fix. 4 TC (`NEW-5`, `NEW-10`, `NEW-13`, `NEW-16`) đang treo ở trạng thái fail vì mang kỳ vọng cũ. | File 03 mục 2 + phần TỰ REVIEW · run #840 | Chốt thành **business rule** trong `feature-spec.md` (bổ sung cạnh BR-17): endpoint này **có / không** chạy trong transaction, và khi lỗi giữa chừng thì trạng thái dữ liệu hợp lệ là gì. Chưa chốt thì 4 TC trên không có chuẩn để chấm → gắn với `[BLOCKER] B3`. |
| **3** | **Mâu thuẫn trong chính file 03**: mục 4.2 ghi *"từ nay được hoàn tác bằng giao dịch"* trong khi mục 2 và phần TỰ REVIEW đều ghi *"KHÔNG bật lại giao dịch"*. Kết quả chạy thật bác bỏ câu ở 4.2. | `03-dev-impact.md` mục 2 vs 4.2 | Tester sửa lại 4.2 khi verify auto-fill (`[MAJOR] M10`). Không được viết TC với expected "dữ liệu được rollback" dựa vào câu sai này. |
| **4** | **Cột `line_id` chưa có mô tả hành vi.** `db-mapping.md` §3.17 chỉ ghi *"NULL = cấu hình chung"*, không nói khi nào non-NULL và ai ghi. Toàn bộ 17 TC chạy trên 1 friend nên nhánh này chưa từng được chạm. | `db-mapping.md` §3.17 · `[MAJOR] M6` | Hỏi Dev: `saveSettingDisplayInfoV2` có bao giờ ghi `line_id` khác NULL không? Nếu có → bổ sung BR + TC cho cấu hình theo từng friend. Nếu không → ghi rõ "luôn NULL, cấu hình theo bot" vào spec. |
| **5** | **Hành vi khi giá trị vượt `varchar(500)` chưa được quy định.** Không có validate ở FE lẫn BE theo mô tả của Dev; hành vi thực tế chưa ai đo. | `db-mapping.md` §3.17 · `TC-FUNC004-03` | Chốt: chặn ở FE, hay để BE trả msg lỗi, hay cắt cụt. Ghi vào cột Validation của `feature-spec.md`. |
| **6** | **Quyết định về bug #40493 (đã Reject) cần ghi lại lý do.** `NEW-15` chứng minh `POST /ajax/saveSettingDisplayInfoItem` vẫn trả `{"success":false}` **không kèm `msg`** ⇒ hộp thoại 「undefined」 **vẫn còn trên chính tab 「友だち情報」** — đúng triệu chứng mà #40213 đi fix, chỉ khác đường lưu. Ticket bị Reject với lý do *"Đồng bộ từ Redmine: Reject"*, không nêu lý do kỹ thuật. | Studio bug #836 → Redmine #40493 · `[NIT] n1` | Leader chốt và **ghi lý do vào ticket**: gộp vào #40213, hay tách ticket riêng cùng phần `isset` + transaction ở mục 2. Nếu để nguyên, người dùng vẫn gặp 「undefined」 qua đường sửa nhanh trên tab. |
| **7** | **Bug Studio #835 bị reject sau khi TC được sửa.** Lý do reject là *"chạy lại #872 đã pass"*, nhưng lượt pass đó chạy trên `NEW-6` **version 2** — kịch bản đã bị đổi từ "dựng dòng mồ côi ở tầng DB" sang "2 tab thật". Kịch bản gốc (dữ liệu mồ côi có sẵn của khách hàng) **chưa bao giờ pass**, và `NEW-17` sau đó tái hiện lại đúng triệu chứng đó. | Studio bug #835 · run #840, #860, #872, #877 | Xác nhận lại: dữ liệu mồ côi **cũ** (tạo trước khi `deleteItem` biết dọn kèm) có còn tồn tại trên production không? Nếu có → cần `RULE-04` (query thống kê **toàn hệ thống** xác nhận phạm vi) trước khi đóng. |

---

> **Ghi chú vận hành**: TC ở §5 dùng **14 cột** (12 cột format kho + `Chạy` + `Phạm vi ENV`) để đẩy thẳng sang Studio bằng `/sync-review-tc`. Nguồn bộ TC gốc là **Studio task #271** ⇒ `/sync-review-tc` sẽ gọi `testcase_create(task_id=271, rows)`; `client_ref` = `ID` nên chạy lại không tạo trùng.
> Quy đổi `Phạm vi ENV` → Studio `env_scope`: `staging` → `["staging"]` · `product` → `["prd"]` · `Tất cả` → `["dev","local","prd","staging"]`.
>
> ⚠️ **Cột `Nhóm` — 4 dòng đã ghi đè `GROUP_MAP`, đừng "sửa lại" theo tiền tố mã quan điểm.** `GROUP_MAP` ([kho-tcs/data/_common.py](../../kho-tcs/data/_common.py)) chỉ là **mặc định**; giá trị đúng là **tầng kiểm chứng thật** của TC, khớp `tc_group` của Studio. Chính bộ TC của task #271 chứng minh: `NEW-11` (`FUNC-004`) có `tc_group = api` và `NEW-13` (`DATA-DB-001`) có `tc_group = api` trong khi `NEW-16` (cùng `DATA-DB-001`) có `tc_group = data` — cùng mã quan điểm, khác tầng test thì khác nhóm.
>
> | TC | `GROUP_MAP` cho | Đã ghi đè thành | Lý do |
> |---|---|---|---|
> | `TC-FUNC002-01` | `UI` | **`API`** | `Chạy = auto`, không có bước UI nào — chỉ gửi request và đọc thân phản hồi |
> | `TC-CONC001-01` | `API` | **`UI`** | Thao tác tay trên 2 tab trình duyệt, quan sát danh sách mục trên màn |
> | `TC-SECISO001-01` | `API` | **`UI`** | Chuyển qua lại giữa 2 friend trên màn chat, đọc tab 「友だち情報」 |
>
> 2 dòng còn lại (`TC-FUNC004-02`, `TC-FUNC004-03`) trùng khớp `GROUP_MAP` nên giữ nguyên.
