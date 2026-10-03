# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-filled từ Redmine #41714 (journal, KHÔNG phải Description — xem note dưới) qua `/new-task`.
> **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs.

⚠️ **Khác thường so với các ticket khác**: nội dung "Đánh giá ảnh hưởng" của ticket này **không nằm trong Description** (Description chỉ nêu yêu cầu ngắn) mà nằm trong **2 journal riêng**, vì fix trải trên **2 repo độc lập**:
- **Journal #139174 (Thanh Duy Nguyen, 2026-09-29)** — đánh giá ảnh hưởng phía **linect-service (Java)** — phần sinh mã trigger 15002 + set `status_sync=4`.
- **Journal #139180 (AI LME Fix bug, 2026-09-29)** — đánh giá ảnh hưởng phía **sns-line (PHP, web + app mobile API)** — phần nhận & hiển thị nhãn mã 15002.

Mục 1–4 dưới đây **hợp nhất cả 2 phần**, đánh dấu rõ theo từng repo. Nguyên văn đầy đủ 2 journal xem [01-bug-task.md](01-bug-task.md).

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Thanh Duy Nguyen (linect-service, Java) + AI LME Fix bug — Auto-fixbug (sns-line, PHP) |
| Commit / Pull Request | linect-service: `e4fa4ec027aa63917c8d4a84078f95789f759952` · sns-line: `cacd763d8a` |
| Branch | linect-service: `m_202609_api_feature_40041_39641` (⚠️ Dev ghi "chưa merge release" tại thời điểm viết journal) · sns-line: `ai_small_41714` (base `release_step_20260930`, đã push origin) |
| Ngày submit đánh giá | 2026-09-29 |
| Auto-filled | 2026-09-29 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại journal #139174 + #139180 trên Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact) của **cả 2 phần Java + web**.

---

## 1. Nguyên nhân

**[Web — journal #139180]** Job Java (linect-service) đã đổi nguồn action do hệ thống ngoài gọi qua API công khai sang mã trigger riêng 15002 thay cho 15001, đồng thời tự đánh status_sync=4 cho hai bảng lịch sử để job chuyển tiếp webhook bỏ qua. Phía web sns-line chưa biết mã 15002 nên mọi dòng lịch sử sinh từ API rơi vào nhánh mặc định và hiển thị sai thành thao tác tay. Riêng phần status_sync web không phải sửa vì web không ghi hai bảng này từ API.

**[Java — journal #139174, mục "Mục đích" — bản chất là lý do/business need của phần Java]**
- Bổ sung trigger type 15002 (APIからアクション) để lịch sử phân biệt được action do API ngoài gọi với action admin thao tác trên web (15001).
- tag_history / friend_info_history sinh từ API phải mang status_sync = 4 (IGNORE) để job forward webhook #40475 không bắn ngược thay đổi về chính bên thứ 3 vừa gọi API.

## 2. Cách fix

**[Java — #139174 mục 2]**
- Thêm `TriggerStartActionConstants.TYPE_API_ACTION = 15002`; `McpModel.requestDoAction` set `type_start_scenario` theo hằng số này thay cho "15001" hardcode.
- `HistoryHelper` set `status_sync = 4` ngay trong câu INSERT khi trigger = 15002 (không update sau khi insert vì job quét `status_sync IS NULL` sẽ hở race) và cho 15002 resolve được `trigger_from_name`; `ActionModel` mở thêm 15002 cho 2 nhánh vốn chỉ chạy với 15001 là update `last_message` của conversation và ghi message ブロック/非表示 vào chat.

**[Web — #139180 mục 2, bao gồm 1 vòng tự-review]**
Bổ sung mã trigger 15002 (APIからアクション) vào phía web sns-line: hằng nhãn dùng chung `SourceMessage::ACTION_API`; hằng `TRIGGER_API=15002` cho `TagHistory` và **chốt lại `TRIGGER_API` của `FriendInformationHistory` từ mã tạm 20001 sang 15002**; thêm nhánh nhận mã mới vào ba bảng nhãn lịch sử (lịch sử thẻ, lịch sử thông tin bạn bè, lịch sử hiển thị rich menu); cột người thao tác ở màn chi tiết bạn bè nhận 15002 để hiện tên chủ API key thay vì `自動`. Không đụng status_sync (job Java ghi lúc INSERT).

⚠️ **[Tự review v1 bổ sung — quan trọng]**: Thêm case 15002 vào `getDetailActionTrigger` của `ChatController.php` **và** `Api/ChatController.php`: AI đã kiểm chứng job Java **CÓ** ghi `source_messages.action_from` (`McpModel:402 → ActionModel:736 → MessageModel:229 setActionFrom`, `StartActionInfo` dùng `@SerializedName trigger_type/from_id` đúng key PHP đọc) nên tiền đề "ngoài-scope" của lần fix đầu là **sai**; thiếu nhánh này thì popup `送信元` ở chat 1:1 (**web + app mobile**) để trống — là **hồi quy** so với trước khi job đổi mã từ 15001 sang 15002. → Đây là bằng chứng cho thấy phạm vi fix ban đầu (chỉ 3 bảng nhãn lịch sử) **chưa đủ**, QA cần verify kỹ nhánh Chat 1:1 vì chính AI tự phát hiện gap này sau lần fix đầu.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Repo | Thay đổi (nếu có) | Lý do |
|---|---|---|---|---|
| 1 | `recordTagAdd` / `recordTagRemove` / `recordFriendInfo` (26 callsite ở `ActionModel`, `LineUserModel`, `BotLineUserModel`, `HandlePostbackTask`, `HandleImportCsvTask`) | linect-service (Java) | Không sửa | Giữ nguyên signature; `status_sync` suy ra từ tham số trigger đã có sẵn |
| 2 | `resolveTriggerFromName` (private, 3 callsite nội bộ `HistoryHelper`: `recordTag`, `recordFriendInfo`, `recordRichMenu`) | linect-service (Java) | Mở rộng resolve cho trigger 15002 | Kéo theo `rich_menu_history` cũng resolve được `trigger_from_name` cho trigger 15002 |
| 3 | `App\Models\TagHistory::getTriggerAttribute` | sns-line (PHP) | Thêm case 15002 → nhãn `APIからアクション` | Đã check, đã sửa |
| 4 | `App\Models\FriendInformationHistory::getTriggerAttribute` | sns-line (PHP) | Đổi hằng `TRIGGER_API` 20001→15002 + thêm case nhãn | Đã check, đã sửa |
| 5 | `App\Traits\ResolveTriggerTypeTrait::resolveTriggerTypeLabel` | sns-line (PHP) | Thêm case 15002 | Dùng chung cho lịch sử hiển thị rich menu |
| 6 | `App\Services\FriendDetailFriendInfoService::transformHistoryRow` | sns-line (PHP) | Thêm 15002 vào `in_array` cùng 15001 | Cột `操作者` hiện tên chủ API key thay vì `自動` |
| 7 | `App\Services\FriendDetailService::getRichmenuHistory` | sns-line (PHP) | Không sửa (chỉ đối chiếu) | Caller của trait #5, chỉ đọc |
| 8 | `sns.line.helper.HistoryHelper.recordTag` / `recordFriendInfo` | linect-service (Java) | Không sửa (chỉ đối chiếu) | Phía ghi `status_sync=4`, web chỉ đối chiếu |
| 9 | `ChatController.php::getDetailActionTrigger` (web) | sns-line (PHP) | Thêm case 15002 — **bổ sung ở tự-review v1**, KHÔNG có trong đánh giá ban đầu | Tránh popup `送信元` chat 1:1 web để trống (hồi quy) |
| 10 | `Api/ChatController.php::getDetailActionTrigger` (app mobile) | sns-line (PHP) | Thêm case 15002 — **bổ sung ở tự-review v1** | Đồng bộ nhãn với bản web cho app mobile |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Repo | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|---|
| F1 | `McpModel.requestDoAction` | (linect-service) | Java | Direct | Set `type_start_scenario` = `TYPE_API_ACTION` (15002) thay hardcode 15001 |
| F2 | `ActionModel.doAction(ActionLineUser)` + overload chính | (linect-service) | Java | Direct | Mở nhánh 15002 cho update `last_message` + ghi message block/hide |
| F3 | `HistoryHelper.recordTag` / `recordFriendInfo` | (linect-service) | Java | Direct | Set `status_sync=4` khi trigger=15002 ngay lúc INSERT |
| F4 | `HistoryHelper.resolveTriggerFromName` (private) + `HistoryHelper.resolveStatusSyncForApi` (mới) | (linect-service) | Java | Direct | Resolve tên cho trigger 15002; kéo theo `recordRichMenu` |
| F5 | `App\SourceMessage` — hằng `ACTION_API` | `app/SourceMessage.php` | PHP | Direct | Nhãn dùng chung `APIからアクション`, đổi 1 nơi ảnh hưởng nhiều màn |
| F6 | `App\Models\TagHistory::getTriggerAttribute` | `app/Models/TagHistory.php` | PHP | Direct | Ảnh hưởng bảng タグ履歴 (tag history) ở màn chi tiết bạn bè |
| F7 | `App\Models\FriendInformationHistory::getTriggerAttribute` | `app/Models/FriendInformationHistory.php` | PHP | Direct | Đổi hằng `TRIGGER_API` 20001→15002 — rủi ro nếu còn nơi khác hardcode 20001 |
| F8 | `App\Traits\ResolveTriggerTypeTrait::resolveTriggerTypeLabel` | `app/Traits/ResolveTriggerTypeTrait.php` | PHP | Direct | Dùng chung ở `FriendDetailService` cho lịch sử hiển thị rich menu |
| F9 | `App\Services\FriendDetailFriendInfoService::transformHistoryRow` | `app/Services/FriendDetailFriendInfoService.php` | PHP | Direct | Cột `操作者` đổi behavior — cần regression cho action nguồn khác không bị đổi nhầm |
| F10 | `App\Services\FriendDetailService::getRichmenuHistory` | `app/Services/FriendDetailService.php` | PHP | Indirect | Caller của F8, chỉ đọc |
| F11 | `ChatController.php` + `Api/ChatController.php` :: `getDetailActionTrigger` | `app/Http/Controllers/ChatController.php`, `app/Http/Controllers/Api/ChatController.php` | PHP | Direct | Bổ sung ở tự-review v1 — popup `送信元` chat 1:1 (web **và** app mobile), phủ cả action block/hide/favorite |

### 4.2. List data bị update khi fix bug

| # | Data (table.column) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `tag_history.trigger_type_start` (giá trị mới 15002) | Java: WRITE lúc INSERT · Web: chỉ READ để hiện nhãn | |
| D2 | `friend_info_history.trigger_type_start` (giá trị mới 15002) | Java: WRITE lúc INSERT · Web: chỉ READ | Hằng `TRIGGER_API` đổi 20001→15002 — AI ghi "không có dòng dữ liệu nào mang 20001" nhưng **chưa verify được trên DB thật** (kết nối MySQL dev bị từ chối lúc chạy verify) |
| D3 | `rich_menu_history.trigger_type_start` (giá trị mới 15002, qua trait dùng chung F8) | Web: chỉ READ | Không có dòng data thực tế nào mang 15002 trừ khi job Java cũng gán cho rich menu — cần QA xác nhận job Java có ghi trigger 15002 vào `rich_menu_history` không |
| D4 | `tag_history.status_sync` / `friend_info_history.status_sync` (set = 4 khi trigger=15002) | Java: WRITE lúc INSERT | **MIGRATE bắt buộc trước deploy**: cột `status_sync` phải tồn tại (migration #40475, `ALTER TABLE ... ADD COLUMN status_sync tinyint DEFAULT NULL`) — thiếu cột thì INSERT lịch sử sẽ **fail** |
| D5 | `source_messages.action_from` | Web: chỉ READ (không có `setActionFrom` mới) | Dùng cho popup `送信元` chat 1:1 — Java đã ghi từ trước, web chỉ thêm nhánh đọc case 15002 (F11) |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Lịch sử thẻ — Tag Management (FA-012) | F3, F4, F6, D1 | Medium — hiện đúng nhãn nguồn API thay vì `手動` |
| T2 | Lịch sử thông tin bạn bè — Friend Information (FA-015), cột `操作者` | F3, F4, F7, F9, D2 | Medium — nhãn + tên người thao tác |
| T3 | Lịch sử hiển thị rich menu — Rich Menu (FA-004) | F4, F8, D3 | Low — chỉ thêm nhãn qua trait dùng chung, cần xác nhận có data thực tế mang 15002 không |
| T4 | Job forward webhook (#40475) | D4 | **High** — nếu `status_sync` không set đúng lúc INSERT sẽ forward ngược webhook cho bên thứ 3 gây loop |
| T5 | Chat 1:1 (web + app mobile) khi action qua API — popup `送信元`, `last_message`, message block/hide | F2, F11, D5 | **High** — đây chính là gap AI tự phát hiện ở tự-review v1; nếu regression tái xuất hiện thì popup để trống |
| T6 | API `/do_action` (nguồn ghi ban đầu) | F1 | Medium — đúng mã trigger + `status_sync` cho record mới sinh |
| T7 | Regression các nguồn trigger **cũ** (thao tác tay 15001, scenario, import CSV, remind, broadcast) trên cả 3 bảng nhãn lịch sử + modal trigger | F5–F9, F11 (đường "else"/default) | **High** — RULE bắt buộc của Dev (#139174 mục 4.3 dòng cuối): các nguồn cũ phải giữ nguyên nhãn + `status_sync NULL` + vẫn được forward webhook |

📌 **Tham khảo thêm (không phải nguồn chính)**: MCP LME TEST STUDIO task #341 đã tự phân tích diff code (`spec_delta`/`dev_impact`) và sinh **12 `requirement_keys`** (REQ-001 → REQ-012, kèm risk High/Medium/Low) khớp khá sát với 4.1–4.3 ở trên, cộng thêm 2 điểm mục 4 ở trên **chưa liệt kê rõ**: REQ-007 (modal `開始トリガー` ở step delivery của màn 友だち情報詳細) và REQ-009 (đảm bảo không còn data mang mã tạm 20001 — trùng lưu ý ở D2). `/review-tc` sẽ tự fetch lại section này khi review, không cần copy 12 requirement vào đây.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
- [ ] **Riêng ticket này**: đã confirm branch Java `m_202609_api_feature_40041_39641` **đã merge vào release cùng đợt** với branch web `ai_small_41714` trước khi test end-to-end (nếu chưa merge, môi trường test sẽ KHÔNG tái hiện được mã trigger 15002 / status_sync=4 phía Java)
