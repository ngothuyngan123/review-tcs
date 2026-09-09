# 03 — Đánh giá ảnh hưởng từ Dev

> **Nguồn**: Redmine #33107 — journal #133179 của **AI LME Fix bug**, `2026-08-27T03:42:52Z`
> (báo cáo tự động "★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST"). Nội dung dưới đây **paste nguyên văn**; phần bảng do `/new-task` cấu trúc lại (đã đánh dấu rõ).

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (hệ thống Auto-fixbug LME) — QA nhận: `Ngô Thúy Ngần` |
| Commit / Pull Request | `<chưa có PR link>` — repo `sns-line`, commit `822b9abcd9` (4 file) |
| Branch | `ai_fixbug_33107` (nhánh gốc `release_step_20260805`) — đã push origin |
| Ngày submit đánh giá | `2026-08-27` |
| Auto-filled | `2026-09-04 by /new-task` |

⚠️ **Branch lệch số ticket**: journal #115487 (Nguyen Ngoc Hai, 2026-03-27) ghi `branch: fix-bug-27083` — mang số ticket **27083**, không phải 33107. Cần hỏi Dev đây là fix cũ khác hay ticket gộp.

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

> Nguyên văn mục ■ 1 của báo cáo AI:

Màn tạo mẫu tin nhắn con và các API lưu chỉ lấy id nhóm/bước từ URL rồi dùng thẳng, không kiểm tra id đó có thuộc tài khoản đang đăng nhập hay không. Vì vậy bot A mở được link tạo mẫu tin của bot B và ghi mẫu tin con vào nhóm của bot B, trong khi mẫu tin con lại mang mã bot của A nên dữ liệu bị lệch chủ sở hữu. Màn sản phẩm cũng vậy: API lưu sản phẩm không kiểm chủ sở hữu nên bot A sửa được sản phẩm của bot B; riêng màn sản phẩm bản cũ câu lệnh cập nhật còn ghi đè cả cột mã bot nên sản phẩm bị chuyển hẳn sang bot A.

**→ `BUG` (root cause):** thiếu ownership check theo `bot_id` ở **cả 2 tầng** (controller màn + service lưu), trên **2 luồng**: (a) tạo mẫu tin con Template V2 (4 biến thể link), (b) xem/sửa item bán hàng (bản mới + bản cũ).

## 2. Cách fix

> Nguyên văn mục ■ 2 của báo cáo AI:

Thêm kiểm tra quyền sở hữu theo bot ở cả 2 tầng cho 2 luồng bị báo lỗi. Luồng mẫu tin: màn tạo mẫu tin con kiểm tra nhóm mẫu tin / bước kịch bản / bước sự kiện / tin gửi hàng loạt nhận qua URL có thuộc bot đang đăng nhập không, không đúng thì đưa về danh sách mẫu tin; đồng thời 4 hàm lưu tương ứng ở tầng nghiệp vụ cũng chặn ghi và trả lỗi thay vì ghi vào dữ liệu bot khác. Luồng sản phẩm: cả màn mới và màn cũ đều tìm sản phẩm kèm điều kiện mã bot và trả lỗi nếu không thuộc bot đang đăng nhập, câu lệnh cập nhật cũng thêm điều kiện mã bot. Guard cố ý chỉ chặn khi bản ghi có thật và thuộc bot khác, còn id rỗng/âm (giá trị quy ước của màn, ví dụ -11 khi gửi hàng loạt) hoặc bản ghi không tồn tại thì giữ nguyên luồng cũ để không làm hỏng thao tác tạo mới. Quét ngang còn 2 chỗ cùng kiểu chưa sửa vì ngoài phạm vi ticket (xem mục yokoten).

> ⚠️ **Input thiếu**: báo cáo AI trỏ tới "mục yokoten" cho **2 chỗ cùng kiểu chưa sửa**, nhưng **journal KHÔNG có mục yokoten**. Phải hỏi Dev 2 chỗ đó là gì — đây chính là vùng dễ lọt bug cross-bot còn lại.
> (Manh mối từ Studio: `REQ-016` — chức năng **xem trước tin nhắn con** cũng phải giới hạn theo bot, gắn nhãn `yokoten RK-01`. Xem cảnh báo W6 cuối file.)

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

> Nguyên văn danh sách mục ■ 3 (13 function). Cột "Thay đổi" / "Lý do" do `/new-task` suy từ mục 2 — **Dev KHÔNG phân loại**, tester confirm lại.

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `TemplateV2Controller::createTemplate` — `app/Http/Controllers/Basic/TemplateV2Controller.php` | Thêm guard ownership trước khi render màn soạn tin | Chặn 4 biến thể link cross-bot |
| 2 | `TemplateV2Controller::isTemplateGroupOwnedByBot` — cùng file | **Hàm mới** (guard) | Kiểm nhóm mẫu tin thuộc bot đang đăng nhập |
| 3 | `TemplateV2Controller::saveTemplate` — cùng file | Thêm guard tầng controller | Chặn ghi cross-bot |
| 4 | `TemplateV2Service::isGroupOwnedByCurrentBot` — `app/Services/Templates/TemplateV2Service.php` | **Hàm mới** (guard tầng service) | Ownership check dùng chung |
| 5 | `TemplateV2Service::saveTemplate` — cùng file | Chặn ghi + trả lỗi | Trước fix dùng `Template::find(id)` không kèm `bot_id` |
| 6 | `TemplateV2Service::saveScenario` — cùng file | Chặn ghi + trả lỗi | Trước fix dùng `StepMessage::find(id)` |
| 7 | `TemplateV2Service::saveSendAll` — cùng file | Chặn sớm bằng guard | Vốn đã scope theo `bot_id` nhưng vẫn **tạo mẫu tin mồ côi** |
| 8 | `TemplateV2Service::saveEvent` — cùng file | Chặn ghi + trả lỗi | Trước fix dùng `EventStep::find(id)` |
| 9 | `TemplateV2Service::saveTemplateByType` — cùng file | Điều phối theo `action_type` | Dispatch tới 4 hàm lưu ở trên |
| 10 | `SalesManagementV2Controller::saveItem` — `app/Http/Controllers/Basic/SalesManagementV2Controller.php` | Tìm item kèm `bot_id`, trả lỗi nếu khác bot | Trước fix dùng `SItems::find(id)` |
| 11 | `SalesManagementV2Controller::ajaxGetItemDetail` — cùng file | Không trả dữ liệu item bot khác | Chống lộ cấu hình action / mục thông tin KH |
| 12 | `SalesManagementController::saveItem` — `app/Http/Controllers/Basic/SalesManagementController.php` (**bản cũ**) | Thêm `bot_id` vào cả `where` lẫn `update` | Trước fix `update` **ghi đè `bot_id`** → chiếm quyền sở hữu |
| 13 | `SalesManagementController::editItem` — cùng file (**bản cũ**) | Guard trước khi render form | Màn cũ vẫn gọi được qua sidebar + `public/js/sales/list_items.js` |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

> Mục ■ 4.1 của báo cáo AI ghi **"File thay đổi"** (4 file), không ghi theo function. Bảng dưới ghép 4 file đó với 13 function ở mục 3.
> ⚠️ Dev **KHÔNG** phân loại Direct/Indirect — cột dưới do `/new-task` suy, tester phải confirm.

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | Màn tạo mẫu tin con (`createTemplate` + guard) | `app/Http/Controllers/Basic/TemplateV2Controller.php` | Direct | 4 biến thể link: nhóm mẫu tin / scenario / sendAll / event |
| F2 | Lưu mẫu tin con (`saveTemplate` / `saveScenario` / `saveSendAll` / `saveEvent` / `saveTemplateByType`) | `app/Services/Templates/TemplateV2Service.php` | Direct | Tầng service — chặn ghi vào dữ liệu bot khác |
| F3 | Sửa / lưu item bán hàng **bản mới** (`saveItem`, `ajaxGetItemDetail`) | `app/Http/Controllers/Basic/SalesManagementV2Controller.php` | Direct | Trả 404 / trả data mặc định khi item thuộc bot khác |
| F4 | Sửa / lưu item bán hàng **bản cũ** (`saveItem`, `editItem`) | `app/Http/Controllers/Basic/SalesManagementController.php` | Direct | `COMPAT-LEGACY` — màn cũ vẫn reachable từ sidebar |
| F5 | Luồng tạo mới hợp lệ (id rỗng / âm `-11` / id không tồn tại) | (đi qua F1, F2) | Indirect | Guard **cố ý không chặn** → rủi ro chặn nhầm hoặc bỏ lọt |

### 4.2. List data bị update khi fix bug

> Nguyên văn mục ■ 4.2 của báo cáo AI, gắn tag `D*`:

| # | Data (table.column) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `template.bot_id` / `template.content` | UPDATE (chặn ghi mới) | Mẫu tin con của bot khác **đã bị ghi vào nhóm sai chủ sở hữu trước fix** — dữ liệu cũ cần rà; fix chỉ chặn phát sinh mới |
| D2 | `step_message.template_ids` | UPDATE (chặn ghi mới) | Danh sách mẫu tin của bước **có thể đã chứa mẫu tin của bot khác**. ⚠️ Bảng này **KHÔNG có cột `bot_id`** → phải tra chủ sở hữu qua `scenario.bot_id` |
| D3 | `event_step.templates_id` | UPDATE (chặn ghi mới) | Bảng có cột `bot_id` |
| D4 | `broadcast.template_ids` | UPDATE (chặn ghi mới) | Có thể đã chứa mẫu tin của bot khác |
| D5 | `s_items.bot_id` | UPDATE (**chiếm quyền sở hữu**) | Màn item **bản cũ** ghi đè `bot_id` → item của bot khác **đã bị chuyển hẳn sang bot A** |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

> Nguyên văn mục ■ 4.3. ⚠️ Dev **KHÔNG** ghi mức nguy cơ regression — tester đánh giá.

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Message Template (FA-010)** — chặn tạo/lưu mẫu tin con vào nhóm của bot khác | F1, F2, D1 | `<Dev không ghi — tester đánh giá>` |
| T2 | **Step Delivery / Scenario (FA-009)** — chặn ghi mẫu tin vào bước kịch bản bot khác | F1, F2, D2 | `<Dev không ghi — tester đánh giá>` |
| T3 | **Broadcast (FA-008)** — chặn ghi mẫu tin vào tin gửi hàng loạt bot khác | F1, F2, D4 | `<Dev không ghi — tester đánh giá>` |
| T4 | **Event Booking (FA-021)** — chặn ghi mẫu tin vào bước sự kiện bot khác | F1, F2, D3 | `<Dev không ghi — tester đánh giá>` |
| T5 | **Single Product / Sales (FA-026)** — chặn xem/sửa + chặn chiếm quyền sở hữu item bot khác | F3, F4, D5 | `<Dev không ghi — tester đánh giá>` |

---

## Phụ lục — các mục còn lại của báo cáo AI auto-fixbug (nguyên văn)

### ■ 5. RECOVER DATA

⚠ **CÓ** — Fix chỉ chặn phát sinh mới. Dữ liệu đã lệch trước đó cần rà: (1) mẫu tin con có `bot_id` khác `bot_id` của nhóm chứa nó (`template.content` / `step_message.template_ids` / `event_step.templates_id` / `broadcast.template_ids`); (2) sản phẩm bị đổi `bot_id` qua màn sản phẩm bản cũ. Chưa dump được vì dev DB không kết nối được.

**Phạm vi**: cần chạy trên DB production/staging — đối chiếu `bot_id` của mẫu tin con với `bot_id` của nhóm cha để liệt kê bản ghi lệch, và rà lịch sử sửa `s_items.bot_id`.

### ■ 6. VERIFY

- **Mức: `lint`** (chưa chạy runtime)
- `php -l` 4 file: No syntax errors detected.
- `git diff --stat release_step_20260805...ai_fixbug_33107`: đúng 4 file đã sửa, không kéo commit lạ.
- **Bằng chứng đọc code (trước fix)**: `TemplateV2Service::saveTemplate` dùng `Template::find(id)`; `saveScenario` dùng `StepMessage::find(id)`; `saveEvent` dùng `EventStep::find(id)` — **đều không có điều kiện `bot_id`**. `SalesManagementV2Controller::saveItem` dùng `SItems::find(id)`. `SalesManagementController::saveItem` dùng `SItems::where(id)` rồi `update` **kèm `bot_id` = bot hiện tại**. `saveSendAll` vốn đã scope update theo `bot_id` nên không bị ghi đè, nhưng **vẫn tạo mẫu tin mồ côi** — đã chặn sớm bằng cùng guard.
- **Không tái hiện được trên dev**: MySQL `host.docker.internal:3306` → Connection refused (dev stack không chạy) → chưa dump được dữ liệu lệch `bot_id`.
- **Schema**: `event_step` và `s_items` có cột `bot_id`; **`step_message` KHÔNG có `bot_id`** → tra chủ sở hữu qua `scenario.bot_id` (nguồn `/workspace/share/db/db-refined`).

### ■ TỰ REVIEW (AI) — rủi ro / lưu ý khi test

1. **Chưa chạy được runtime/dev DB** (Connection refused) → chưa verify bằng thao tác thật; mức verify mới chỉ là **lint + đọc code**.
2. Nếu có **luồng hợp lệ nào cố tình truyền `template_group_id` của bot khác** (ví dụ tính năng dùng chung mẫu tin giữa các bot) thì sẽ **bị chặn nhầm** — đọc code hiện tại không thấy luồng như vậy, nhưng **human nên xác nhận**.
3. Màn sản phẩm **bản cũ** (`list-items-old`) vẫn được tham chiếu trong sidebar và `public/js/sales/list_items.js` nên vẫn gọi tới được → đã fix luôn thay vì bỏ qua.

### Link tham chiếu

- Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=fixbug-lme&tab=events&session=5f804523-c1d5-41b1-89fc-4ae67630946f
- Dashboard fixbug: https://dashboard.melonglobal.net/fixbug-lme/?id=33107
- Thời gian AI xử lý: 9 phút 16 giây

---

## ⚠️ Cảnh báo cho Leader trước khi giao TCs

| # | Vấn đề | Ảnh hưởng tới TC |
|---|---|---|
| W1 | **Mục yokoten bị thiếu** — báo cáo nói còn "2 chỗ cùng kiểu chưa sửa" nhưng không liệt kê | Không biết vùng cross-bot nào còn hở → hỏi Dev trước khi chốt coverage |
| W2 | Verify mới ở mức **lint**, chưa chạy runtime; dev DB không kết nối được | Toàn bộ hành vi guard **chưa được Dev chứng minh bằng thao tác thật** |
| W3 | **Recover data chưa làm** — dữ liệu lệch `bot_id` phát sinh **trước fix** vẫn còn | Cần TC/query rà dữ liệu lệch (Studio đã có `REQ-012`), không chỉ test chặn phát sinh mới |
| W4 | Guard **cố ý bỏ qua** id rỗng / âm / không tồn tại | Vùng boundary rủi ro: `-11`, `-1111`, `0`, `999999999`, chuỗi không phải số |
| W5 | `step_message` không có `bot_id` → ownership tra gián tiếp qua `scenario.bot_id` | TC biến thể scenario phải dựng đúng quan hệ scenario ↔ step |
| W6 | Studio `REQ-016` (**xem trước tin nhắn con** phải giới hạn theo bot, nhãn `yokoten RK-01`) **KHÔNG có trong đánh giá của Dev** — và TC Studio `NEW-36` test đúng mục này đã **FAIL** ở run mới nhất (xem `04-tc-list.md`) | Nhiều khả năng là 1 trong 2 chỗ yokoten chưa sửa → **lỗ hổng cross-bot còn mở** |

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót) — **W1: mục yokoten thiếu**
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
