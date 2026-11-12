# 02 — Review docs MCP

> Draft cho Leader chốt — sinh bởi `/review-mcp-docs` 2026-10-14. Task MCP: `MCP/2026-10-14_39446_mcp-tinh-nang-tao-formanswer/`.
>
> **Leader điền cột `Quyết định Leader`** cho từng dòng ở §2 → §5, rồi chạy `/review-mcp-tc <folder>`.
> `/review-mcp-tc` **DỪNG** nếu còn dòng `DOC-*` chưa có quyết định (trừ khi human nói rõ "chạy tiếp").
> Chạy lại `/review-mcp-docs` → **giữ nguyên** quyết định đã điền (merge theo mã `DOC-*`), chỉ thêm dòng mới.
>
> Cách điền `Quyết định Leader` (1 trong 3, có thể kèm 1 câu):
> `Theo docs` (docs đúng — spec / kho cần update) · `Theo spec` (docs sai — Dev sửa code / docs) · `Khác: <quy tắc chốt>`.
> Quyết định là **expected** khi viết TC ở `/review-mcp-tc`.
>
> ℹ️ Nhiều dòng đã có **chỉ đạo của Leader** trong lần review trước (`tasks/2026-10-13_39446_mcp-tinh-nang-tao-formanswer/05-review-report.md` §4.3, 2026-10-13 → 14). AI chỉ trích chỉ đạo đó ở cột `Khả năng` để Leader xác nhận lại — **cột `Quyết định Leader` để trống**.

## 0. Nguồn

| Trường | Giá trị |
|---|---|
| Docs MCP | `docs/04-form-survey.md` — bản cập nhật 2026-10-14 (`04-form-survey (2).md`, human gửi trong chat). Attachment Redmine #39446 bản cũ: `04-form-survey.md` (2026-10-13) |
| Tài liệu tham khảo khác trong `docs/` | `Không có`. Bản spec đi kèm ticket (`form-answer.zip`) đã có tương đương trong `spec-features/admin/form-answer/` → dùng `spec-features/` |
| Spec đối chiếu | `spec-features/admin/form-answer/feature-spec.md` · `db/db-mapping.md` · `ui/ui-spec.md` (đọc targeted) |
| Kho TCs đối chiếu | `kho-tcs/fa011-taobieumau-フォーム作成.md` (MT-00 → MT-24 + TC-FORM-xx targeted) · sheet `Msg validate` r173–r269 (đã trích ở report 05 §2.2) |
| Quy mô | `5 tool · 246 param · 32 param ID` — chi tiết ở `docs/_tool-inventory.md` |
| Input khác | Folder tạo bằng tay (không qua `/new-task-mcp`): `01-bug-task.md` + `03-dev-impact.md` copy từ `tasks/2026-10-13_39446_.../`. TC gốc vẫn ở Studio task #361 |

**Docs bản 2026-10-14 đã sửa so với bản 2026-10-13** (6 điểm report 05 §4 từng nêu — không đẻ dòng mới):

| Điểm cũ (report 05) | Docs mới |
|---|---|
| D9 — `get_form_detail` ghi "range tạo qua MCP không set `action_id`" | Bỏ câu đó (§2 `diagnostic`) |
| D10 — reminder "theo từng field" ↔ "lưu theo form" | §5 `reminders`: step lưu **theo form**, chỉ gửi 1 phần tử (còn sót 1 chỗ → DOC-INT-3) |
| C9 — `line_display_name` ≤ 50 | ≤ **20** ký tự (bắt buộc chưa ghi → DOC-MISS-2) |
| D14 — countdown chỉ có ngày/giờ | Thêm `deadline_type` DATE / DURATION / ONE_TIME + `duration_*` |
| D15 — thiếu タイトル / 説明 hiển thị LINE talk | Thêm `line_talk_title` (≤ 20) + `line_talk_description` (≤ 50) |
| D22 — thiếu text + màu đồng hồ đếm ngược | Thêm `show_timer` · `timer_label` · `pin_top` · `precision` · `text_color` · `bg_color` |
| (kho TC-FORM-197) SELECT ghi friend info chỉ kiểu select | SELECT → friend info kiểu **select hoặc text** — khớp kho |

---

## 1. Tóm tắt inventory

| Tool | Thao tác | Số param | Bắt buộc | Tính năng LME (FA-xxx) |
|---|---|---|---|---|
| `list_forms` | đọc (list) | 4 | 1 | `FA-011 Tạo biểu mẫu (フォーム作成)` |
| `get_form_detail` | đọc (get) | 2 | 2 | `FA-011 Tạo biểu mẫu (フォーム作成)` |
| `get_form_responses` | đọc (get) | 4 | 2 | `FA-011 Tạo biểu mẫu (フォーム作成)` — 回答一覧 |
| `create_form_survey` | tạo | 5 | 3 | `FA-011 Tạo biểu mẫu (フォーム作成)` — 新規作成 |
| `update_form_survey` | sửa (12 thao tác) · xoá field / page | 231 | 54 (gồm `type` của 12 thao tác) | `FA-011 Tạo biểu mẫu (フォーム作成)` — フォーム編集 + 5 tab |

Ticket #39446 chỉ làm `create_form_survey` / `update_form_survey`; 3 tool đọc là tool cũ, chỉ dùng làm bước "get sau ghi" (MCP-RULE-05) và rule quyền (MCP-RULE-02). Docs **không ghi mã lỗi / mã HTTP nào** cho cả 5 tool.

---

## 2. Mâu thuẫn nội tại docs MCP (`DOC-INT`)

> **Mâu thuẫn nội tại** = trong chính file `docs/04-form-survey.md`, có 2 chỗ nói về **cùng 1 thứ** nhưng **nói khác nhau** → không biết lấy expected theo chỗ nào.
> `L365` = dòng 365 trong file docs. Leader chọn cách hiểu **(A)** hoặc **(B)** ở cột cuối.

| # | Chỗ A (dòng · docs ghi) | Chỗ B (dòng · docs ghi) | Mâu thuẫn là gì | (A) | (B) | Severity | Quyết định Leader |
|---|---|---|---|---|---|---|---|
| DOC-INT-1 | **L365** `create_form_survey.title`:<br>"フォーム名 — hiển thị cho người trả lời, ≤ 20" | **L834** `UPDATE_SETTINGS.line_display_name`:<br>"フォーム名 — hiển thị cho người trả lời, ≤ 20" | Cùng là フォーム名 nhưng 2 tên param. Tạo dùng `title`, sửa dùng `line_display_name` → sửa cái này có đổi cái kia không? | Là **1 dữ liệu**: sửa `line_display_name` thì `title` đổi theo | Là **2 dữ liệu**: `title` hiện ở form, `line_display_name` chỉ hiện ở LINE talk | `[MAJOR]` | |
| DOC-INT-2 | **L364** `create_form_survey.name`:<br>"管理名, ≤ 50" | **L835** `UPDATE_SETTINGS.system_name`:<br>"管理名, ≤ 50" | Cùng là 管理名 nhưng tạo dùng `name`, sửa dùng `system_name` → sửa xong list form có hiện tên mới không? | Là **1 dữ liệu**: list form hiện tên mới | **Chỉ đổi `system_name`**, list form vẫn tên cũ → bug | `[MINOR]` | |
| DOC-INT-3 | **L744** `reminders`:<br>"gửi nhiều phần tử thì phần tử sau ghi đè phần tử trước" | **L746 + L765**:<br>"1 phần tử = 1 field REMINDER" · "chỉ gửi 1 phần tử" | Chỗ A: gửi 2 phần tử vẫn chạy. Chỗ B: mỗi câu REMINDER 1 phần tử nhưng chỉ được gửi 1 → gửi 2 phần tử thì sao? | **Chạy được**, phần tử sau thắng | **Bị chặn** 400 / 422 | `[MINOR]` | |
| DOC-INT-4 | **L961** tiêu đề mục:<br>"Field chung — áp dụng cho **câu hỏi** nhóm 1 + 2" | **L970–972** 3 param css:<br>"áp cho câu hỏi **+ HEADING** … **DIVIDER**" | Tiêu đề nói css chỉ cho câu hỏi, nhưng mô tả param lại nói áp cả HEADING / DIVIDER (item trang trí) | css áp **cả HEADING / DIVIDER** | css **chỉ cho câu hỏi** | `[MINOR]` | |
| DOC-INT-5 | **L615** `SET_NEXT_PAGE.field_id`:<br>"Chỉ nhận câu **SELECT** bắt buộc" | **L621** ràng buộc:<br>"câu rẽ nhánh **không chuyển sang checkbox**" | SELECT không có kiểu checkbox, chỉ câu **診断** mới có → chỗ B ngầm cho 診断 làm câu rẽ nhánh, trái chỗ A | **Chỉ SELECT** | **SELECT + 診断** (+ 性別) — chốt chung DOC-SPEC-1 | `[MINOR]` | |
| DOC-INT-6 | **L1314** "Bảng limit tổng hợp" | **L737, 761, 810, 834–837, 852, 861, 868**: limit ghi trong bảng param | Không trái nghĩa — bảng tổng hợp **thiếu** ~10 limit (≤ 20 / ≤ 50 / ≤ 5000…) đã ghi ở bảng param | Dev bổ sung bảng tổng hợp | — | `[NIT]` | |

---

## 3. Docs trái spec-features / kho-tcs (`DOC-SPEC`)

| # | Tool · param | Docs ghi | Đối chiếu (nguồn + vị trí) | Khả năng | Severity | Quyết định Leader |
|---|---|---|---|---|---|---|
| DOC-SPEC-1 | `SET_NEXT_PAGE.field_id` — loại câu được điều khiển rẽ nhánh | "Chỉ nhận SELECT (radio/dropdown) bắt buộc"; mục "Áp dụng cho form phân nhánh" nhắc lại | Kho **TC-FORM-232** (web): select box rẽ nhánh gồm radio 必須 · dropdown 必須 · **診断 単一選択 必須** · **性別 必須** | (A) docs / code MCP hẹp hơn web → MCP phải nhận thêm DIAGNOSTIC radio + GENDER · (B) cố ý giới hạn MCP → ghi rõ ngoại lệ. **Chỉ đạo Leader 2026-10-13 (05 §4.3 C3):** radio / dropdown / 診断 / 性別 必須 đều hợp lệ | `[MAJOR]` | |
| DOC-SPEC-2 | `REMOVE_FIELD` câu đang điều khiển rẽ nhánh | "xoá được — cấu hình phân nhánh của page tự reset về kết thúc form" (§5 REMOVE_FIELD + SET_NEXT_PAGE + mục form phân nhánh) | Kho **TC-FORM-234** + sheet Msg validate r217: web **chặn** xoá, message 「この項目は分岐が設定されていますので、変更できません。」 | (A) docs / code MCP sai → MCP phải chặn 400 / 422 · (B) cố ý cho MCP xoá → ghi rõ ngoại lệ so với web | `[MAJOR]` | |
| DOC-SPEC-3 | Mã friend info hệ thống: `BIRTHDAY` −4 · `DATE.friend_info_id` −5 (生年月日) · `ADDRESS` −11 | Bảng nhóm 2 + mục DATE | `feature-spec.md` BR-05 + `db/db-mapping.md:167`: chỉ có −1 view_name · −2 phone · −3 email · **−6 province**; không có −4 / −5 / −11 | (A) docs ghi sai mã → câu trả lời ghi nhầm friend info · (B) spec reverse-engineer cũ thiếu mã mới → update BR-05 + db-mapping | `[MAJOR]` | |
| DOC-SPEC-4 | `SELECT.record_mode=tags` — cách gắn tag | "mỗi option gắn với 1 tag **theo label** — tag **chưa có sẽ tự tạo** khi friend trả lời"; options "label **không được trùng nhau**" | Kho **TC-FORM-138 / 140**: web mỗi option có 2 phần (フォームに表示する選択肢 + dropdown **連携するタグ** chọn tag có sẵn), thiếu tag báo 「タグを選択してください。」 · **TC-FORM-141**: khi liên kết tag **cho phép trùng text option** | (A) docs / code MCP khác web → MCP phải nhận `tag_id` có sẵn cho từng option, chặn khi thiếu, cho trùng label ở chế độ tags · (B) cố ý đơn giản hoá cho MCP (map theo label, auto-create) → ghi rõ, spec bổ sung hành vi MCP. Liên quan TC NEW-1455 đang fail (report 05 C10) | `[MAJOR]` | |
| DOC-SPEC-5 | `UPDATE_MESSAGE_ACTION.reminders[].steps` — REPLACE | "REPLACE toàn bộ step hiện có của form (step không gửi sẽ bị xóa)" | `03-dev-impact.md` 4.3 **T3**: "step tạo từ MCP … **không phá step tạo từ web**" · kho **TC-FORM-290**: xoá step trên web có confirm + huỷ lịch nhắc chưa gửi | (A) docs đúng → MCP gửi thiếu step là xoá luôn step web + huỷ lịch của bạn bè (không confirm) — Dev xác nhận T3 hiểu theo nghĩa này · (B) Dev T3 đúng → MCP không được xoá step web, docs sửa | `[BLOCKER]` (xoá dữ liệu + lịch gửi) | |
| DOC-SPEC-6 | Limit gói Free | "Số form (gói free) ≤ 3 (server từ chối)" — không phân biệt Free cũ / mới | Kho **MT-24** (Leader chốt 2026-10-13): bot Free **cũ** (`flag_contract_new = 0`) tạo form **không giới hạn**; Free mới ≤ 3, đếm gộp form web + MCP. `mcp-rules.md` MCP-RULE-03 | (A) docs thiếu ngoại lệ Free cũ → sửa docs · (B) code MCP chặn cả Free cũ → bug. **Chỉ đạo Leader 2026-10-13 (05 §4.3 C2):** Free cũ không giới hạn | `[BLOCKER]` (gói) | |
| DOC-SPEC-7 | `SET_NEXT_PAGE.branches` — option không có trong mảng | "Option không có trong mảng sẽ theo đích của **phần tử đầu tiên**" | Kho **TC-FORM-238** (web): option mới thêm vào câu rẽ nhánh hiển thị "**chưa có next page**" | (A) docs / code MCP đặt đích ngầm khác web → MCP phải để trống / bắt khai đủ option · (B) web cũng fallback phần tử đầu khi trả lời → kho cập nhật expected | `[MAJOR]` | |
| DOC-SPEC-8 | `field.required` default cho `GENDER` | "required — Default `true` (giống web khi thêm mới)" áp chung mọi câu hỏi | Kho **TC-FORM-192**: item 性別 mặc định **任意** | (A) docs / code MCP sai cho GENDER → default false · (B) web đã đổi → kho update | `[MINOR]` | |

---

## 4. Docs thiếu so với spec-features (`DOC-MISS`)

| # | Nhóm | Tool · param / setting | Spec / web có | Docs MCP | Câu hỏi cho Leader | Severity | Quyết định Leader |
|---|---|---|---|---|---|---|---|
| DOC-MISS-1 | `(c) MCP-RULE-01` | `get_form_detail.form_ids` · `get_form_responses.form_id` · `update_form_survey.form_id` · `bot_id` của bot không thuộc user | mcp-rules.md 2.1 | Không nói | Form của bot B (cùng account / account khác / không tồn tại) truyền với `bot_id` bot A → 403 / 404, không lộ dữ liệu? `form_ids` trộn ID hợp lệ + ID bot B → bỏ ID lạ hay chặn cả request? | `[BLOCKER]` | |
| DOC-MISS-2 | `(b) validate` | `UPDATE_SETTINGS.line_display_name` · `line_talk_title` · `line_talk_description` | Kho **TC-FORM-309 / 310**: cả 3 **bắt buộc** (rỗng → invalid); フォーム名 + タイトル ≤ 20, mặc định = 管理名; 説明 ≤ 50, mặc định 「こちらから回答してください。」 | Chỉ ghi max, không ghi bắt buộc / default | MCP chặn chuỗi rỗng / chỉ khoảng trắng ở 3 param này (400 / 422)? Form tạo qua MCP có nhận đúng default như web? **Chỉ đạo Leader 2026-10-14 (05 §4.3 C9):** `line_display_name` bắt buộc, ≤ 20 | `[MAJOR]` | |
| DOC-MISS-3 | `(c) MCP-RULE-01` | ID đối tượng **con của form**: `page_id` (HEADER_IMAGE · ADD_FIELD · UPDATE_BUTTON · REMOVE_PAGE · SET_NEXT_PAGE) · `field_id` · `next_page_id` · `branches[].next_page_id` · `reminders[].field_id` · `steps[].id` · `point_ranges[].id` | mcp-rules.md 2.1 | Không nói | ID thuộc form khác (cùng bot / bot B) hoặc không tồn tại → 403 / 404 hay 400 / 422? Không sửa nhầm page / field / step của form khác? | `[BLOCKER]` | |
| DOC-MISS-4 | `(c) MCP-RULE-01` | ID **tham chiếu tài nguyên khác**: `folder_id` · `reply_action_id` · `open_action_id` · `steps[].action_id` · `point_ranges[].action_id` · `point_field_id` · `friend_info_id` (TEXT / DATE / FILE_UPLOAD / DIAGNOSTIC) | mcp-rules.md 2.1 (docs chỉ ghi "của bot khác → lỗi" cho `SELECT.friend_info_id`) | Chỉ SELECT có | ID của bot B / không tồn tại / sai loại (vd tag_id truyền vào action_id) → chặn, không tạo nửa chừng — áp cho **mọi** param ID trên? | `[BLOCKER]` | |
| DOC-MISS-5 | `(c) MCP-RULE-02` | Mọi tool form (cả 3 tool đọc) | Kho **MT-19** chốt quyền staff; `feature-spec.md` §1 Actors | Không nói | Staff không có quyền フォーム gọi bất kỳ tool form nào → 403? Thu hồi quyền khi token còn hạn → lần gọi sau bị chặn? **Chỉ đạo Leader 2026-10-13 (05 §4.3 D13):** staff không quyền form không được gọi tool form | `[BLOCKER]` | |
| DOC-MISS-6 | `(c) MCP-RULE-03` | `create_form_survey` — gói Free | Kho MT-24 · mcp-rules.md MCP-RULE-03 | "≤ 3 (server từ chối)", không ghi mã lỗi, không nói đếm gộp web + MCP | Vượt limit trả 400 / 422 (chỉ đạo Leader 05 §4.3 C5)? Đếm gộp form web + MCP? Form trong thùng rác có tính không (TC NEW-6)? | `[MAJOR]` | |
| DOC-MISS-7 | `(c) MCP-RULE-04` | `create_form_survey.name` · `UPDATE_SETTINGS.system_name` (đổi tên) | Kho **MT-23** (Leader chốt 2026-10-13): 管理名 **không được trùng** trong bot | Không nói | Trùng 管理名 (MCP vs MCP · MCP vs web · đổi tên qua `system_name` · khác hoa/thường · khoảng trắng đầu/cuối) → 400 / 422; bot khác → cho phép? **Chỉ đạo Leader 2026-10-13 (05 §4.3 C1)** | `[MAJOR]` | |
| DOC-MISS-8 | `(b) validate` | Limit theo web chưa có trong docs: `CUSTOM_HTML.html` / `TEXT_BLOCK.content` ("không giới hạn") · `css.custom_css` / `custom_js` · `after_submit.message` · `countdown.expired_message` · số step nhắc · số dải điểm · số item / page | Kho **MT-03** (Leader chốt): HTML / CSS / JS / trang sau trả lời / text hết countdown **20.000** · **50** step nhắc · **1.000** dải điểm · **500** item / page. ⚠️ Kho **TC-FORM-333** lại ghi text hết countdown **bắt buộc, ≤ 50** — mâu thuẫn trong kho | Không ghi / ghi "không giới hạn" | MCP chặn đúng các ngưỡng này (400 / 422)? `expired_message` theo MT-03 (20.000) hay TC-FORM-333 (≤ 50, bắt buộc)? **Chỉ đạo Leader 2026-10-13 (05 §4.3 D1):** check limit theo kho MT-03 | `[MAJOR]` | |
| DOC-MISS-9 | `(b) validate` | `countdown.timer_label` · `countdown.text_color` / `bg_color` · `countdown.expired_url` | Sheet Msg validate **r266 → r269**: タイマーテキスト **bắt buộc, ≤ 50**; màu chữ / nền timer bắt buộc + đúng `#RRGGBB` · kho **TC-FORM-333**: URL hết hạn rỗng / không phải URL → invalid | Không ghi bắt buộc / limit | `show_timer=true` mà thiếu `timer_label` / quá 50 ký tự / màu sai định dạng → 400 / 422? `expired_display=URL` mà `expired_url` rỗng / sai định dạng → chặn? | `[MAJOR]` | |
| DOC-MISS-10 | `(b) validate` | `countdown` kiểu DURATION | Kho **TC-FORM-340** (1 ngày 1 giờ 30 phút) — không có biên | Không ghi min của `duration_days`; không nói tổ hợp 0 ngày 0 giờ 0 phút | `duration_days` = 0 / âm, tổng thời lượng = 0 → chặn? `duration_mode=CLOCK` thiếu `duration_end_time` → chặn? | `[MINOR]` | |
| DOC-MISS-11 | `(b) validate` | `update_form_survey.items[]` — 1 item lỗi | `01-bug-task.md` Cách thực hiện: `McpFormSurveyTool` **pre-validate toàn bộ items gồm DB refs trước khi áp** | Chỉ ghi "thực thi tuần tự theo thứ tự mảng"; không ghi mã lỗi / format lỗi | 1 item lỗi → **cả batch** bị từ chối, không item nào được áp (all-or-nothing)? Response báo item thứ mấy lỗi? Mã 400 / 422 (MCP-RULE-07)? | `[MAJOR]` | |
| DOC-MISS-12 | `(b) validate` | `ADD_PAGE` | Kho **TC-FORM-213**: trùng tên page trong form → 「ページ名はすでに利用されています。」 | Chỉ ghi "≤ 10 ký tự" | Trùng `page_name` (kể cả khoảng trắng đầu/cuối) → 400 / 422? **Chỉ đạo Leader 2026-10-13 (05 §4.3 D6):** check trùng tên page | `[MAJOR]` | |
| DOC-MISS-13 | `(b) validate` | `ADD_PAGE` · `REMOVE_PAGE` · `SET_NEXT_PAGE` trên form シンプル | Web: form シンプル không có nút thêm page / 次のページ | "form シンプル … không dùng" — không nói bị chặn | Gọi 3 thao tác này trên form_type=1 → 400 / 422 hay tạo page "ẩn"? | `[MAJOR]` | |
| DOC-MISS-14 | `(b) validate` | `ADD_FIELD` DIAGNOSTIC khi chưa bật 診断 | Yêu cầu Leader 2026-10-13: phải bật 診断 (`UPDATE_DIAGNOSTIC.enabled=true`) trước · `ui-spec.md` §SCR-FA11-06 | Chỉ ghi chiều ngược ("không tắt được khi còn field DIAGNOSTIC") | Thêm item DIAGNOSTIC khi chưa bật → 400 / 422? Bật + thêm trong cùng 1 `items[]` (bật trước) → được? | `[MAJOR]` | |
| DOC-MISS-15 | `(b) validate` | `SELECT` liên kết friend info **có sẵn** — thêm option qua `UPDATE_FIELD` | QA xác nhận 2026-10-13 theo web: không cho thêm option (ghi chú TC NEW-41, đang fail) | Không nói | MCP chặn thêm option mới vào câu SELECT liên kết friend info có sẵn? | `[MAJOR]` | |
| DOC-MISS-16 | `(a) setting web` | SELECT ghi friend info kiểu **text**: 2 cột 選択肢 + 登録する友だち情報 | Kho **TC-FORM-209**: cột 2 (giá trị ghi vào friend info) khác cột 1 được; bỏ trống thì ăn theo cột 1 | `options[]` chỉ có `{label}` | MCP có cần set giá trị ghi vào friend info khác label hiển thị không? | `[MINOR]` | |
| DOC-MISS-17 | `(a) setting web` | 入力制限 (`input_restriction`) | Kho **TC-FORM-126 / MT-17**: 6 lựa chọn, tách 整数 (không thập phân) và 数値 (có thập phân) | 5 giá trị, chỉ có `numeric` | `numeric` ứng với 整数 hay 数値? MCP có cần lựa chọn còn lại? | `[MINOR]` | |
| DOC-MISS-18 | `(a) setting web` | Item 住所: chế độ tìm theo mã bưu điện + từng ô con ON/OFF + 必須/任意 | Kho **TC-FORM-185 / 186 / 187** | Chỉ `address_placeholders`; `required` chung 4 ô | MCP có cần bật/tắt ô con + chế độ tìm mã bưu điện? | `[MINOR]` | |
| DOC-MISS-19 | `(a) setting web` | Trang xác nhận: text nút (≤ 30, mặc định 回答を送信する) + design | Kho **TC-FORM-323 / 324** · sheet r255 → r258 | `confirm_page` chỉ Boolean | MCP có cần đổi text / design nút trang xác nhận? | `[MINOR]` | |
| DOC-MISS-20 | `(a) setting web` | Font chữ form (7 loại) | Kho **TC-FORM-266** | UPDATE_DESIGN không có font | MCP có cần đổi font? | `[MINOR]` | |
| DOC-MISS-21 | `(a) setting web` | Filter (絞り込み) cho action trả lời / action mở form / action dải chẩn đoán | Kho **TC-FORM-279 / 306** | Chỉ step nhắc dùng `update_filter` | MCP có cần đặt filter cho 3 loại action này? | `[MINOR]` | |

---

## 5. Docs có, spec không có (`DOC-EXTRA`) — thông tin

| # | Tool · param | Docs ghi | Ghi chú | Quyết định Leader |
|---|---|---|---|---|
| DOC-EXTRA-1 | `countdown.timer_label` ↔ `show_duration.display_text` | "**Dùng chung cột `title_timer`** — set cái này đè cái kia" | db-mapping chỉ có 1 cột `title_timer` (show_duration chỉ là cờ tinyint) → khớp cấu trúc DB, nhưng spec / kho không mô tả web có hành vi đè chéo. Cần xác nhận trên web: sửa text 回答時間表示 có làm đổi text đồng hồ không. Nếu đúng → spec bổ sung; TC MCP phải có case đè chéo | |
| DOC-EXTRA-2 | `list_forms.names` | Lọc EXACT theo `name` HOẶC `title`, case-insensitive, trim, OR; trả `not_found_names` | Chỉ có ở MCP — không áp ngược sang TC màn list web | |
| DOC-EXTRA-3 | `get_form_detail` — `message_action` · `diagnostic` · `design` · `settings` · `pages[].button` · `pages[].next_page` · `pages[].fields[].field` | Reverse-map đúng shape của input `update_form_survey` để verify | Nguồn oracle cho MCP-RULE-05 (get sau ghi). Các khoá `apply_to_existing` / `*_overwrite` write-only, **không trả về** | |
| DOC-EXTRA-4 | `UPDATE_MESSAGE_ACTION.reminders` — filter của step | Đặt filter step nhắc qua tool `update_filter` (`target='form_reminder'`, `target_id=<step id>`) | Luồng 2 tool chỉ có ở MCP; web đặt filter ngay trong modal step | |
| DOC-EXTRA-5 | `HEADER_IMAGE.image_url` · `IMAGE.image_url` · `header.image_url` | Ảnh lấy từ `download_url` của tool `get_file_params` | Luồng upload chỉ có ở MCP; limit 10MB / định dạng / 10000px theo web (đã có TC-MEDIA001-01 → 04) | |
| DOC-EXTRA-6 | `UPDATE_FIELD` | Gửi **toàn bộ trạng thái mới**, option ghi đè toàn bộ (không phải diff); `field_type` không đổi được | Ngữ nghĩa REPLACE riêng của MCP | |
| DOC-EXTRA-7 | `UPDATE_DESIGN` / `UPDATE_SETTINGS` / `UPDATE_MESSAGE_ACTION` | Ngữ nghĩa **PATCH** theo section / khối / field | Web luôn lưu cả tab → TC MCP cần case "chỉ khối truyền lên đổi, khối khác giữ nguyên" | |

---

## 6. Tổng hợp chờ Leader chốt

| Severity | DOC-INT | DOC-SPEC | DOC-MISS | DOC-EXTRA | Tổng |
|---|---|---|---|---|---|
| `[BLOCKER]` | 0 | 2 | 4 | — | 6 |
| `[MAJOR]` | 1 | 5 | 10 | — | 16 |
| `[MINOR]` / `[NIT]` | 5 | 1 | 7 | 7 | 20 |

6 dòng `[BLOCKER]`: DOC-SPEC-5 (REPLACE xoá step nhắc tạo từ web) · DOC-SPEC-6 (Free cũ) · DOC-MISS-1 / 3 / 4 (bot A ↔ B theo từng loại ID) · DOC-MISS-5 (staff).

Đã có chỉ đạo Leader từ lần review trước (chỉ cần xác nhận lại): DOC-SPEC-1 · DOC-SPEC-6 · DOC-MISS-2 · DOC-MISS-5 · DOC-MISS-6 · DOC-MISS-7 · DOC-MISS-8 · DOC-MISS-12.

**Bước tiếp theo**: Leader điền cột `Quyết định Leader` → Studio đã có TC (task #361) → chạy `/review-mcp-tc MCP/2026-10-14_39446_mcp-tinh-nang-tao-formanswer/`.
