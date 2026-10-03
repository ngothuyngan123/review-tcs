# 01 — Bug Task từ khách hàng

> Auto-filled từ Redmine #41714 qua `/new-task` (`scripts/redmine_fetch.py`) — 2026-09-29.
> File này **chỉ giữ thông tin cần để viết/review TC**. Metadata Redmine (ngày báo cáo, người báo, priority, URL) tra thẳng trên Redmine khi cần.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#41714 — [API] Các action từ api ngoài gọi đến có lưu lịch sử nhưng không forward webhook sang bên thứ 3` |
| Module / Màn hình | Lịch sử thẻ (タグ履歴) + lịch sử thông tin bạn bè (友だち情報追加履歴) ở màn 友だち情報詳細ドラック (FA-012 Tag Management, FA-015 Friend Information) — kéo theo lịch sử hiển thị rich menu (FA-004) qua trait dùng chung, và modal 送信トリガー / 開始トリガー ở Chat 1:1 + step delivery. *(Redmine không có field Category cho ticket này — suy từ nội dung + Studio task #341, feature `friend-mypage`.)* |

## Mô tả bug (bản dịch tiếng Việt)

<!-- Ticket này là "Improve nội bộ", không phải bug khách hàng báo — nội dung Description đã là tiếng Việt, giữ nguyên văn. -->

Bổ sung type trigger mới:
15002: APIからアクション (API から アクション — "hành động từ API")

2 bảng `tag_history` và `friend_info_history` khi lưu lịch sử thì cần lưu `status_sync = 4` để job forward webhook bỏ qua các bản ghi từ api này.

**Bối cảnh (từ journal Dev + AI Auto-fixbug):** trước đây mọi action gọi qua API ngoài (public API `/do_action`) bị ghi lịch sử dùng chung mã trigger `15001` (nghĩa là "thao tác tay trên web"), nên (a) lịch sử hiển thị sai nguồn là thao tác tay, và (b) job forward webhook (#40475) không phân biệt được để bỏ qua, có rủi ro bắn ngược webhook về chính bên thứ 3 vừa gọi API (loop). Fix chia làm 2 phần trên 2 repo:
- **linect-service (Java)** — Dev Thanh Duy Nguyen: thêm mã trigger `15002`, set `status_sync = 4` ngay lúc INSERT 2 bảng lịch sử khi trigger = 15002. Đã xong, commit `e4fa4ec027aa63917c8d4a84078f95789f759952`, branch `m_202609_api_feature_40041_39641` (chưa merge release theo lưu ý của AI Auto-fixbug).
- **sns-line (PHP, web)** — AI LME Fix bug (auto-fixbug): web chưa biết mã `15002` nên mọi dòng lịch sử sinh từ API rơi vào nhánh mặc định và hiển thị sai thành `手動` (thao tác tay). Bổ sung nhãn `APIからアクション` vào 3 bảng lịch sử dùng nhãn dùng chung (lịch sử thẻ, lịch sử thông tin bạn bè, lịch sử hiển thị rich menu) + cột 操作者 ở modal chi tiết bạn bè + modal `送信トリガー` ở Chat 1:1 (web **và** app mobile qua `Api/ChatController.php`). Đã xong, commit `cacd763d8a`, branch `ai_small_41714` (base `release_step_20260930`).

Chi tiết đầy đủ 2 phần đánh giá ảnh hưởng (journal #139174 + #139180) xem [03-dev-impact.md](03-dev-impact.md).

## Steps to reproduce

<!-- Không có — ticket "Improve nội bộ", không phải bug report có repro steps. Xem note ở "Ghi chú thêm của Leader". -->

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- issue.attachments = 0, không có file đính kèm. -->

## Ghi chú thêm của Leader

⚠️ Đây là ticket **"Improve nội bộ"** (chủ động bổ sung tính năng phân biệt nguồn trigger), **không phải bug** khách/CS báo — Redmine không có section "Tái hiện bug" nên Steps/Expected/Actual để trống. TCs nên tập trung verify: (1) nhãn `APIからアクション` hiện đúng ở mọi màn dùng chung nhãn trigger, (2) `操作者`/tên chủ API key hiện đúng, (3) regression các nguồn trigger cũ (`手動`, scenario, import CSV, remind, broadcast...) không đổi nhãn.

Status hiện tại: **Fix done - Đợi test**. Fix trải trên **2 repo/branch độc lập** — QA cần checkout đúng cả 2 khi test end-to-end:
- linect-service: branch `m_202609_api_feature_40041_39641` (Dev xác nhận **chưa merge vào nhánh release** tại thời điểm viết journal — cần đảm bảo nhánh job lên cùng đợt với web, nếu không sẽ không tái hiện được hành vi mới vì Java chưa sinh `status_sync=4`/mã 15002).
- sns-line (web + app mobile API): branch `ai_small_41714` (base `release_step_20260930`), đã push origin.

⚠️ **Gap AI tự phát hiện ở lần fix đầu (self-review v1)**: bản fix đầu bỏ sót `ChatController.php` + `Api/ChatController.php` (`getDetailActionTrigger`) — nếu thiếu, popup `送信元` ở Chat 1:1 (cả web và app mobile) sẽ để **trống** cho action nguồn API, là **hồi quy** so với hành vi trước khi Java đổi mã 15001→15002. Đây là điểm QA nên soi kỹ vì chính AI đã phải tự sửa lại sau lần fix đầu.

⚠️ Có 1 chi tiết QA cần confirm lại với Dev/BA: `FriendInformationHistory::TRIGGER_API` trước đây tạm gán `20001`, fix này đổi chốt lại thành `15002`. Cần xác nhận **không có dữ liệu thật nào đang mang mã 20001** trên các môi trường (dev/staging/product) — nếu có, dòng đó sẽ hiển thị sai thành `手動` sau fix (AI ghi "không có dòng dữ liệu nào mang 20001 nên không cần migrate" nhưng chưa verify được trên DB thật — xem journal #139180 mục VERIFY: "Không kiểm chứng được trên MySQL dev: kết nối host.docker.internal:3306 bị từ chối").

📌 **MCP LME TEST STUDIO đã có task cho ticket này**: task_id `341`, feature `friend-mypage`, status `tc-ready`, **23 TC do AI sinh, tất cả CHƯA CHẠY** (exec_mode `auto`, env chưa có lần run nào) — xem [04-tc-list.md](04-tc-list.md). 4 mã quan điểm Studio dùng (`TOOL-NEGCTRL-001`, `DATA-HIST-001`, `TOOL-OLDREC-001`, `TOOL-KNOW-002`) không có trong `framework/checklist-lme.md`.

## Journal / note từ Redmine (nguyên văn)

**Journal #139171 — Thanh Duy Nguyen — 2026-09-29:**
```
Commit: e4fa4ec027aa63917c8d4a84078f95789f759952
```

**Journal #139174 — Thanh Duy Nguyen — 2026-09-29:**
```
Improve nội bộ #41714 [API] Các action từ api ngoài gọi đến có lưu lịch sử nhưng không forward webhook sang bên thứ 3

1. Mục đích
   - Bổ sung trigger type 15002 (APIからアクション) để lịch sử phân biệt được action do API ngoài gọi với action admin thao tác trên web (15001).
   - tag_history / friend_info_history sinh từ API phải mang status_sync = 4 (IGNORE) để job forward webhook #40475 không bắn ngược thay đổi về chính bên thứ 3 vừa gọi API.

2. Cách thực hiện
   - Thêm TriggerStartActionConstants.TYPE_API_ACTION = 15002; McpModel.requestDoAction set type_start_scenario theo hằng số này thay cho "15001" hardcode.
   - HistoryHelper set status_sync = 4 ngay trong câu INSERT khi trigger = 15002 (không update sau khi insert vì job quét status_sync IS NULL sẽ hở race) và cho 15002 resolve được trigger_from_name; ActionModel mở thêm 15002 cho 2 nhánh vốn chỉ chạy với 15001 là update last_message của conversation và ghi message ブロック/非表示 vào chat.

3. Đã check và sửa các function sử dụng đến function/data vừa sửa
   - recordTagAdd / recordTagRemove / recordFriendInfo giữ nguyên signature, status_sync suy ra từ tham số trigger đã có sẵn nên 26 callsite ở ActionModel, LineUserModel, BotLineUserModel, HandlePostbackTask, HandleImportCsvTask không phải sửa.
   - resolveTriggerFromName là private, 3 callsite nội bộ HistoryHelper (recordTag, recordFriendInfo, recordRichMenu) — kéo theo rich_menu_history cũng resolve được trigger_from_name cho trigger 15002.

4. Đánh giá ảnh hưởng
	4.1 List function
		- Nhóm trigger API: McpModel.requestDoAction, ActionModel.doAction(ActionLineUser), ActionModel.doAction (overload chính)
		- Nhóm ghi lịch sử: HistoryHelper.recordTag, HistoryHelper.recordFriendInfo, HistoryHelper.resolveTriggerFromName, HistoryHelper.resolveStatusSyncForApi (mới)
		- Nhóm entity: TagHistory, FriendInfoHistory (map thêm status_sync, created_at)
	4.2 List những data bị update khi fix bug
		- Bắt đầu ghi cột status_sync của tag_history / friend_info_history — migration của #40475 (ALTER TABLE ... ADD COLUMN status_sync tinyint DEFAULT NULL) phải chạy trước khi deploy, nếu chưa có cột thì INSERT lịch sử sẽ fail.
		- Thêm giá trị mới 15002 cho cột trigger_type_start của tag_history / friend_info_history / rich_menu_history.
	4.3 Dựa vào 2 mục trên list những tính năng sẽ ảnh hưởng
		- API do_action: check tag_history / friend_info_history có trigger_type_start = 15002, trigger_from_name = tên user của X-USER-ID, status_sync = 4.
		- Job forward webhook #40475: check không forward row sinh từ API, vẫn forward bình thường row từ web / scenario / autoreply (status_sync NULL).
		- Màn lịch sử tag và lịch sử thông tin bạn bè trên web: check hiển thị được trigger 15002 (bên web cần bổ sung label cho giá trị này).
		- Chat 1:1 khi do_action qua API: check last_message và thời gian tin nhắn cuối được cập nhật, action block/hide có dòng ブロックしました / 非表示しました.
		- Regression thao tác tag / thông tin bạn bè từ web (15001), scenario, import CSV: history vẫn ghi status_sync NULL và vẫn được forward.

5. Commit / Branch
	5.1 Commit hoặc pull request
		- e4fa4ec027aa63917c8d4a84078f95789f759952
	5.2 Branch hiện tại của task
		- m_202609_api_feature_40041_39641
```

**Journal #139180 — AI LME Fix bug — 2026-09-29:**
```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt & push lên origin. Chi tiết bên dưới để QA tiếp nhận.
════════════════════════════════════════════════

■ 1. NGUYÊN NHÂN
Job Java (linect-service) đã đổi nguồn action do hệ thống ngoài gọi qua API công khai sang mã trigger riêng 15002 thay cho 15001, đồng thời tự đánh status_sync=4 cho hai bảng lịch sử để job chuyển tiếp webhook bỏ qua. Phía web sns-line chưa biết mã 15002 nên mọi dòng lịch sử sinh từ API rơi vào nhánh mặc định và hiển thị sai thành thao tác tay. Riêng phần status_sync web không phải sửa vì web không ghi hai bảng này từ API.

■ 2. CÁCH FIX
Bổ sung mã trigger 15002 (APIからアクション) vào phía web sns-line: hằng nhãn dùng chung SourceMessage::ACTION_API; hằng TRIGGER_API=15002 cho TagHistory và chốt lại TRIGGER_API của FriendInformationHistory từ mã tạm 20001 sang 15002; thêm nhánh nhận mã mới vào ba bảng nhãn lịch sử (lịch sử thẻ, lịch sử thông tin bạn bè, lịch sử hiển thị rich menu); cột người thao tác ở màn chi tiết bạn bè nhận 15002 để hiện tên chủ API key thay vì 自動. Không đụng status_sync (job Java ghi lúc INSERT, commit e4fa4ec02). [Tự review v1 bổ sung] Thêm case 15002 vào getDetailActionTrigger của ChatController.php và Api/ChatController.php: đã kiểm chứng job Java CÓ ghi source_messages.action_from (McpModel:402 -> ActionModel:736 -> MessageModel:229 setActionFrom, StartActionInfo dùng @SerializedName trigger_type/from_id đúng key PHP đọc) nên tiền đề ngoài-scope của lần fix đầu là sai; thiếu nhánh này thì popup 送信元 ở chat 1:1 (web + app) để trống, là hồi quy so với trước khi job đổi mã từ 15001 sang 15002.

■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN
App\Models\TagHistory::getTriggerAttribute (app/Models/TagHistory.php)
App\Models\FriendInformationHistory::getTriggerAttribute (app/Models/FriendInformationHistory.php)
App\Traits\ResolveTriggerTypeTrait::resolveTriggerTypeLabel (app/Traits/ResolveTriggerTypeTrait.php)
App\Services\FriendDetailFriendInfoService::transformHistoryRow (app/Services/FriendDetailFriendInfoService.php)
App\Services\FriendDetailService::getRichmenuHistory (app/Services/FriendDetailService.php — caller của trait, chỉ đọc)
sns.line.helper.HistoryHelper.recordTag/recordFriendInfo (linect-service, phía ghi status_sync=4 — chỉ đối chiếu, không sửa)

■ 4. ĐÁNH GIÁ ẢNH HƯỞNG
 • 4.1 File thay đổi:
   - app/SourceMessage.php
   - app/Models/TagHistory.php
   - app/Models/FriendInformationHistory.php
   - app/Traits/ResolveTriggerTypeTrait.php
   - app/Services/FriendDetailFriendInfoService.php
 • 4.2 Data ảnh hưởng:
   - tag_history.trigger_type_start — chỉ ĐỌC để hiện nhãn, web không ghi mã 15002
   - friend_info_history.trigger_type_start — chỉ ĐỌC; hằng TRIGGER_API đổi 20001 thành 15002, không có dòng dữ liệu nào mang 20001 nên không cần migrate
   - tag_history.status_sync / friend_info_history.status_sync — KHÔNG đụng, do job Java ghi lúc insert
 • 4.3 Tính năng liên quan:
   - Tag Management (FA-012) — lịch sử thẻ hiện đúng nguồn API thay vì thao tác tay
   - Friend Information (FA-015) — lịch sử thông tin bạn bè hiện đúng nguồn API và đúng người thao tác
   - Rich Menu (FA-004) — lịch sử hiển thị menu phong phú nhận cùng mã trigger qua trait dùng chung

■ 5. RECOVER DATA
   ✔ Không cần recover data

■ 6. VERIFY
   Mức: unit-test
   Lệnh: php -l cho cả 5 file sửa: không có lỗi cú pháp; Chạy thử runtime qua composer autoload: hằng TRIGGER_API của hai model đều ra 15002, nhãn SourceMessage ra APIからアクション; Chạy thử accessor getTriggerAttribute của hai model với trigger_type_start dạng chuỗi '15002' và số 15002: cả hai ra APIからアクション; 15001 vẫn ra 手動 kèm tên; null và mã lạ vẫn ra 手動; Chạy thử resolveTriggerTypeLabel của trait: 15002 ra APIからアクション, 15001/19001/mã lạ giữ nguyên nhãn cũ
   Bằng chứng: linect-service commit e4fa4ec027aa (nhánh m_202609_api_feature_40041_39641) đã thêm TYPE_API_ACTION=15002, đặt status_sync=4 lúc insert trong HistoryHelper và đổi McpModel từ 15001 sang mã mới — xác nhận phần job đã xong, phần còn thiếu chỉ là hiển thị bên web; Java chỉ đọc source_messages.action_from (không có lệnh setActionFrom nào) nên mã 15002 không lan sang màn chi tiết nguồn tin nhắn; Không kiểm chứng được trên MySQL dev: kết nối host.docker.internal:3306 bị từ chối tại thời điểm chạy

■ TỰ REVIEW (AI)
Fix thuần hiển thị, chỉ thêm nhánh nhận mã trigger mới vào các bảng nhãn có sẵn; không đổi truy vấn, không đổi luồng ghi dữ liệu. Ba bảng nhãn lịch sử là bản sao gần giống nhau (đã có lesson #38316) nên sửa đủ cả ba, cộng thêm chỗ duy nhất còn so sánh 15001 theo giá trị ở màn chi tiết bạn bè.
 • Rủi ro / lưu ý khi test:
   - Nhãn lấy đúng chữ trong ticket là APIからアクション, không kèm tên người thao tác như nhãn 手動（tên）. Nếu BA muốn kèm tên thì sửa một chỗ ở SourceMessage::ACTION_API.
   - Cột người thao tác nay hiện tên chủ khóa API thay vì 'tự động' — đây là suy luận từ việc job cố ý điền trigger_from_name cho mã 15002; nếu BA muốn giữ 'tự động' thì bỏ phần sửa ở FriendDetailFriendInfoService.
   - Phần status_sync=4 hoàn toàn nằm ở job Java (đã xong ở nhánh feature, chưa merge release) — web không kiểm soát được, cần đảm bảo nhánh job lên cùng đợt.

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_small_41714 (nhánh gốc release_step_20260930, commit cacd763d8a, 7 file)  [đã push]

────────────────────────────────────────────────
» Thời gian AI xử lý: 12 phút 29 giây
» Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=implement-task-small-lme&tab=events&session=a97ff994-2d8c-4b4c-8f5c-9a12562acaa7
» Dashboard fixbug: https://dashboard.melonglobal.net/implement-task-small-lme/?id=41714
(Báo cáo tạo tự động bởi hệ thống Auto-fixbug LME)
```
