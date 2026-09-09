# 05 — Review Report

> Draft cho Leader verify. Bug #38962 — *IDOR đọc: `getBroadcastLimitAlert` lấy broadcast theo id không scope bot [S5]*.

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | **(1) MCP LME TEST STUDIO — task `#242`** |
| Vì sao không dùng nguồn ưu tiên cao hơn | N.A. — đã dừng ở nguồn 1 (nguồn ưu tiên cao nhất) |
| Ticket · task_id · round · branch | `38962` · `#242` · round `1` · `ai_fixbug_38962` |
| Thời điểm fetch | `2026-09-03` (đầu session này, qua `task_list` → `testcase_list` → `task_get_context` → `task_get_report`) |
| Tổng số TC review | **16** |
| Snapshot đã ghi | `04-tc-list.md` — đã có header `<!-- source: MCP LME TEST STUDIO ... -->` từ `/new-task` cùng ngày, nội dung trùng khớp bản fetch ⇒ **không ghi đè lại** |
| Đối chiếu chéo nguồn | **KHÔNG** — đã dừng ở nguồn 1 |
| Tester được review | **AI pipeline** (Studio job `#750`) — 16/16 TC; QA `anhptn` là người **chạy**, không phải người viết |
| Vòng review | Round 1 (`reviewState = leader`, `reviewed = false`) |
| **Nguồn spec đã dùng** | ① [spec-features/admin/message-send-all/feature-spec.md](../../spec-features/admin/message-send-all/feature-spec.md) §5 **BR-04** (template_ids) · **BR-08** (Bot Switch Guard) · **BR-10** (giới hạn plan 1.000 tin/tháng gói free) · §6 API endpoints · §1 Actors<br>② [kho-tcs/fa008-broadcast-メッセージ配信.md](../../kho-tcs/fa008-broadcast-メッセージ配信.md) — **39 TC** của chính modal 配信数上限アラート (nhóm 28/29/30) + 10 TC nhóm *Phân quyền & môi trường* + 8 TC *Broadcast cũ & tương thích*<br>⚠️ **`feature-spec.md` KHÔNG có tính năng 配信数上限アラート** — kho ghi nhận ở mâu thuẫn **MT-20**: spec chốt 2026-03-26, ticket #36436 phát sinh sau, spec thiếu hẳn 1 màn (modal) + endpoint quota-check + business rule về cảnh báo quota ⇒ **không có spec chính thức** cho hành vi modal. Xem §6 SPEC-03. |

**Cảnh báo bắt buộc về chất lượng nguồn** — *Nguồn 1 (Studio)*:

| # | Chiều | Kết quả | Flag |
|---|---|---|---|
| 1 | Kết quả thực thi thật | **8/16 pass (50,0 %)** · 8 `skip` · 0 `fail` (trên staging) | `[MAJOR]` (dưới 80 %; đúng ngưỡng 50 %, chưa rơi vào BLOCKER của riêng mục này) |
| 2 | TC `fail`/`error` + ticket bug | Run auto **#621 (local)**: `fail` **1** (`#14442`) · `error` **1** (`#14445`). Bug Studio **`#729`** (`Medium`) sinh từ `#14442` → **`status = rejected`**, lý do *"luồng chung của tool"*, **`redmine_id = null`** ⇒ **fail chưa raise ticket Redmine** · `bug_tickets = []` ở cả 16 TC | **`[BLOCKER]`** — xem **B4** |
| 3 | Môi trường đã chạy | PROD **0** · STAGING **16** (chạy tay) · LOCAL **16** (auto run #621). Run auto `#822` trên staging = **`queued`, chưa từng chạy** | `[MAJOR]` RULE-08 / ENV-003 — xem **M10** |
| 4 | Ai chạy | 100 % `last_exec.source = manual`, `by = anhptn` (**QA người chạy**). Studio `envAuto` ghi `automated = 0` ở staging. `submittedWithoutMcp = false` | OK về mục "chỉ AI tự chạy" |
| 5 | Tác giả TC | **16/16 do AI sinh** (`provenance.source = ai`, `author = AI`, `created_job_id = 750`); `toolWritten: tool 16 / mcp 0 / human 0`; `reviewState = leader`, chưa `done` | `[MAJOR]` — xem **M15** |
| 6 | Mã quan điểm KHÔNG có trong `checklist-lme.md` | **4 mã / 7 lượt TC**: `API-CONTRACT-001` (2) · `TOOL-ERRHYG-001` (2) · `AUTH-SESSION-001` (2) · `TOOL-NEGCTRL-001` (1) | `[MAJOR]` — 7/16 TC không map được coverage, xem **M12** |

---

## 1. Verdict

> ### ❌ REJECTED
>
> 4 `[BLOCKER]`. Điểm cốt lõi: **một nửa bản vá (ràng buộc bot cho truy vấn mẫu tin con) hiện KHÔNG có một lần chạy nào chứng minh có hiệu lực**, và **nhánh lỗi 403 của bản vá đang có 2 expected mâu thuẫn nhau** giữa bộ TC Studio và kho TC chuẩn của tính năng.

---

## 2. Tóm tắt cho member

Bộ 16 TC của Studio **thiết kế tốt và bám đúng trục rủi ro**: có TC tái hiện đúng kịch bản khai thác IDOR, có TC chống enumeration (mã thật của bot khác và mã không tồn tại phải trả lời giống hệt nhau), có TC bảo vệ nhánh hợp lệ, và các `note` tự nhận diện được điểm yếu của chính mình (dataset của `TC-PERM003-02` v1 không đủ phân biệt fixed/buggy) — đây là chất lượng cao hơn mặt bằng.

**Vấn đề không nằm ở TC, mà nằm ở việc CHẠY.** 8/16 TC bị `skip` trên staging với lý do gọn `"skip api"` / `"skip DB"`, và 8 TC đó lại chính là toàn bộ tầng API + Data — trong đó có **TC duy nhất verify nửa sau của bản vá**. Cả 6 TC vừa được sửa (version 2) đều nằm trong nhóm bị skip, nên **không TC bản mới nào từng chạy**. Thêm nữa, một `fail` thật ở run local đã bị lượt `skip` trên staging ghi đè, và bug sinh ra từ nó đã bị reject mà chưa có ticket Redmine.

**Phải fix trước khi approve**: chạy lại 8 TC bị skip (ưu tiên `TC-PERM003-02` bản v2), chốt expected cho nhánh 403 (mâu thuẫn với kho `TC-BC-299`), xử lý bug `#729`, và bổ sung 5 TC ở §5.

---

## 3. Coverage Matrix

> `Exec` = số TC **`pass` trên staging** / tổng TC cover impact đó. TC `skip` **không** được tính là đã test.

| Impact | Loại | TC cover (suy luận) | # TC | Exec | Status |
|---|---|---|---|---|---|
| **BUG** — đọc `BroadCast` theo `id` client gửi, không ràng buộc `bot_id`; route ajax không có cổng quyền theo bot | Root cause | `TC-PERM003-01` · `TC-SEC001-01` · `TC-AUTHSESSION001-01` · `TC-TOOLERRHYG001-02` · `TC-APICONTRACT001-02` (nhánh hợp lệ) | 5 | **3/5** | **RISK** — 2 nhánh phiên (đổi bot · chưa chọn bot) đều `skip` |
| **F1** `getBroadcastLimitAlert` — validate mã > 0 · 1 truy vấn có `bot_id` · trả 403 | Direct | `TC-FUNC001-01` · `TC-OUTTRUTH001-01` · `TC-APICONTRACT001-02` · `TC-PERM003-01` · `TC-SEC001-01` · `TC-TOOLERRHYG001-01` · `TC-FUNC003-01` | 7 | **5/7** | **RISK** — toàn bộ nhánh *validate mã không hợp lệ* (`TOOLERRHYG001-01`, `FUNC003-01`) `skip` |
| **F2** truy vấn đếm **mẫu tin con** + ràng buộc bot | Direct | `TC-PERM003-02` (**skip**) · `TC-DATACOUNT001-01` (pass, **toàn mẫu tin cùng bot ⇒ không chạm ràng buộc**) · `TC-FUNC004-01` (pass, nhóm rỗng) | 3 | **0/1** *(chỉ 1 TC thật sự test ràng buộc)* | 🔴 **GAP** — xem **B1** |
| **F3** route ajax `check_login` + `check_remember_token`, không có cổng quyền theo bot | Indirect | `TC-AUTHSESSION001-02` (**skip** trên staging, **`fail` ở local**) | 1 | **0/1** | 🔴 **GAP** — xem **B4** |
| **F4** nhánh `.fail()` của `openAlertMessage` → gọi tiếp `registerBroadcast()` | Indirect | `TC-APICONTRACT001-01` (pass) | 1 | 1/1 | 🔴 **RISK — expected mâu thuẫn kho** `TC-BC-299`, xem **B2** |
| **F5** 2 đường vào modal (`confirmSaveBroadcast` · preview từ màn danh sách `index.js:1554`) | Indirect | `TC-FUNC001-01` (chỉ đường vào **tab 下書き → 編集**) | 1 | 1/1 | **GAP một nửa** — đường vào từ **màn danh sách** không có TC, xem **M7** |
| **D1** `broadcast.bot_id` — READ, điều kiện lọc mới | Data | `TC-PERM003-01` (pass) · `TC-DATADB001-01` (skip) | 2 | 1/2 | **RISK** |
| **D2** `template.bot_id` — READ, ràng buộc mẫu tin con | Data | `TC-PERM003-02` (skip) · `TC-TOOLNEGCTRL001-01` (skip) · `TC-DATADB001-01` (skip) | 3 | **0/3** | 🔴 **RISK — 100 % skip** |
| **D3** `broadcast.filter_number` · `broadcast.template_ids` — 2 field bị lộ trước fix | Data | `TC-PERM003-01` (pass — verify không lộ `777`, không lộ mã mẫu tin `7997484`) · `TC-SEC001-01` (pass) | 2 | 2/2 | **OK** |
| **T1** Broadcast (FA-008) — modal chỉ đọc tin gửi của bot đang đăng nhập | High | `TC-FUNC001-01` · `TC-OUTTRUTH001-01` · `TC-DATACOUNT001-01` · `TC-FUNC004-01` · `TC-APICONTRACT001-01` | 5 | 5/5 | **RISK** — tất cả tiền đề đều *data sạch, cùng bot*; không TC nào chạy với legacy/dirty data (**AP-3**) |
| **T2** Message Template (FA-010) — đếm mẫu tin giới hạn theo bot | Medium | `TC-PERM003-02` (skip) · `TC-DATACOUNT001-01` (pass, cùng bot) | 2 | 0/1 | 🔴 **GAP** (cùng gốc với F2) |
| **T3** Luồng đăng ký tin gửi hàng loạt 「この内容で配信登録」 | Medium | `TC-OUTTRUTH001-01` · `TC-APICONTRACT001-01` | 2 | 2/2 | **RISK** — phụ thuộc kết luận của **B2** |

**Tổng kết**: `OK` **1** · `RISK` **7** · `GAP` **4** trên 12 impact.

### ORPHAN TCs

| TC | Vì sao ORPHAN | Đề xuất |
|---|---|---|
| `TC-DATADB001-01` (`#14445`) | Kiểm schema `bot_id NOT NULL` + đếm bản ghi NULL. Đây là **tiền đề** của bản vá, không trace tới code path đã sửa (`AP-5` — layer-downstream). Run #621 chính nó cũng kết luận sai lệch phát hiện được là **lỗi dữ liệu môi trường**, không phải lỗi sản phẩm. | **Giữ** làm pre-check môi trường, nhưng **không tính là coverage** cho D1/D2. `[NIT]` |
| `TC-TOOLNEGCTRL001-01` (`#14446`) | Audit dữ liệu legacy lệch bot toàn hệ thống. Studio tự gắn `spec_status = impact-audit`, `priority = Low`, và note ghi rõ *"không blocking core fix"*. | **Giữ** làm impact audit, **không tính coverage**. `[NIT]` |

> ⚠️ 2 TC này chiếm 2/16 slot và làm D2 *trông như* có 3 TC cover, trong khi thực chất chỉ có **`TC-PERM003-02`** verify được ràng buộc bot. Đây là `DUP-INFLATE` ở tầng coverage — xem §4.5.

---

## 3.5 Fix-shape analysis (adversarial)

**Fix shape nhận diện** (từ mục 2 `03-dev-impact.md`): `"mã tin gửi phải là số dương"` + `"đọc bản ghi bằng MỘT truy vấn có ràng buộc bot"` + `"trả 403"` ⇒ khớp **row "validate input / add check / thêm if / kiểm tra điều kiện"**. Khớp thêm **row "số đếm / count / thống kê"** (今回の配信合計 · 超過 · 配信済み).

| Câu hỏi adversarial | Trả lời từ bộ TC | Kết luận |
|---|---|---|
| Validation cover bao nhiêu input variant? | **Thiết kế 14+**: `TC-TOOLERRHYG001-01` 10 giá trị (thiếu tham số / rỗng / 0 / −1 / `abc` / `1 OR 1=1` / `1' OR '1'='1` / `1;DROP TABLE broadcast` / khoảng trắng / `１` full-width) + `TC-FUNC003-01` 4 giá trị (`X.9` / `+X` / `1e3` / số cực lớn). **Đã chạy trên staging: 0.** | `[MAJOR]` — trigger space **thiết kế đủ** nhưng **thực thi = 0** |
| Có test **server-side** (gọi thẳng API) không? | Có — 9/16 TC là `tc_group = api`, gọi thẳng endpoint. Nhưng 6/9 bị `skip`. | `[MAJOR]` |
| Đủ 5 pattern biên (biên / biên±1 / 0 / rỗng)? | Với `broadcast_id`: có 0 / rỗng / âm. **Với quota** (biên thật sự của nghiệp vụ): chỉ có *vượt hẳn* (`TC-FUNC001-01`) và *dưới hẳn* (`TC-OUTTRUTH001-01`) — **thiếu đúng biên** (今回の配信合計 = đúng phần còn lại) và biên ±1. | `[MAJOR]` — xem **M4** |
| Đủ luồng vào (create / edit / **copy** / import / API)? | Chỉ **edit từ tab 下書き** + gọi thẳng API. **Thiếu**: preview từ **màn danh sách** (`index.js:1554` — Dev liệt kê ở mục 3), và luồng **copy** broadcast (BR-07 kho có 14 TC). | `[MAJOR]` — xem **M7** |
| Số đếm: đối chiếu **4 nguồn** (tóm tắt / chi tiết / CSV / API)? | Chỉ **2 nguồn** — modal UI (`TC-DATACOUNT001-01`) và API (`TC-APICONTRACT001-02`). **Thiếu** đối chiếu với **header 配信数 ở màn danh sách** (kho `TC-BC-296` làm đúng việc này). Mẫu số **friend đã block** không TC nào chạm (kho `TC-BC-321`). | `[MAJOR]` — xem **M5** |
| Phép tính tay có không? | **Có** — `TC-DATACOUNT001-01` bước 5, `TC-APICONTRACT001-02` bước 3, `TC-PERM003-02` bước 3-5 (100通 vs 200通). Đây là điểm mạnh của bộ TC. | ✅ OK |

### Trigger space — nhánh từ chối của bản vá

| Nhánh vào cổng 403 | TC thiết kế | Đã chạy staging |
|---|---|---|
| Mã thuộc bot khác (có thật) | `TC-PERM003-01` · `TC-SEC001-01` | ✅ 2 |
| Mã không tồn tại | `TC-SEC001-01` | ✅ 1 |
| Mã không hợp lệ (rỗng / 0 / âm / phi số / injection) | `TC-TOOLERRHYG001-01` | ❌ 0 |
| Mã sai định dạng số (`X.9` / `+X` / `1e3` / tràn) | `TC-FUNC003-01` | ❌ 0 |
| Phiên đã đăng nhập nhưng **chưa chọn bot** | `TC-TOOLERRHYG001-02` | ❌ 0 |
| Phiên **đổi sang bot khác** | `TC-AUTHSESSION001-01` | ❌ 0 |
| **Chưa đăng nhập / cookie hỏng** | `TC-AUTHSESSION001-02` | ❌ 0 (**`fail` ở local — HTTP 500**) |

⇒ **3/7 nhánh** được verify trên staging. Cổng 403 là **lớp bảo vệ duy nhất** của endpoint này (F3) ⇒ 4 nhánh chưa chạy là rủi ro trực tiếp.

### Symptom-only KH report

**KHÔNG áp dụng** (`AP-2` không dính). Ticket là tracker `Bug tự detect` — description nêu **chính xác** file : dòng, câu truy vấn thiếu `where('bot_id')`, và cơ chế khai thác. Không có triệu chứng mơ hồ nào cần suy ≥ 2 root cause.

### Anti-patterns

| AP | Dính? | Ghi chú |
|---|---|---|
| **AP-1** Single-trigger generic-fix | ❌ Không | Fix **cố ý gộp** 2 nhánh từ chối thành 1 phản hồi 403 để chống enumeration — và `TC-SEC001-01` khoá đúng tính chất đó (4 mã khác loại phải trả lời **giống hệt**). Trigger space thiết kế 14+, không phải single-trigger. |
| **AP-2** Symptom-only | ❌ Không | Xem trên. |
| **AP-3** Happy-path-only regression | ✅ **Dính** | T1/T2/T3 đều chỉ có TC với tiền đề *data sạch, mẫu tin cùng bot, broadcast tạo mới*. Không TC nào chạy regression ở **edge state**: broadcast tạo từ phiên bản cũ, dữ liệu lệch `bot_id`, mẫu tin nhóm lồng mẫu tin của bot khác (run #621 đã tìm thấy `grp#7990456(bot 1057) → con#7990465(bot 46225)` trong dữ liệu thật). → **M8** |
| **AP-4** Specific code-check disguised as generic | ✅ **Dính (một phần)** | Mục *Commit / Pull Request* **không có link PR** (chỉ có commit hash `4c2606f832`). Không đọc được diff ⇒ không verify được ràng buộc `bot_id` đã áp cho **cả** truy vấn broadcast **và** truy vấn mẫu tin con, hay chỉ áp cho cái đầu. → **M9** |
| **AP-5** Layer-downstream over-coverage | ✅ **Dính (nhẹ)** | 2 TC data-layer (`#14445`, `#14446`) test tầng DB/dữ liệu môi trường trong khi fix nằm ở Controller. Xem ORPHAN §3. → `[NIT]` |
| **AP-6** Mục 3 dev-impact trống | ❌ Không | Mục 3 liệt kê **đủ 7 mục** (function + route + 4 JS caller + helper mẫu). Đây là điểm tốt của file 03. |

---

## 3.6 Bảng quan điểm đối chiếu

> Quan điểm **đáng lẽ phải ◯** suy từ: root cause (IDOR đọc chéo bot) · cách fix (validate + ràng buộc `bot_id` + 403) · F1-F5 / D1-D3 / T1-T3 · loại feature (broadcast + quota gói cước, đa LINE OA).

| Mã quan điểm | Ưu tiên | Trigger khớp task? | TC cover | Exec | Kết luận |
|---|---|---|---|---|---|
| `FUNC-001` | Cao | ◯ mọi chức năng | `TC-FUNC001-01` | 1/1 | **OK** — luồng chính có TC chạy pass |
| `FUNC-003` | Trung bình | ◯ `broadcast_id` có định dạng quy định (số dương) | `TC-FUNC003-01` | **0/1** | **RISK** — skip |
| `FUNC-004` | **Cao** | ◯ giới hạn số lượng (quota tháng · công thức `ceil(n/5)`) | `TC-FUNC004-01` (biên 0 mẫu tin) | 1/1 | **RISK** — thiếu biên tại **đúng quota** và biên **5 mẫu tin** (`ceil(5/5)=1` vs `ceil(6/5)=2`) |
| `DATA-COUNT-001` | **Cao** | ◯ **BẮT BUỘC** — modal toàn số đếm | `TC-DATACOUNT001-01` · `TC-APICONTRACT001-02` | 2/2 | **RISK** — chỉ 2/4 nguồn; thiếu header màn danh sách + xử lý friend block |
| `DATA-DB-001` ★ | **Cao** | ◯ RULE-07 — kiểm `WHERE` scope trên 2 tài khoản | `TC-PERM003-02` (skip) · `TC-DATADB001-01` (skip, ORPHAN) | **0/2** | 🔴 **GAP** → **B1** |
| `PERM-002` | **Cao** | ◯ gọi thẳng API thao tác nhạy cảm (PII: số người nhận + danh sách mẫu tin) → phải 403 | *(không TC nào gắn mã)* — nội dung cover bởi `TC-PERM003-01` · `TC-SEC001-01` | 2/2 | **OK về nội dung** · `[MINOR]` thiếu mã liên kết. ⚠️ Nhưng chỉ cover **1 endpoint**; PERM-002 yêu cầu *"lập mapping màn hình × API endpoint"* → **B3** |
| `PERM-003` | **Cao** | ◯ **BẮT BUỘC** — tổ chức nhiều LINE OA + có change bot | `TC-PERM003-01` (pass) · `TC-PERM003-02` (skip) · `TC-AUTHSESSION001-01` (skip) | **1/3** | **RISK** — nhánh *change bot* (chính là **BR-08**) chưa chạy → **M3** |
| `SEC-001` | **Cao** | ◯ đổi ID sang tổ chức khác phải bị chặn | `TC-SEC001-01` | 1/1 | **OK** — chiều *file EXPORT* đánh **×**: endpoint này không sinh export (RULE-03 đã ghi lý do) |
| `SEC-ISO-001` | **Cao** | ◯ multi-session cùng user (2 tab), cross-account cùng trình duyệt | **KHÔNG TC nào** | 0 | **GAP** → **M3** / TC mới `TC-SECISO001-01` |
| `MSG-005` | **Cao** | ◯ **BẮT BUỘC** — chức năng tiêu thụ quota tin nhắn; modal hiển thị **tên gói thực tế** (`フリープラン`) | *(không TC nào gắn mã)* — `TC-FUNC001-01` (vượt) · `TC-OUTTRUTH001-01` (dưới) | 2/2 | **RISK** — thiếu `limit−1 / limit / limit+1`. Kho **đã có** `TC-BC-294` → **M4** |
| `OUT-TRUTH-001` | **Cao** | ◯ thao tác lưu/gửi có thông báo kết quả | `TC-OUTTRUTH001-01` | 1/1 | **RISK** — nhánh lỗi mâu thuẫn kho `TC-BC-299` → **B2** |
| `REG-SHARED-001` | **Cao** | ◯ *"fix bug có thể tồn tại ở chức năng tương tự"* — Dev **tự khai** còn nhiều chỗ cùng kiểu | **KHÔNG TC nào**; Dev **không cung cấp danh sách function** | 0 | 🔴 **GAP** → **B3** |
| `COMPAT-LEGACY-001` ★ | **Cao** | ◯ chạm **template** + broadcast **V2** (đối tượng đã version-up); RULE-09 | **KHÔNG TC nào**. Kho có `TC-BC-328`…`333` nhưng không TC nào chạm modal quota | 0 | **GAP** → **M6** |
| `ENV-003` ★ | **Cao** | ◯ modal đọc **gói cước + hạn mức tháng**; RULE-08 nhóm *bill tiền* | **KHÔNG TC nào chạy production** | 0 | **GAP** → **M10** |
| `PAY-LIMIT-001` | Cao | ◯ chức năng bị giới hạn theo gói (`フリープラン` 1.000 tin — BR-10) | `TC-FUNC001-01` · `TC-APICONTRACT001-02` (hiển thị nhãn gói) | 2/2 | **RISK** — chỉ test gói **free**; chưa test gói trả phí (`-1` = không giới hạn, card rút gọn — kho `TC-BC-293`) |
| `UI-003` | Trung bình → **Cao** (rủi ro *false success*) | ◯ 403 → không modal → vẫn đăng ký = người dùng **không biết** mình vừa đăng ký vượt quota | `TC-APICONTRACT001-01` | 1/1 | **RISK** — cùng gốc **B2** |
| `CONC-001` | Cao | **×** — fix chỉ READ, không đổi trạng thái, không có giới hạn dùng chung mới | — | — | × có lý do (RULE-03) |
| `MEDIA-*` · `INTG-*` · `JOB-001` · `LIFF-ENTRY-001` · `NOTI-MAIL-001` | Cao | **×** — endpoint không chạm media / webhook / job nền / URL LINE user / mail | — | — | × có lý do (RULE-03) |
| `DATA-MIG-001` · `DATA-BACKUP-001` | Cao | **×** — không đổi schema, không thêm bảng, không migration (4.2 = 0 data ghi) | — | — | × có lý do (RULE-03) |

**Quan điểm ưu tiên Cao KHÔNG có TC nào cover**: `SEC-ISO-001` · `REG-SHARED-001` · `COMPAT-LEGACY-001` · `ENV-003` — **4 quan điểm**.

> **RULE-01** (Cao → đủ Normal + Abnormal + Boundary): xét theo **từng mã quan điểm** thì 6/8 mã Cao đang có TC chỉ có 1 loại case. Tuy nhiên bộ TC phân bổ các chiều **sang mã quan điểm khác** (Normal ở `FUNC-001`, Abnormal ở `PERM-003`/`SEC-001`, Boundary ở `FUNC-004`/`FUNC-003`) và tổng thể đạt Normal **5** · Abnormal **9** · Boundary **2** — tỷ lệ **hợp lý cho task phân quyền/validation**. Vì vậy ghi **1 issue gộp mức `[MINOR]`** thay vì 6 `[MAJOR]` riêng lẻ. Xem **N1**.

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

**`[BLOCKER] B1` — `TC-PERM003-02` (Studio `#14443`): nửa sau của bản vá KHÔNG có lần chạy nào chứng minh có hiệu lực.**

- Bản vá gồm **2 ràng buộc bot**: (a) cho truy vấn `BroadCast`, (b) cho truy vấn **mẫu tin con** (`TemplateV2Controller.php:1088`, impact **F2** / **D2** / **T2**).
- `TC-PERM003-02` là **TC duy nhất** verify (b). Trên staging: **`skip`** (`"skip api"`, 09:42:59).
- Lần chạy duy nhất từng có là run auto **#621 ở bản v1**, và chính runner ghi nhận: *"với bộ dữ liệu này hai cách tính cho CÙNG kết quả (`ceil(2/5)=ceil(3/5)=1`), nên riêng con số không đủ phân biệt 'đã loại mẫu tin bot khác'"* ⇒ **`pass` đó không chứng minh được gì**.
- TC đã được sửa dataset thành **5 mẫu bot A + 1 mẫu bot B** (100通 nếu đúng vs 200通 nếu sai) lúc `2026-09-03 09:23:28` — **bản có khả năng bắt lỗi này chưa chạy lần nào, ở bất kỳ môi trường nào**.
- 2 TC còn lại của D2 (`TC-DATADB001-01`, `TC-TOOLNEGCTRL001-01`) đều là ORPHAN audit và đều `skip`.

→ **Fix**: chạy `TC-PERM003-02` **bản version 2** trên staging với đúng dataset 5+1, đính evidence (giá trị `今回の配信合計` thực tế + `bot_id` của 6 mẫu tin ở tầng dữ liệu). **Không viết TC mới** — TC đã tồn tại và đã đúng.

**`[BLOCKER] B2` — `TC-APICONTRACT001-01` (Studio `#14426`): expected MÂU THUẪN với kho TC chuẩn của tính năng.**

| | Kỳ vọng |
|---|---|
| **Studio `TC-APICONTRACT001-01`** | Endpoint trả 403 → *"lớp phủ đang tải biến mất; **KHÔNG** hiện modal cảnh báo; … Tin gửi **VẪN ĐƯỢC ĐĂNG KÝ** theo hành vi cũ"* |
| **Kho `TC-BC-299`** `[UI-003]` Abnormal | *"Lỗi mạng khi kiểm tra quota — **hiện lỗi rõ ràng, KHÔNG đăng ký nhầm**"* |

- 2 expected **loại trừ nhau** cho cùng tiền đề (endpoint quota-check không trả được số liệu) và cùng thao tác (bấm 「この内容で配信登録」).
- **Hệ quả nếu Studio đúng và kho sai**: kết hợp với **rủi ro Dev tự nêu** — *"nếu tồn tại dữ liệu cũ có tin gửi mang `bot_id` lệch … thì màn sẽ trả **403 thay vì hiện cảnh báo**"* — thì **chủ bot hợp lệ sẽ mất cảnh báo vượt quota một cách im lặng, và tin gửi vẫn được đăng ký**. Người dùng không hề biết mình vừa đăng ký một broadcast vượt hạn mức tháng. Đây chính là `UI-003` *false success*.
- **KHÔNG tự chọn bên.** Cần Leader/PO chốt (xem §6 SPEC-01). Cho tới khi chốt, **không được kết luận `Đạt`** cho `TC-APICONTRACT001-01`.

→ **Fix**: chốt contract nhánh lỗi, rồi sửa TC bên sai qua `testcase_update` trên Studio (hoặc sửa kho).

**`[BLOCKER] B3` — `REG-SHARED-001` / `PERM-002`: 2 endpoint còn lại của CHÍNH luồng xem trước chưa được dò cross-bot.**

- Dev khai ở mục 2: *"còn **nhiều chỗ cùng kiểu** đọc/ghi tin gửi theo mã thô ở `BroadcastV2Controller` / `BroadcastController` / `ChatController`, **chưa sửa** vì ngoài phạm vi ticket"* — nhưng **không liệt kê function nào**.
- Trong đó có 2 mục **Dev tự liệt kê ở mục 3** thuộc **cùng luồng, cùng màn hình** với endpoint vừa vá: `getDataPreview` (`modal-preview-draff-delivered.js:386`) và **preview từ màn danh sách** (`index.js:1554`).
- Mục tiêu ticket ở **T1** (risk **High**) là *"chặn dò mã tin của bot khác"*. Nếu 2 endpoint trên cũng đọc broadcast theo mã thô, thì **cùng một màn hình vẫn còn cửa để lấy dữ liệu bot khác** ⇒ mục tiêu T1 **không đạt** dù `TC-PERM003-01` pass.
- `PERM-002` yêu cầu rõ *"lập mapping màn hình × API endpoint"* — bộ TC hiện chỉ có mapping cho **1 endpoint**.

→ **Fix**: (1) yêu cầu Dev liệt kê **tên function cụ thể** cho phần quét ngang; (2) thêm `TC-PERM002-01` ở §5 để dò 2 endpoint cùng luồng. Phần quét ngang **rộng** (toàn bộ `BroadcastV2Controller` / `BroadcastController` / `ChatController`) **KHÔNG** đưa vào bộ TC của ticket này — đó là **ticket riêng**, xem §6 SPEC-06.

**`[BLOCKER] B4` — `TC-AUTHSESSION001-02` (Studio `#14442`): `fail` thật bị `skip` ghi đè, bug đã reject và CHƯA có ticket Redmine.**

- Run auto **#621 (local)**: gọi endpoint nhóm `/ajax` **không cookie** → **HTTP 500**; **cookie hỏng** → **HTTP 500**, thân phản hồi lộ `Illuminate\`, `/workspace/source/sns-line/`, `vendor/laravel/…` (`ErrorException: Trying to get property 'headers' of non-object` tại `VerifyCsrfToken.php:159`).
- Root cause: `App\Http\Middleware\CheckLogin` chỉ có nhánh `if (Auth::check())`, **không trả response nào** khi chưa đăng nhập ⇒ **áp dụng cho MỌI route nhóm prefix `/ajax`**, không riêng endpoint của #38962.
- Bug Studio **`#729`** (`Medium`) → **`status = rejected`**, `reject_reason = "luồng chung của tool"`, **`redmine_id = null`**.
- Lượt chạy tay trên staging **`skip`** TC này (09:45:11, `"skip api"`) ⇒ trong `testcase_list`, `last_exec.status` hiện là `skip`, **`fail` biến mất khỏi tầm nhìn**. Nếu Leader chỉ đọc `testcase_list` sẽ thấy *"0 fail"*.
- Kho **đã có** quan điểm tương ứng: `TC-BC-340` `[SEC-002]` *"Gọi API broadcast khi chưa đăng nhập — bị chặn"*.

→ **Fix**: (1) chạy lại `TC-AUTHSESSION001-02` trên staging (không được `skip`) để xác nhận 500 còn tái hiện ngoài local; (2) **mở ticket Redmine riêng** cho middleware `CheckLogin` — reject vì *"luồng chung của tool"* là lý do để **tách ticket**, không phải để **đóng vấn đề**. Xem §6 SPEC-07.

### 4.2 Major (nên fix)

| # | Issue | Đề xuất fix |
|---|---|---|
| **M1** | **Evidence rỗng 100 %** — cả 8 TC `Đạt` trên staging đều có `evidence: []` và `actual = null`. Vi phạm **RULE-02**. Nghịch lý: run auto #621 ở local **có** screenshot (`621/tc-14423/modal.png`, …) còn lượt chạy tay quyết định thì không có gì. | Chạy lại kèm evidence đúng loại: screenshot modal + giá trị số + kết quả ở tầng dữ liệu. Không tick Đạt nếu thiếu. |
| **M2** | **6 TC `version 2` chưa từng chạy ở bản đã sửa** (`#14439` `#14442` `#14443` `#14444` `#14445` `#14446`, sửa 09:23–09:24, chạy tay 09:35–09:45 → **skip toàn bộ**). Sửa TC xong không chạy = sửa vô nghĩa. | Chạy đủ 6 TC bản v2. |
| **M3** | `PERM-003` / `SEC-ISO-001` — nhánh **change bot** (`TC-AUTHSESSION001-01`) `skip`; **không TC nào** cho kịch bản **2 tab đồng thời** (spec **BR-08** Bot Switch Guard tồn tại chính vì kịch bản này). | Chạy `TC-AUTHSESSION001-01`; thêm `TC-SECISO001-01` (§5). |
| **M4** | `MSG-005` — thiếu biên quota `limit−1 / limit / limit+1`; chỉ có *vượt hẳn* và *dưới hẳn*. `MSG-005` còn yêu cầu **cảnh báo ghi đúng tên plan thực tế** (đã từng có bug hiện sai tên plan Lite/Standard). | **Dùng lại kho `TC-BC-294`** *"Ranh giới quota — bằng đúng giới hạn, vượt 1 tin, thiếu 1 tin"* — không viết TC mới. |
| **M5** | `DATA-COUNT-001` — chỉ đối chiếu **2/4 nguồn** (modal + API). Thiếu **header 配信数 màn danh sách**; thiếu xử lý **friend đã block** ở mẫu số. | **Dùng lại kho `TC-BC-296`** (khớp công thức + header danh sách), **`TC-BC-297`** (配信対象 khớp filter thực tế), **`TC-BC-321`** (friend block). |
| **M6** | `COMPAT-LEGACY-001` — bản vá thêm ràng buộc `bot_id` vào truy vấn **template**, trong khi broadcast/template là đối tượng **đã version-up (V1 → V2)**. Không TC nào chạy modal với **broadcast tạo từ phiên bản cũ**. RULE-09. | Thêm `TC-COMPATLEGACY001-01` (§5), dẫn từ kho `TC-BC-330` / `TC-BC-332`. |
| **M7** | **F5** — modal có **2 đường vào** (Dev liệt kê ở mục 3), TC chỉ đi đường **tab 下書き → 編集**. Đường vào **preview từ màn danh sách** (`index.js:1554`) không có TC. | Thêm `TC-FUNC001-02` (§5). |
| **M8** | **`AP-3`** happy-path-only regression — T1/T2/T3 chỉ có tiền đề *data sạch, mẫu tin cùng bot*. Run #621 đã tìm thấy trong dữ liệu thật **1 mẫu tin nhóm chứa mẫu tin con của bot khác** (`grp#7990456(bot 1057) → con#7990465(bot 46225)`) — chưa TC nào chạy với trạng thái đó. | Bổ sung tiền đề edge-state vào TC regression; chạy `TC-TOOLNEGCTRL001-01` trên staging/production để biết dữ liệu thật có lệch bot không. |
| **M9** | **`AP-4`** — mục *Commit / Pull Request* **không có link PR**, chỉ có commit hash. Không đọc được diff ⇒ **không verify được** ràng buộc `bot_id` đã áp cho **cả 2** truy vấn (broadcast **và** mẫu tin con) hay chỉ truy vấn đầu. Đây đúng là điểm **B1** đang bỏ ngỏ. | Yêu cầu Dev cung cấp link PR / diff của `4c2606f832`. |
| **M10** | `ENV-003` / **RULE-08** — **0 TC chạy production**. Modal đọc **gói cước + hạn mức tháng + nhãn plan + nút nâng cấp** ⇒ thuộc nhóm *bill tiền*; staging dùng account test, production dùng **account thật với gói thật**. Thêm nữa, rủi ro số 1 của bản vá là **chặn nhầm chủ bot hợp lệ** — chưa được kiểm trên dữ liệu thật. | Thêm `TC-ENV003-01` (§5) — smoke **chỉ đọc**, không tạo/xoá dữ liệu thật. Kho có `TC-BC-341` cùng hướng. |
| **M11** | **FIX-SHAPE validate input** — 14+ input variant được thiết kế nhưng **0 variant nào chạy trên staging**; chỉ 3/7 nhánh vào cổng 403 được verify (xem bảng §3.5). | Chạy `TC-TOOLERRHYG001-01` + `TC-FUNC003-01` + `TC-TOOLERRHYG001-02`. |
| **M12** | **4 mã quan điểm ngoài `checklist-lme.md`** (`API-CONTRACT-001` · `TOOL-ERRHYG-001` · `AUTH-SESSION-001` · `TOOL-NEGCTRL-001`) phủ **7/16 TC** ⇒ coverage của 7 TC này **không map được** vào bảng quan điểm chuẩn. | Map lại sang mã chuẩn: `API-CONTRACT-001` → `OUT-TRUTH-001` / `UI-003`; `TOOL-ERRHYG-001` → `FUNC-002` / `SEC-002`; `AUTH-SESSION-001` → `PERM-003` / `SEC-002`; `TOOL-NEGCTRL-001` → `DATA-DB-001`. Hoặc Leader duyệt bổ sung mã mới vào tầng 1 (**RULE-10**). |
| **M13** | **Khai báo môi trường sai thực tế**: `env_tag = local-only` ở 14/16 TC nhưng chạy trên **staging**; `exec_mode = auto` ở **16/16** nhưng lượt chạy quyết định là **tay 100 %** (`envAuto.automated = 0` ở staging). | Sửa `env_tag` / `exec_mode` trên Studio cho khớp thực tế, nếu không mọi thống kê tự động đều sai. |
| **M14** | **Checkbox "Tester verify auto-fill chính xác" CHƯA tick** ở **cả `01-bug-task.md` và `03-dev-impact.md`** (đều có `Auto-filled: 2026-09-03 by /new-task`). F/D/T có thể thiếu hoặc map sai. | Tester đọc lại Redmine #38962 + journal `133115` rồi tick 2 checkbox. |
| **M15** | **16/16 TC do AI sinh**, `reviewState = leader`, `reviewed = false`, `status` của cả 16 TC vẫn là `draft`. Chưa có người nào duyệt nội dung TC. | Leader duyệt và chuyển `reviewState`; đổi `status` khỏi `draft` sau khi duyệt. |

### 4.3 Minor (có thể fix sau)

| # | Issue | Đề xuất |
|---|---|---|
| **N1** | **RULE-01 theo từng mã quan điểm**: 6/8 mã Cao đang có TC chỉ mang 1 loại case (`FUNC-001` chỉ Normal, `DATA-COUNT-001` chỉ Normal, `SEC-001` chỉ Abnormal, …). Tổng thể bộ TC vẫn cân (Normal 5 · Abnormal 9 · Boundary 2, hợp lý cho task phân quyền). | Ghi lý do vào `Ghi chú` của các TC đó ("chiều còn lại cover ở mã `<X>`") thay vì đẻ thêm TC. |
| **N2** | `PERM-002` — quan điểm **đúng trọng tâm nhất** của bug (bypass quyền bằng API trực tiếp) nhưng **không TC nào gắn mã này**. | Gắn `PERM-002` làm mã phụ cho `TC-PERM003-01` / `TC-SEC001-01`. |
| **N3** | `spec_status` dùng **giá trị ngoài enum canonical**: `needs-human-review` (`#14439`, `#14444`) · `impact-audit` (`#14446`). Enum chuẩn chỉ có `Spec ghi rõ` / `Spec không ghi` / `Đã hỏi leader`. | Quy về enum chuẩn (`Spec không ghi` + ghi rõ đã hỏi ai), giữ giá trị Studio ở `Ghi chú`. |
| **N4** | 13/16 TC có `spec_status = null` ⇒ cột *Trạng thái đánh giá spec* trống. Vì spec chính thức **không có** modal này (MT-20), đáng lẽ phải là `Spec không ghi`. | Điền `Spec không ghi` + tên người đã hỏi. |

### 4.4 Nit (gợi ý)

- **`[NIT]` ORPHAN** — `TC-DATADB001-01` · `TC-TOOLNEGCTRL001-01`: giữ làm pre-check / impact audit môi trường, nhưng **không tính vào coverage** của D1/D2 (xem §3). Studio tự gắn `priority = Low` + `impact-audit`, đúng hướng.
- **`[NIT]` Nhãn coverage lệch spec** — `task_get_report.coverage` của Studio ghi ref **`BR-09`** với note *"bot-switch guard"* và `level = none`. Trong [feature-spec.md](../../spec-features/admin/message-send-all/feature-spec.md) §5 thì **`BR-08`** mới là *Bot Switch Guard*, còn `BR-09` là *URL tracking trong text message*. Studio có thể đang dùng bản spec khác — cần thống nhất mã BR để coverage đối chiếu được.
- **`[NIT]`** Coverage tổng của Studio: **23 ref · `covered = 0` · `partial = 22` · `none = 1`** — **không ref nào đạt `covered`**. Con số này tự nó đã nói bộ TC chưa đủ độ phủ theo đánh giá của chính Studio.
- **`[NIT]`** Description Redmine ghi `TemplateV2Controller.php:1051`, journal ghi `:1056` — lệch 5 dòng (đã ghi ở `03-dev-impact.md` `BUG-GAP-04`).

---

## 4.5 TC trùng lặp nội dung

> Đã rà **toàn bộ 16 TC** theo 4 yếu tố (`mã quan điểm` × `loại case` × `đối tượng + thao tác` × `tiền đề tương đương` → `expected` tương đương).

**Kết luận: KHÔNG có cặp TC nào cần xóa hoặc gộp.** Chi tiết các cặp có chồng lấn một phần:

| Cặp | Chồng lấn | Vì sao **KHÔNG** phải trùng | Xử lý |
|---|---|---|---|
| `TC-PERM003-01` ↔ `TC-SEC001-01` | Cùng *gọi endpoint với mã ngoài bot → 403*, cùng Abnormal | Verify **2 tính chất khác nhau**: `PERM003-01` = *không lộ giá trị cụ thể* (777, mã mẫu tin) + dữ liệu bot B không đổi; `SEC001-01` = *4 mã khác loại phải trả lời **giống hệt nhau*** (chống enumeration). Xóa 1 cái là mất 1 tính chất. | **Giữ cả 2** |
| `TC-FUNC001-01` ↔ `TC-APICONTRACT001-02` | Cùng kịch bản vượt quota của chính bot, cùng bộ số | **Khác tầng có chủ đích**: UI trên browser thật vs hợp đồng JSON của endpoint. Studio ghi rõ ý đồ này ở `note`. RULE-07 cũng yêu cầu khớp cả 2 tầng. | **Giữ cả 2** |
| `TC-TOOLERRHYG001-01` ↔ `TC-FUNC003-01` | Cùng *input `broadcast_id` xấu → 4xx sạch, không 500* | **Khác lớp input**: `TOOLERRHYG001-01` = rỗng/0/âm/phi số/injection (Abnormal); `FUNC003-01` = định dạng số không chuẩn `X.9` `+X` `1e3` tràn số (Boundary). Bổ sung nhau. | **Giữ cả 2** |
| `TC-TOOLERRHYG001-02` ↔ `TC-AUTHSESSION001-02` | Cùng *phiên không hợp lệ → không đọc được dữ liệu* | Khác trạng thái phiên: *đã đăng nhập nhưng chưa chọn bot* vs *chưa đăng nhập / cookie hỏng*. `note` của `#14441` **cấm** thay thế cho nhau. | **Giữ cả 2** |
| `TC-DATADB001-01` ↔ `TC-TOOLNEGCTRL001-01` | Cùng là truy vấn đọc DB, cùng `read-only`, cùng `priority = Low` | Khác đối tượng: schema `NOT NULL` + đếm NULL vs rà lệch bot broadcast↔template. | **Giữ cả 2** — nhưng cả 2 là **ORPHAN**, xem §3 |

⚠️ **`DUP-INFLATE` ở tầng coverage (không phải trùng TC)**: impact **D2** *trông như* có **3 TC** cover, nhưng 2 trong đó là ORPHAN audit môi trường ⇒ số TC thật sự verify ràng buộc bot cho mẫu tin con là **1** (`TC-PERM003-02`) và nó đang `skip`. Đã hạ **D2** và **F2** xuống `GAP`/`RISK` ở §3 — đây là nguồn gốc của **B1**.

---

## 5. TCs đề xuất bổ sung

> **Đã đối chiếu `16` TC ở BƯỚC 0 + [kho-tcs/fa008-broadcast-メッセージ配信.md](../../kho-tcs/fa008-broadcast-メッセージ配信.md) (39 TC nhóm 配信数上限アラート · 10 TC Phân quyền & môi trường · 8 TC Broadcast cũ & tương thích) — không TC đề xuất nào trùng.**

**GAP xử lý KHÔNG bằng TC mới** (theo §5a — kho đã có, hoặc TC đã tồn tại, hoặc đang conflict):

| GAP | Xử lý | Lý do |
|---|---|---|
| **GAP-1** — F2/D2 ràng buộc bot cho mẫu tin con | **Chạy `TC-PERM003-02` bản v2**, không viết TC mới | TC đã tồn tại và dataset đã đúng — vấn đề là bị `skip` (**B1**) |
| **GAP-3** — nhánh 403 với chủ bot hợp lệ + dữ liệu lệch bot | **KHÔNG viết TC** — đẩy §6 SPEC-01 | Expected đang mâu thuẫn (**B2**); viết TC lúc này = tự chọn bên |
| **GAP-4** — biên quota `limit−1 / limit / limit+1` | **Dùng lại kho `TC-BC-294`** — *"Ranh giới quota — bằng đúng giới hạn, vượt 1 tin, thiếu 1 tin"* | Kho đã cover đúng; chỉ cần thêm tiền đề *"mẫu tin đều thuộc bot đang chọn"* cho hợp bug này |
| **GAP-5** — DATA-COUNT-001 đối chiếu 4 nguồn | **Dùng lại kho `TC-BC-296`** (công thức + header màn danh sách) · **`TC-BC-297`** (配信対象 khớp filter) · **`TC-BC-321`** (friend đã block) | Kho đã cover; không đẻ TC trùng |
| **GAP-10** — quét ngang `BroadcastV2Controller` / `BroadcastController` / `ChatController` | **KHÔNG đưa vào bộ TC ticket này** → §6 SPEC-06 (ticket riêng) | Các endpoint đó **chưa được fix** và **ngoài phạm vi ticket**; viết TC ở đây sẽ fail theo thiết kế, không phải regression của bản vá |

**5 TC mới** (14 cột):

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-PERM002-01 | API | PERM-002 | 配信数上限アラート — trigger & modal | Abnormal | manual | staging | Dò 2 đường lấy dữ liệu còn lại của cùng luồng xem trước bằng mã tin gửi của bot khác — cùng phải bị từ chối | - Hai bot thuộc hai tài khoản khác nhau: bot A (tài khoản đăng nhập) và bot B (tài khoản khác)<br>- Bot B có tin gửi hàng loạt 「TC38962_B_SECRET2」 đã lưu, số người nhận biết trước và danh sách mẫu tin biết trước<br>- Đăng nhập tài khoản bot A, đã chọn bot A ở màn chọn bot<br>- Mở tab Network của trình duyệt để ghi lại các yêu cầu mà màn xem trước gửi đi | 1. Ở bot A, mở màn 一斉配信, tab 下書き, bấm 編集 một tin gửi bất kỳ<br>2. Bấm nút xác nhận nội dung để mở hộp xem trước 配信内容, rồi bấm 「この内容で配信登録」<br>3. Trong tab Network, ghi lại **toàn bộ** yêu cầu mà 2 bước trên gửi đi kèm tham số mã tin gửi (ngoài yêu cầu lấy số liệu cảnh báo đã được vá)<br>4. Quay lại màn danh sách 一斉配信 của bot A, bấm xem trước trên một dòng, ghi lại các yêu cầu có tham số mã tin gửi<br>5. Với **từng** yêu cầu ghi được ở bước 3 và 4, gửi lại yêu cầu đó nhưng thay mã tin gửi bằng mã của 「TC38962_B_SECRET2」 (bot B), vẫn dùng phiên đang chọn bot A<br>6. Với từng phản hồi, ghi lại mã trạng thái HTTP và rà xem có chứa số người nhận, mã mẫu tin, hay nội dung tin gửi của bot B không<br>7. Đối chiếu ở tầng dữ liệu: tin gửi của bot B không bị thay đổi | Mã tin gửi của bot B thay vào tham số của từng yêu cầu ghi được ở bước 3-4; phiên đăng nhập chỉ có quyền trên bot A | Mọi yêu cầu bị thay mã đều **không trả về bất kỳ dữ liệu nào của bot B**: không có số người nhận, không có mã hay nội dung mẫu tin, không có nội dung tin gửi. Yêu cầu bị chặn bằng lỗi 4xx (403 hoặc tương đương). Nếu **bất kỳ** yêu cầu nào trả HTTP 200 kèm dữ liệu của bot B thì mục tiêu của ticket #38962 (chặn dò mã tin của bot khác trên màn này) **CHƯA đạt** — ghi lại tên đường dẫn của yêu cầu đó và báo Leader ngay. Dữ liệu tin gửi của bot B ở tầng dữ liệu không đổi. | | Lấp GAP-2 / cover impact F5 · liên quan BLOCKER B3 · Đánh giá spec: Spec không ghi (đã hỏi Dev qua BUG-GAP-01 ở file 03) · Evidence: bảng liệt kê từng đường dẫn yêu cầu + mã trạng thái + trích thân phản hồi · dẫn từ TC-BC-339 (kho) · ⚠️ Nếu phát hiện đường rò, **không sửa trong ticket này** — mở ticket riêng theo §6 SPEC-06 |
| TC-FUNC001-02 | UI | FUNC-001 | 配信数上限アラート — trigger & modal | Normal | manual | staging | Mở modal cảnh báo từ đường vào thứ hai (xem trước ở màn danh sách) — số liệu đúng của chính bot, không bị 403 | - Đăng nhập chủ bot A, đã chọn bot A<br>- Bot A có hạn mức 「LINE公式アカウント」 = 5.000, đã gửi 4.900<br>- Bot A ở gói エルメ 「フリープラン」, đã gửi 950<br>- Bot A có tin gửi hàng loạt 「TC38962_ENTRY2」 đã lưu, gồm 2 mẫu tin thường **đều thuộc bot A**, 配信対象 = 200 người<br>- Tin gửi này hiển thị được ở màn danh sách 一斉配信 | 1. Mở màn danh sách 一斉配信 của bot A (**không** vào màn tạo/sửa)<br>2. Trên dòng 「TC38962_ENTRY2」, bấm nút xem trước ngay tại màn danh sách<br>3. Trong hộp xem trước, bấm nút 「この内容で配信登録」<br>4. Đọc trên modal: dòng tóm tắt 配信対象 và từng con số trên hai thẻ dịch vụ<br>5. So sánh từng con số với kết quả khi mở cùng tin gửi đó theo đường 下書き → 編集<br>6. Kiểm tra bảng điều khiển trình duyệt không có lỗi JavaScript và không có yêu cầu nào trả 403 | 配信対象 = 200 người; 2 mẫu tin thường; hạn mức LINE 5.000 / đã gửi 4.900; エルメ フリープラン / đã gửi 950. Phép tính tay: 2 mẫu tin ⇒ làm tròn lên 2/5 = 1 lượt × 200 người = 200通; 超過 LINE = 200 − 100 = 100通; 超過 エルメ = 200 − 50 = 150通 | Modal 「配信数が月間上限を超える可能性があります」 hiện lên **y hệt** đường vào 下書き → 編集: 配信対象 「200人」, 今回の配信合計 200通 ở cả hai thẻ, thẻ 「LINE公式アカウント」 超過 100通, thẻ 「エルメ」 có nhãn 「フリープラン」 và 超過 150通. **KHÔNG** có yêu cầu nào trả 403 — chủ bot hợp lệ không bị cổng quyền mới chặn ở đường vào này. Không có lỗi JavaScript. | | Lấp GAP-9 / cover impact F5 (đường vào `index.js:1554` Dev liệt kê ở mục 3) · regression · Đánh giá spec: Spec không ghi (modal không có trong feature-spec.md — xem §6 SPEC-03) · Evidence: screenshot modal của **cả 2 đường vào** đặt cạnh nhau + ảnh tab Network không có 403 |
| TC-SECISO001-01 | API | SEC-ISO-001 | Phân quyền & môi trường | Abnormal | manual | staging | Hai tab cùng phiên, tab B đổi sang bot khác — tab A đang mở dở màn tạo tin gửi bấm đăng ký thì không đọc được dữ liệu bot cũ | - Một tài khoản quản trị có quyền trên **cả hai** bot A và bot B<br>- Bot A có tin gửi nháp 「TC38962_2TAB」 đã lưu, 配信対象 = 200 người, 2 mẫu tin thường của bot A, hạn mức bot A đặt sao cho chắc chắn vượt (LINE: 5.000 / đã gửi 4.900)<br>- Ghi lại 配信対象 của tin gửi này ở tầng dữ liệu<br>- Dùng **cùng một trình duyệt, cùng một phiên đăng nhập** cho cả 2 tab | 1. Tab A: mở màn 一斉配信 của bot A, tab 下書き, bấm 編集 trên 「TC38962_2TAB」, để nguyên màn tạo/sửa (**chưa bấm gì thêm**)<br>2. Tab B: mở màn chọn bot của cùng phiên, chuyển sang **bot B**<br>3. Quay lại tab A (**không F5**), bấm nút xác nhận nội dung để mở hộp xem trước, rồi bấm 「この内容で配信登録」<br>4. Quan sát tab A: có modal cảnh báo không, có thông báo lỗi gì, lớp phủ đang tải có biến mất không, có lỗi JavaScript không<br>5. Ghi lại mã trạng thái HTTP của yêu cầu lấy số liệu cảnh báo và toàn bộ thân phản hồi<br>6. Đối chiếu ở tầng dữ liệu: trạng thái của tin gửi 「TC38962_2TAB」 sau thao tác | Cùng một phiên; tab A giữ màn tạo/sửa tin gửi của bot A; tab B đã chuyển bot hiện tại sang bot B; 配信対象 của tin gửi = 200 | Yêu cầu lấy số liệu cảnh báo **KHÔNG trả về số liệu của bot A**: không có 配信対象 200, không có 今回の配信合計, không có thẻ dịch vụ — phạm vi đọc bám theo bot **đang chọn trong phiên** (bot B) chứ không theo bot của màn đang mở. Màn hình tab A **không vỡ**, không màn trắng, lớp phủ đang tải biến mất, không có lỗi JavaScript. Ghi lại chính xác điều gì xảy ra tiếp theo với tin gửi ở tầng dữ liệu (được đăng ký hay không) và đối chiếu với kết luận của §6 SPEC-01 — **không tự kết luận Đạt/Không đạt cho phần này cho tới khi contract nhánh lỗi được chốt**. | | Lấp GAP-7 / cover impact F3 + BUG · liên quan spec BR-08 (Bot Switch Guard) và BLOCKER B2 · Đánh giá spec: Spec không ghi (BR-08 chỉ mô tả form legacy, không mô tả nhóm route ajax — đã hỏi Leader) · Evidence: screenshot 2 tab + ảnh tab Network kèm mã trạng thái + kết quả truy vấn trạng thái tin gửi |
| TC-COMPATLEGACY001-01 | Data | COMPAT-LEGACY-001 | Broadcast cũ & tương thích | Normal | manual | staging | Tin gửi tạo từ phiên bản cũ — modal vẫn đếm đủ mẫu tin của chính bot, ràng buộc bot mới không lọc nhầm | - Đăng nhập chủ bot A, đã chọn bot A<br>- Bot A có **tin gửi được tạo từ phiên bản cũ** (trước khi lên broadcast V2) đang ở trạng thái chưa gửi và có mẫu tin — lấy theo cách kho TC đã dùng ở nhóm 「Broadcast cũ & tương thích」<br>- Ghi lại **trước khi chạy**, ở tầng dữ liệu: danh sách mẫu tin của tin gửi này, `bot_id` của **từng** mẫu tin, và số người nhận đã lưu<br>- Đặt hạn mức bot A sao cho chắc chắn vượt để modal hiện lên | 1. Mở màn 一斉配信 của bot A và mở tin gửi cũ đó ở màn tạo/sửa<br>2. Bấm nút xác nhận nội dung để mở hộp xem trước, rồi bấm 「この内容で配信登録」<br>3. Đọc con số 今回の配信合計 trên modal<br>4. Tính tay theo công thức: làm tròn lên (số mẫu tin thuộc bot A / 5) × số người nhận đã lưu<br>5. Đối chiếu con số trên modal với kết quả tính tay ở bước 4<br>6. Kiểm tra yêu cầu lấy số liệu **không** trả 403 và **không** trả 500 | Tin gửi tạo từ phiên bản cũ của bot A; số mẫu tin và `bot_id` từng mẫu tin lấy từ tầng dữ liệu ở tiền điều kiện; phép tính tay ghi rõ trong kết quả chạy | Yêu cầu lấy số liệu trả về bình thường (**không 403, không 500**) vì tin gửi thuộc đúng bot A. 今回の配信合計 **khớp phép tính tay** ở bước 4 và **không nhỏ hơn** số đếm được từ toàn bộ mẫu tin của tin gửi — nghĩa là ràng buộc bot mới thêm **không loại nhầm** mẫu tin hợp lệ của dữ liệu cũ. Nếu con số nhỏ hơn: ghi lại `bot_id` của các mẫu tin bị loại và báo Leader (đúng rủi ro Dev nêu ở mục 7 file 03: *cảnh báo hiện nhẹ hơn thực tế*). | | Lấp GAP-6 / cover impact F2 + D2 + T2 · regression · RULE-09 · Đánh giá spec: Spec ghi rõ (feature-spec.md §5 BR-04 template_ids) · Evidence: ảnh chụp truy vấn `bot_id` của từng mẫu tin trước khi chạy + screenshot modal + phép tính tay · dẫn từ TC-BC-330, TC-BC-332 (kho) |
| TC-ENV003-01 | API | ENV-003 | Phân quyền & môi trường | Normal | manual | **product** | Smoke trên production: chủ bot gói trả phí mở modal — đúng tên gói và hạn mức thật, không bị chặn nhầm | - Tài khoản **thật** trên production (`step.lme.jp`) đang dùng **gói trả phí** (không phải フリープラン)<br>- Bot đó có sẵn **tin gửi đã lưu của chính mình** — **KHÔNG tạo mới, KHÔNG xoá, KHÔNG đăng ký gửi**<br>- Biết trước tên gói và hạn mức tháng thật của tài khoản từ màn hợp đồng<br>- Có sự đồng ý của Leader trước khi thao tác trên tài khoản thật | 1. Đăng nhập production bằng tài khoản thật, chọn đúng bot cần kiểm<br>2. Mở màn 一斉配信, mở một tin gửi đã lưu ở màn tạo/sửa<br>3. Bấm nút xác nhận nội dung để mở hộp xem trước, rồi bấm 「この内容で配信登録」<br>4. **Đọc modal rồi đóng bằng nút 「×」 — KHÔNG bấm nút đăng ký nào**<br>5. Ghi lại: nhãn gói hiển thị trên thẻ 「エルメ」, 月間上限, 配信済み, và mã trạng thái của yêu cầu lấy số liệu<br>6. Đối chiếu nhãn gói và hạn mức trên modal với màn hợp đồng của chính tài khoản đó<br>7. Xác nhận tin gửi vẫn ở nguyên trạng thái cũ ở màn danh sách | Tài khoản production gói trả phí; không nhập dữ liệu mới; chỉ đọc | Yêu cầu lấy số liệu trả **HTTP 200** — chủ bot hợp lệ trên production **không bị cổng 403 mới chặn nhầm**. Nhãn gói trên thẻ 「エルメ」 **khớp đúng tên gói thật** ở màn hợp đồng (không hiện sai tên gói); 月間上限 và 配信済み khớp số liệu thật của tài khoản. Với gói trả phí không giới hạn, thẻ hiển thị theo đúng dạng rút gọn của gói đó. Sau khi đóng modal, tin gửi **giữ nguyên trạng thái cũ**, không phát sinh bản ghi mới. | | Lấp GAP-8 / cover impact F1 + T1 · **RULE-08** (nhóm bill tiền: gói cước + hạn mức + nút nâng cấp) · MSG-005 yêu cầu cảnh báo ghi **đúng tên plan thực tế** (đã từng có bug hiện sai tên plan Lite/Standard) · Đánh giá spec: Spec ghi rõ (feature-spec.md §5 BR-10) · Evidence: screenshot modal trên production + screenshot màn hợp đồng để đối chiếu · ⚠️ **TC chỉ đọc** — tuyệt đối không tạo/xoá/đăng ký dữ liệu thật · dẫn từ TC-BC-341, TC-BC-293 (kho) |

---

## 6. Spec update needed

| # | Vấn đề | Cần ai chốt | Vì sao chặn |
|---|---|---|---|
| **SPEC-01** | **Contract nhánh lỗi của quota-check.** Studio `TC-APICONTRACT001-01`: *403 → không modal → **vẫn đăng ký***. Kho `TC-BC-299` `[UI-003]`: *lỗi khi kiểm tra quota → **hiện lỗi rõ ràng, KHÔNG đăng ký nhầm***. Hai expected loại trừ nhau. | **PO + Leader** | **B2**. Kết hợp rủi ro Dev tự nêu (dữ liệu lệch `bot_id` → 403 với chính chủ bot), hành vi hiện tại nghĩa là **người dùng mất cảnh báo vượt quota một cách im lặng nhưng broadcast vẫn được đăng ký**. Chưa chốt thì không kết luận Đạt được. |
| **SPEC-02** | **400 vs 403 cho input không hợp lệ.** Spec `sprint-36436: spec-dev-BE:64-67` ghi **400**; bản vá #38962 cố ý gộp *invalid* + *out-of-scope* thành **403** để chống enumeration. | **PO + Leader** | Studio đã đánh dấu `spec_status = needs-human-review` ở `TC-TOOLERRHYG001-01` và `TC-FUNC003-01`; 2 TC này **không khoá được** mã trạng thái cho tới khi chốt. |
| **SPEC-03** | **`feature-spec.md` KHÔNG có tính năng 配信数上限アラート.** Kho ghi ở mâu thuẫn **MT-20**: spec chốt 2026-03-26, ticket #36436 phát sinh sau ⇒ thiếu hẳn 1 màn (modal), endpoint quota-check, và toàn bộ business rule về công thức cảnh báo. | **Leader + người giữ spec** | Không có chuẩn chính thức để đánh giá Expected của **16/16 TC** — mọi kết luận hiện dựa vào đọc mã nguồn. Cần bổ sung: ① màn modal vào `ui-spec.md`; ② endpoint vào `api-spec.md`; ③ BR công thức quota vào `feature-spec.md` §5. |
| **SPEC-04** | **Endpoint không khớp spec sprint.** `note` của `TC-FUNC001-01` ghi: *"spec nháp sprint 36436 mô tả **một endpoint khác**"* — công thức đang lấy theo `TemplateV2Controller::getBroadcastLimitAlert`. Kho MT-20 cũng nói sprint mô tả **2 endpoint mới** (quota-check riêng). | **Dev + PO** | Nếu spec sprint mới là chuẩn thì bản vá đang vá **nhầm endpoint**, hoặc tồn tại **2 endpoint song song** — endpoint còn lại chưa được rà IDOR. |
| **SPEC-05** | **Mã BR lệch nhau.** Studio `coverage` dùng ref **`BR-09`** với note *"bot-switch guard"*, `level = none`. Repo `feature-spec.md` §5: **`BR-08`** = Bot Switch Guard, `BR-09` = URL tracking. | **Leader** | Coverage của Studio không đối chiếu được với spec repo; rule **đúng trọng tâm của ticket** đang hiển thị `level = none` dưới một mã sai. |
| **SPEC-06** | **Quét ngang chưa có danh sách.** Dev khai còn nhiều chỗ đọc/ghi tin gửi theo mã thô ở `BroadcastV2Controller` / `BroadcastController` / `ChatController` nhưng **không liệt kê function nào**. Đây là **cùng một lớp lỗ hổng IDOR**, gốc là nhóm route `/ajax` không có cổng phân quyền theo bot. | **Dev + Leader** | **B3**. Cần Dev liệt kê tên function ⇒ **mở ticket riêng**. Không nhồi vào phạm vi #38962 (các endpoint đó chưa được fix). Tham chiếu `BUG-GAP-01` ở `03-dev-impact.md`. |
| **SPEC-07** | **Bug middleware bị reject nhưng chưa có ticket.** Studio bug `#729`: gọi endpoint nhóm `/ajax` khi chưa đăng nhập / cookie hỏng → **HTTP 500 + lộ stack trace**; gốc ở `CheckLogin` không trả response. `status = rejected`, lý do *"luồng chung của tool"*, `redmine_id = null`. | **Leader** | **B4**. *"Luồng chung của tool"* là lý do để **tách ticket**, không phải để đóng vấn đề. Lỗi áp cho **mọi route `/ajax`** và làm lộ đường dẫn mã nguồn. Kho đã có quan điểm tương ứng `TC-BC-340`. |

---

## Tóm tắt hành động cho member

1. **Chạy lại 8 TC bị `skip`** trên staging, **bắt đầu bằng `TC-PERM003-02` bản v2** (B1) — kèm evidence.
2. Chờ Leader/PO chốt **SPEC-01** và **SPEC-02** trước khi kết luận Đạt cho `TC-APICONTRACT001-01`, `TC-TOOLERRHYG001-01`, `TC-FUNC003-01`.
3. Chạy `TC-AUTHSESSION001-02` để xác nhận lỗi 500 có tái hiện ngoài local; báo Leader mở ticket riêng (B4 / SPEC-07).
4. Thêm **5 TC** ở §5; **dùng lại** kho `TC-BC-294` · `TC-BC-296` · `TC-BC-297` · `TC-BC-321` thay vì viết mới.
5. Bổ sung evidence cho **8 TC đang ghi Đạt** (RULE-02) và sửa `env_tag` / `exec_mode` trên Studio cho khớp thực tế.
6. Tick 2 checkbox *"Tester verify auto-fill chính xác"* ở `01-bug-task.md` và `03-dev-impact.md`.
