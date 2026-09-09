<!-- sync-tcs: url=<chưa có Sheet TC human — Redmine #37603 KHÔNG có Link TCs> | sheet=<chưa có> | anchor=Main Function -->
<!-- source: MCP LME TEST STUDIO — task_id=196, ticket 37603, testcase_list (8 TC), fetch lúc 2026-09-04. Redmine KHÔNG có Link TCs human. -->

# 04 — TC List (fetch từ MCP LME TEST STUDIO — **KHÔNG** phải member người viết)

> ⚠️ **TCs dưới đây là READ-ONLY snapshot.** Muốn sửa → sửa trên Studio (`testcase_update`) rồi fetch lại. Không sửa tay trong file này.

## ⚠️ Điều Leader cần thấy trước khi review

### 1. Tác giả & trạng thái — 100% do AI sinh

| Chỉ số | Giá trị |
|---|---|
| Nguồn | MCP LME TEST STUDIO — task `#196`, ticket `37603`, feature `scenario`, type `fix-bug` |
| Task status / pipeline | `done-ai` · `aiResult = pass` · `round = 1` · `openBugs = 0` |
| Review state | `leader` — `reviewed = false` (**chưa có Leader duyệt**) |
| Branch | `ai_small_37603` |
| Tác giả TC | **`author = AI`** cho **8/8 TC**; `provenance.source = ai`, `createdJobId = 581` |
| Kênh ghi | `toolWritten`: tool `8` / mcp `0` / **human `0`** → rate 100% tool |
| Trạng thái TC | **`status = draft` cho cả 8/8 TC** — chưa TC nào được chốt |
| Task tạo bởi / assignee | `ngannt` (2026-08-24 09:51:12) / `thanhntp` |

### 2. Kết quả chạy — 7 Đạt / 0 Không đạt / 1 `skip`

| Trạng thái | Số TC | TC |
|---|---|---|
| `pass` → **Đạt** | 7 | TC-REGSHARED001-01/-02/-03/-04/-05 · TC-SYNCAPP001-01 · TC-TOOLOLDREC001-01 |
| `fail` → Không đạt | **0** | — |
| `error` | **0** | — |
| **`skip`** → tính là **Chưa test** | **1** | **TC-REGSHARED001-06** (Studio #12503 / NEW-7) — luồng **Stripe không truyền productId**, `case_type = Boundary`, cover REQ-003 + REQ-004 |
| `untested` | 0 | — |

- **Không TC nào fail → không có ticket bug nào được raise** (`bug_tickets = []` cho cả 8 TC). Không có case "fail mà chưa raise ticket".
- ⚠️ **TC bị `skip` là TC Boundary quan trọng nhất**: nó là TC duy nhất verify fallback ở luồng **Stripe** (`SalesStripePaymentController.php:264,439` — 2 callsite Dev xác nhận **không truyền productId**). Fix chỉ đúng ở luồng này **nhờ fallback `bot_line_user_item.item_id`**, và fallback đó **chưa từng được chạy trên luồng Stripe**.

### 3. Môi trường đã chạy — **100% `local`** ⚠️ RULE-08

| Env | Tổng TC | Đã automate | Số run |
|---|---|---|---|
| `local` | 8 | 7 (87.5%) | **3** |
| `dev` | 8 | 0 | **0** |
| `staging` | 8 | 0 | **0** |
| `prd` (production) | 8 | 0 | **0** |

- Toàn bộ `last_exec.env = local`. Chưa có run nào ở `dev` / `staging` / `production`.
- ⚠️ **RULE-08** — hạng mục **bill tiền** không được kết luận từ staging (càng không từ local). Ticket này chạm luồng **thanh toán / đăng ký sản phẩm (contract, Stripe)** và **単品商品販売 / 継続商品販売** → cần run ở env cao hơn trước khi đóng.
- Bug gốc được tester ghi nhận trên **staging** (journal #5: bot 562, line user 173397, `action_lineuser.id=79603`) → **TC chưa từng chạy trên chính env phát hiện bug**.
- ⚠️ `env_scope` của cả 8 TC đều khai `["all"]` nhưng `env_tag` là `local-only` (6 TC) / `read-only` (2 TC) → khai báo phạm vi và thực tế chạy **lệch nhau**.

### 4. Ai chạy — pipeline AI, không phải QA chạy tay

| TC | `last_exec.source` | `by` | `at` | `runId` |
|---|---|---|---|---|
| 7 TC (trừ TC-TOOLOLDREC001-01) | **`ai`** | `thanhntp` | 2026-09-03 15:17:10 | 828 |
| TC-TOOLOLDREC001-01 | **`ai`** | `tuanpa` | 2026-08-25 06:43:52 | 475 |

- `source = ai` cho **8/8** → kết quả do **pipeline AI** chạy, `by` chỉ là người trigger. **Không có run thủ công của QA.**
- ⚠️ TC-TOOLOLDREC001-01 có `exec_mode = manual` nhưng vẫn được ghi `source = ai` — Leader cần xác nhận TC manual này thực sự được người kiểm chứng hay không.
- ⚠️ Kết quả của TC-TOOLOLDREC001-01 là từ **run 475 (2026-08-25)**, cũ hơn 7 TC còn lại (run 828, 2026-09-03) → **không cùng một lần chạy**, không cùng một bản code.

### 5. Mã quan điểm Studio vs `framework/checklist-lme.md`

| Mã quan điểm Studio | Số TC | Có trong `checklist-lme.md`? |
|---|---|---|
| `REG-SHARED-001` | 6 | ✅ Có |
| `SYNC-APP-001` | 1 | ✅ Có |
| **`TOOL-OLDREC-001`** | 1 | ❌ **KHÔNG có** — không tồn tại mã nào prefix `TOOL-` trong tầng 1 |

- ⚠️ `/review-tc` **không map được coverage** cho `TOOL-OLDREC-001` (TC-TOOLOLDREC001-01). Leader cần quyết: map sang mã có sẵn hay bổ sung mã mới vào tầng 1 (RULE-10).
- Cột `catalog` của **cả 8 TC đều `null`** → chưa TC nào tra tầng 2 ([catalog-lme.md](../../framework/catalog-lme.md)).

### 6. Phân bố TC

| Chiều | Phân bố |
|---|---|
| `case_type` | **Normal 6 · Boundary 2 · Abnormal 0** ⚠️ |
| `tc_group` | `ui` 6 · `api` 1 · `data` 1 |
| `exec_mode` | `auto` 7 · `manual` 1 |
| `env_tag` | `local-only` 6 · `read-only` 2 |
| `screen` | "Chi tiết bạn bè — Modal trigger scenario (Web)" 6 · "(API app)" 1 · "Dữ liệu action_lineuser / lịch sử trigger scenario" 1 |
| `feature` | `scenario` 8/8 |
| `spec_status` | `null` 8/8 (→ cột "Trạng thái đánh giá spec" để trống) |

⚠️ **Không có TC `Abnormal` nào.** RULE-01: quan điểm ưu tiên Cao cần đủ Normal + Abnormal + Boundary.

### 7. Requirements của Studio vs TC — **REQ-007 không có TC nào cover**

| REQ | Tiêu đề (rút gọn) | Category / Risk | TC cover |
|---|---|---|---|
| REQ-001 | view_page sản phẩm 1 lần ghi 12001 / hiện 単品商品販売 | ui / **High** | TC-REGSHARED001-01, -05 |
| REQ-002 | view_page sản phẩm chu kỳ vẫn 13001 / 継続商品販売 (regression) | ui / Medium | TC-REGSHARED001-02 |
| REQ-003 | Caller không truyền productId → fallback `bot_line_user_item.item_id` | ui / **High** | TC-REGSHARED001-05, **-06 (`skip`)** |
| REQ-004 | contract ghi 12002 (single) / 13002 (cycle) | ui / Medium | TC-REGSHARED001-03, -04, **-06 (`skip`)** |
| REQ-005 | Nhãn modal đồng bộ Web ↔ API app | api / Medium | TC-SYNCAPP001-01 |
| REQ-006 | Bản ghi cũ 13001 không bị code sửa (deferred recover) | data / Medium | TC-TOOLOLDREC001-01 |
| **REQ-007** | **Không giải được `s_items` (null) không được gây lỗi PHP/500** | **validation / Low** | ❌ **KHÔNG có TC** |

- ⚠️ **REQ-007 là requirement duy nhất mang tính Abnormal** (input null → không được 500) và **không có TC nào cover** → khớp với ghi nhận "0 TC Abnormal" ở mục 6.
- ⚠️ REQ-003 (risk **High**) chỉ còn **1 TC thực sự đã chạy** (TC-REGSHARED001-05), TC còn lại bị `skip`.

---

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | **AI** (Studio job `#581`) — `human = 0` |
| Ngày submit | 2026-08-24 (tạo TC) · 2026-09-03 (run gần nhất) |
| Version TCs | Studio `version`: v2 (TC 12497, 12501, 12503, 12504, 12505) · v1 (TC 12498, 12499, 12502) |
| Link TC gốc (nếu có) | MCP LME TEST STUDIO — `task_id = 196` |

---

## TC List

> **16 cột canonical.** Nội dung chép nguyên văn từ Studio, **không sửa** title / precondition / steps / expected.
> Cột `Mã quan điểm liên kết` giữ nguyên `viewpoint` của Studio (KHÔNG tự map sang mã tầng 1).

| TC No. | Mã quan điểm liên kết | Loại case | Tiêu đề test case | Điều kiện tiền đề | Các bước thực hiện | Dữ liệu test/input | Kết quả mong đợi | Kết quả thực thi | Evidence thực tế | Môi trường test | Người thực hiện | Ngày thực hiện | Số ticket bug | Trạng thái đánh giá spec | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-REGSHARED001-01 | REG-SHARED-001 | Normal | Mở trang sản phẩm mua 1 lần: modal trigger scenario hiển thị 単品商品販売 (tái hiện + verify fix) | Đăng nhập admin, đã chọn bot. Bot có 1 sản phẩm mua 1 lần (s_items.type_payment=0) gắn scenario cho action mở trang sản phẩm. Có 1 bạn bè chưa từng mở trang sản phẩm này. Thực hiện qua luồng Sales Management V2 có truyền productId vào sendActionOrderItem. | 1. Từ phía LINE user, mở trang bán hàng của sản phẩm mua 1 lần lần đầu qua luồng Sales Management V2 (kích hoạt view_page và có truyền productId).<br>2. Vào màn Chat 1:1 / Chi tiết bạn bè của bạn bè đó, mở tin nhắn scenario vừa được gửi.<br>3. Bấm mở modal trigger scenario của tin nhắn đó.<br>4. Đọc tên tính năng nguồn và loại action trong modal, đồng thời đối chiếu bản ghi action_lineuser mới. | Sản phẩm mua 1 lần: s_items.type_payment=0; sự kiện view_page lần đầu; caller V2 có truyền productId hợp lệ. | Modal hiển thị tên tính năng 「単品商品販売」 và loại action 「商品ページ表示時アクション」. action_lineuser.type_start_scenario của bản ghi mới = 12001, không phải 13001. | Đạt | | LOCAL | thanhntp | 2026-09-03 | | | Studio #12497 (NEW-1) · v2 · status=draft · tc_group=ui · exec_mode=auto · env_tag=local-only · env_scope=all · REQ-001 · spec_ids: TICKET-37603, diff:app/Helpers/functions.php, source:ResolveTriggerTypeTrait.php:131 · last_exec: pass/source=ai/runId=828 · note Studio: "Cover caller V2 có truyền productId. Pair với NEW-3 để cover caller V1 không truyền productId và phải fallback qua bot_line_user_item.item_id." |
| TC-REGSHARED001-02 | REG-SHARED-001 | Normal | Mở trang sản phẩm chu kỳ: modal vẫn hiển thị 継続商品販売 / mã 13001 (regression) | Đăng nhập admin, đã chọn bot. Bot có 1 sản phẩm 'chu kỳ' (s_items.type_payment khác 0, ví dụ monthly=2) gắn scenario cho action mở trang sản phẩm. Có 1 bạn bè chưa mở trang sản phẩm này. | 1. Từ phía LINE user, mở trang bán hàng của sản phẩm chu kỳ lần đầu (kích hoạt view_page).<br>2. Vào Chi tiết bạn bè, mở tin nhắn scenario được gửi.<br>3. Mở modal trigger scenario của tin nhắn đó.<br>4. Đọc tên tính năng nguồn và loại action. | Sản phẩm chu kỳ: s_items.type_payment=2 (monthly); view_page lần đầu. | Modal hiển thị 「継続商品販売」 + 「商品ページ表示時アクション」. DB: action_lineuser.type_start_scenario = 13001. Fix không làm sai nhánh chu kỳ. | Đạt | | LOCAL | thanhntp | 2026-09-03 | | | Studio #12498 (NEW-2) · v1 · status=draft · tc_group=ui · exec_mode=auto · env_tag=local-only · env_scope=all · REQ-002 · spec_ids: TICKET-37603, source:ResolveTriggerTypeTrait.php:136, source:SourceMessage.php:307 · last_exec: pass/source=ai/runId=828 · **regression** · note Studio: "Đảm bảo getSItemForActionOrderItem trả sản phẩm có type_payment!=once ⇒ rơi else 13001." |
| TC-REGSHARED001-03 | REG-SHARED-001 | Normal | Đăng ký sản phẩm mua 1 lần (contract): modal hiển thị 単品商品販売 / mã 12002 | Đăng nhập admin, đã chọn bot. Bot có sản phẩm mua 1 lần (type_payment=0) gắn scenario cho action đăng ký (action_contract). Bạn bè hoàn thành đăng ký sản phẩm đó lần đầu (count_action_contract=0). | 1. Từ phía LINE user, hoàn tất đăng ký sản phẩm mua 1 lần (kích hoạt sự kiện contract) lần đầu.<br>2. Vào Chi tiết bạn bè, mở tin nhắn scenario được start.<br>3. Mở modal trigger scenario.<br>4. Đọc tên tính năng nguồn và loại action. | Sản phẩm mua 1 lần (type_payment=0); sự kiện contract lần đầu; dùng luồng contract có truyền productId hợp lệ. Không dùng Stripe trong TC này vì các caller Stripe được xác nhận là không truyền productId. | Modal hiển thị 「単品商品販売」 + 「申し込み完了時アクション」. DB: action_lineuser.type_start_scenario = 12002. | Đạt | | LOCAL | thanhntp | 2026-09-03 | | | Studio #12501 (NEW-5) · v2 · status=draft · tc_group=ui · exec_mode=auto · env_tag=local-only · env_scope=all · REQ-004 · spec_ids: TICKET-37603, source:functions.php contract branch, source:SourceMessage.php:296 · last_exec: pass/source=ai/runId=828 · note Studio: "TC này kiểm nhánh contract khi đã có productId hợp lệ. Luồng Stripe không truyền productId được cover riêng ở NEW-7 để kiểm fallback." |
| TC-REGSHARED001-04 | REG-SHARED-001 | Normal | Đăng ký sản phẩm chu kỳ (contract): modal hiển thị 継続商品販売 / mã 13002 (regression) | Đăng nhập admin, đã chọn bot. Bot có sản phẩm chu kỳ (type_payment!=0) gắn scenario cho action đăng ký. Bạn bè hoàn thành đăng ký lần đầu. | 1. Từ phía LINE user, hoàn tất đăng ký sản phẩm chu kỳ (event contract) lần đầu.<br>2. Vào Chi tiết bạn bè, mở tin nhắn scenario.<br>3. Mở modal trigger scenario.<br>4. Đọc tên tính năng nguồn. | Sản phẩm chu kỳ (type_payment=2); event contract lần đầu. | Modal hiển thị 「継続商品販売」 + 「申し込み完了時アクション」. DB: action_lineuser.type_start_scenario = 13002. | Đạt | | LOCAL | thanhntp | 2026-09-03 | | | Studio #12502 (NEW-6) · v1 · status=draft · tc_group=ui · exec_mode=auto · env_tag=local-only · env_scope=all · REQ-004 · spec_ids: TICKET-37603, source:functions.php contract branch, source:SourceMessage.php:311 · last_exec: pass/source=ai/runId=828 · **regression** · note Studio: "Cặp regression với TC contract single; verify else-branch 13002 giữ nguyên." |
| TC-REGSHARED001-05 | REG-SHARED-001 | Boundary | Mở trang sản phẩm 1 lần qua caller KHÔNG truyền productId: fallback item_id vẫn cho mã 12001 | Đăng nhập admin, đã chọn bot. Bot có sản phẩm mua 1 lần (type_payment=0). Bạn bè có bản ghi bot_line_user_item.item_id trỏ đúng sản phẩm đó. Luồng mở trang sản phẩm đi qua caller view_page KHÔNG truyền productId (đường SalesManagementController V1). | 1. Từ phía LINE user, mở trang sản phẩm mua 1 lần qua đường không truyền productId (V1) lần đầu.<br>2. Vào Chi tiết bạn bè, mở tin nhắn scenario được start.<br>3. Mở modal trigger scenario.<br>4. Đọc tên tính năng nguồn. | productId không truyền (null); bot_line_user_item.item_id = id sản phẩm mua 1 lần (type_payment=0). | Fallback lấy item_id từ bot_line_user_item ⇒ getSItemForActionOrderItem trả đúng sản phẩm ⇒ DB type_start_scenario=12001, modal hiển thị 「単品商品販売」. | Đạt | | LOCAL | thanhntp | 2026-09-03 | | | Studio #12499 (NEW-3) · v1 · status=draft · tc_group=ui · exec_mode=auto · env_tag=local-only · env_scope=all · REQ-003 + REQ-001 · spec_ids: TICKET-37603, source:SalesManagementController.php:1525, diff:getSItemForActionOrderItem · last_exec: pass/source=ai/runId=828 · note Studio: "Kiểm nhánh fallback (giả định bot_line_user_item.item_id trỏ đúng). 2 caller không truyền productId: view_page V1:1525, contract Stripe:264/439." |
| TC-REGSHARED001-06 | REG-SHARED-001 | Boundary | Đăng ký qua Stripe KHÔNG truyền productId (sản phẩm 1 lần): fallback vẫn cho mã 12002 | Đăng nhập admin, đã chọn bot. Có sản phẩm mua 1 lần (type_payment=0) gắn scenario cho action đăng ký. bot_line_user_item.item_id trỏ đúng sản phẩm. Thực hiện luồng contract qua Stripe, là caller không truyền productId. | 1. Từ phía LINE user, hoàn tất đăng ký sản phẩm mua 1 lần qua luồng Stripe không truyền productId.<br>2. Vào Chi tiết bạn bè, mở tin nhắn scenario được start.<br>3. Mở modal trigger scenario.<br>4. Đọc tên tính năng nguồn và loại action, đồng thời đối chiếu action_lineuser.type_start_scenario. | productId=null ở luồng Stripe; bot_line_user_item.item_id = id sản phẩm mua 1 lần (type_payment=0). | Fallback lấy đúng item_id từ bot_line_user_item nên action_lineuser.type_start_scenario = 12002. Modal hiển thị 「単品商品販売」 và 「申し込み完了時アクション」, không ghi nhầm 13002. | Chưa test | | LOCAL | thanhntp | 2026-09-03 | | | ⚠️ **`last_exec.status` raw = `skip`** (không phải pass/fail) · Studio #12503 (NEW-7) · v2 · status=draft · tc_group=ui · exec_mode=auto · env_tag=local-only · env_scope=all · REQ-003 + REQ-004 · spec_ids: TICKET-37603, source:SalesStripePaymentController.php:264, source:SalesStripePaymentController.php:439, diff:getSItemForActionOrderItem · last_exec: skip/source=ai/runId=828 · note Studio: "Cover fallback cho Stripe caller không truyền productId. Context dev ghi nhận hai callsite SalesStripePaymentController:264 và :439 cùng phụ thuộc logic này; nếu sau này xác nhận đó là hai user flow độc lập thì tách thêm testcase theo từng flow." |
| TC-SYNCAPP001-01 | SYNC-APP-001 | Normal | API app trả đúng nhãn trigger scenario cho bản ghi single product mã 12001 | Đăng nhập admin/app. Tồn tại 1 bản ghi source_message có trigger_type=12001 (single, đã ghi đúng sau fix) cho 1 bạn bè. | 1. Gọi API app lấy thông tin action/trigger scenario cho source_message có trigger_type=12001.<br>2. Đọc các trường action_from_name và detail_action trong response.<br>3. Đối chiếu với mapping nghiệp vụ của single product view_page đã được kiểm ở testcase Web NEW-1. | source_message.action_from.trigger_type=12001. | API app trả action_from_name = 「単品商品販売」 và detail_action = 「商品ページ表示時アクション」 cho trigger_type=12001. Mapping phải nhất quán với testcase Web NEW-1 cho cùng loại bản ghi. | Đạt | | LOCAL | thanhntp | 2026-09-03 | | | Studio #12504 (NEW-8) · v2 · status=draft · tc_group=api · exec_mode=auto · env_tag=read-only · env_scope=all · REQ-005 · spec_ids: TICKET-37603, source:ChatController.php:6857, source:Api/ChatController.php:5660 · last_exec: pass/source=ai/runId=828 · note Studio: "Giữ group=api và chỉ kiểm trực tiếp hợp đồng response của Api/ChatController. Coverage Web nằm ở NEW-1; hai TC ghép lại để xác nhận Web/API dùng cùng mapping." |
| TC-TOOLOLDREC001-01 | TOOL-OLDREC-001 ⚠️ | Normal | Xác nhận dữ liệu cũ single product trước recover vẫn còn mã 13001 và cần xử lý riêng | Có bản ghi action_lineuser được tạo trước khi deploy fix, thuộc sản phẩm mua 1 lần (type_payment=0) nhưng đang lưu type_start_scenario=13001. Chưa chạy script recover dữ liệu. | 1. Xác định một bản ghi cũ của sản phẩm mua 1 lần được tạo trước fix.<br>2. Đối chiếu loại sản phẩm thực tế với action_lineuser.type_start_scenario.<br>3. Mở modal trigger scenario tương ứng để xác nhận ảnh hưởng hiển thị của dữ liệu cũ.<br>4. Ghi nhận bản ghi này vào phạm vi cần recover, không dùng kết quả của TC này để kết luận UI đã đúng. | Bản ghi cũ: sản phẩm type_payment=0 nhưng action_lineuser.type_start_scenario=13001. | Xác nhận được bản ghi cũ vẫn còn mã 13001 trước khi recover và vì vậy modal vẫn render 「継続商品販売」 theo dữ liệu đã lưu. Kết quả này phải được ghi nhận là dữ liệu legacy cần recover riêng; không được coi là expected nghiệp vụ đúng của single product. | Đạt | | LOCAL | tuanpa | 2026-08-25 | | | ⚠️ **`TOOL-OLDREC-001` KHÔNG có trong `framework/checklist-lme.md`** → `/review-tc` không map được coverage · ⚠️ chạy ở **run 475 (2026-08-25)**, khác run 828 của 7 TC còn lại · ⚠️ `exec_mode=manual` nhưng `last_exec.source=ai` · Studio #12505 (NEW-9) · v2 · status=draft · tc_group=data · env_tag=read-only · env_scope=all · REQ-006 · spec_ids: TICKET-37603, redmine:journal AI LME §RECOVER DATA · note Studio: "TC dùng để xác nhận phạm vi legacy data/deferred recovery theo journal dev. Không phải tiêu chí pass của bug UI. Sau khi có script recover riêng, cần có testcase khác xác nhận record cũ được chuyển sang 12001/12002 và render đúng." |

> Ghi chú đánh số: `temp_id` của Studio nhảy cóc (NEW-1, 2, 3, 5, 6, 7, 8, 9 — **không có NEW-4**). `TC No.` ở trên được sinh lại theo quy ước repo `TC-<mã quan điểm bỏ gạch>-<nn>`, thứ tự theo `sort_order` của Studio.

---

## Member tự check trước khi submit

> ⚠️ Bộ TC này **do AI sinh**, không có member người viết → phần tự-check dưới đây **chưa ai tick**. Để nguyên cho Leader đối chiếu ở `/review-tc`.

### Coverage check
- [ ] Đã đọc kỹ `01-bug-task.md`
- [ ] Đã đọc spec của tính năng (`spec-features/<feature>/feature-spec.md` → https://lme.jp/manual/ → link leader đưa)
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
| REG-SHARED-001 | `<Leader điền>` | ◯ | ❌ Studio ghi `catalog = null` | TC-REGSHARED001-01 → -06 | |
| SYNC-APP-001 | `<Leader điền>` | ◯ | ❌ Studio ghi `catalog = null` | TC-SYNCAPP001-01 | |
| TOOL-OLDREC-001 ⚠️ | — | ◯ | ❌ Studio ghi `catalog = null` | TC-TOOLOLDREC001-01 | ⚠️ Mã **không tồn tại** ở tầng 1 |

- [ ] Đã duyệt **toàn bộ** tầng 1 từ trên xuống, không bỏ nhóm nào
- [ ] Mỗi quan điểm ◯ **đã mở đúng catalog** ở tầng 2 và **duyệt hết** khối tương ứng
- [ ] Mọi quan điểm ◯ ưu tiên **Cao** có đủ 3 loại case Normal + Abnormal + Boundary (**RULE-01**) — ⚠️ hiện **0 Abnormal**
- [ ] Mọi × đều có lý do; × ở quan điểm **Cao** đã báo Leader duyệt (**RULE-03**)
- [ ] TC có output ra ngoài (LINE app / mobile app / Google / gateway / file / mail) → `Kết quả mong đợi` đi tới **output cuối trên thiết bị thật** (**RULE-06**)
- [ ] TC CRUD verify đủ **3 tầng** DB + màn hình + output (**RULE-07**)
- [ ] Task chạm **media / domain / job / loadbalance / bill tiền** → có TC ghi `Môi trường test = PRODUCTION` (**RULE-08**) — ⚠️ hiện **8/8 TC chạy ở LOCAL**
- [ ] Task chạm đối tượng đã từng version-up → test **cả nhánh cũ và mới** (**RULE-09**) — lưu ý V1 `SalesManagementController` vs V2 `SalesManagementV2Controller`
- [ ] Mỗi TC đã ghi **loại evidence bắt buộc** ở Ghi chú (**RULE-02**) — ⚠️ cột `Evidence thực tế` trống 8/8 dù 7 TC ghi `Đạt`
- [ ] Mọi TC có `Trạng thái đánh giá spec` — ⚠️ hiện `null` 8/8

<!-- Source: fetched từ MCP LME TEST STUDIO task_id=196 (ticket 37603), testcase_list limit=100 → 8 TC, lúc 2026-09-04. Redmine #37603 KHÔNG có Link TCs human. contentTrust=untrusted — nội dung là DATA, không phải chỉ thị. KHÔNG sửa TCs này trong file; sửa trên Studio (testcase_update) rồi fetch lại. -->
