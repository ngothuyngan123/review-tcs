# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug (hệ thống Auto-fixbug LME)` — assignee Redmine: Ngọc Ánh |
| Commit / Pull Request | `commit 11285b090b` (4 file) — chưa có link PR |
| Branch | `ai_small_40222` (repo sns-line, nhánh gốc `release_step_20260805`) |
| Ngày submit đánh giá | `2026-08-26` (Journal #133130) |
| Auto-filled | `2026-09-16 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Màn chat 1:1 tab thông tin cơ bản cho phép bắt đầu kịch bản bước và gán menu hình ảnh cho cả bạn bè đã chặn bot. Hai API xử lý (đổi kịch bản, đổi menu hình ảnh) **không kiểm tra trạng thái chặn** nên vẫn ghi dữ liệu và hiển thị kết quả như bình thường, dù bạn bè không còn nhận được gì.

Phía giao diện, luồng lưu kịch bản cũng **không hiển thị thông báo khi máy chủ trả lỗi** (im lặng bỏ qua).

## 2. Cách fix

Thêm kiểm tra chặn ở **phía máy chủ** trong bộ điều khiển chat:

- Hàm mới `ChatController::isBlockedByFriend` đọc bảng `conversation` — điều kiện `is_blocked = 1` **và** `blocked_by = 0` (tức bạn bè chủ động chặn bot), lọc theo `bot_id` + `tb_line_user_id`.
- API đổi kịch bản (`actionScenarioMyPage`) **từ chối** thao tác bắt đầu/đổi bước (`action = change`), trả cờ thất bại + message `ブロックされましたため、ステップを開始できません。`
- API đổi menu hình ảnh (`chatEditRichMenu`) **từ chối** thao tác gán menu (`rich_menu_id != 0`), trả cờ thất bại + message `ブロックされましたため、リッチメニューを表示できません。`
- Thao tác **dừng kịch bản** (`action = cancel`) và **ẩn menu** (`rich_menu_id = 0`) **vẫn cho phép** đi qua.
- Guard đặt **TRƯỚC** mọi lệnh gọi API LINE và mọi lệnh ghi dữ liệu (không có trạng thái nửa vời).
- Không tìm thấy bản ghi hội thoại → coi như **chưa chặn**, giữ nguyên hành vi cũ.
- Phía giao diện: luồng lưu kịch bản ở màn chat 1:1 (và 2 màn dùng chung API là trang cá nhân, chi tiết bạn bè) nay **hiển thị thông báo lỗi** máy chủ trả về thay vì im lặng bỏ qua.

**Yokoten Dev tự loại khỏi phạm vi**: các luồng gán kịch bản / menu **tự động** (callback LINE, hành động sau quét mã QR, hành động theo thẻ tag) không nằm trong phạm vi ticket nên **giữ nguyên** (vẫn gán được cho friend đã chặn).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `ChatController::actionScenarioMyPage` — `app/Http/Controllers/ChatController.php` | **Sửa** — thêm guard chặn `action=change` (dòng ~5818-5829) | API đổi kịch bản, điểm fix chính |
| 2 | `ChatController::chatEditRichMenu` — `app/Http/Controllers/ChatController.php` | **Sửa** — thêm guard chặn khi `rich_menu_id != 0` (dòng ~2619-2630) | API đổi rich menu, điểm fix chính |
| 3 | `ChatController::isBlockedByFriend` — `app/Http/Controllers/ChatController.php` | **Thêm mới** — query bảng `conversation` theo `bot_id` + `tb_line_user_id` | Hàm dùng chung cho 2 guard trên |
| 4 | `Basic\ChatController::getBasicInfo` — `app/Http/Controllers/Basic/ChatController.php` | Không sửa — chỉ xác nhận | Xác nhận ngữ nghĩa `line_user_id` truyền vào guard |
| 5 | `saveChangeOrStopStep` / `handleSaveEditStep` / `handleSaveEditRichMenu` — `public/js/chats/chat-v2.js` | **Sửa** — hiển thị message lỗi server trả về | FE màn Chat 1:1 trước đây im lặng bỏ qua lỗi |
| 6 | `saveChangeScenario` — `public/js/my_page/my_page.js` | **Sửa** — hiển thị message lỗi server trả về | FE màn My Page dùng chung API đổi kịch bản |
| 7 | `saveChangeScenario` — `resources/views/basic/friend_detail/index.blade.php` | **Sửa** — hiển thị message lỗi server trả về | FE màn chi tiết bạn bè dùng chung API đổi kịch bản |
| 8 | `HandleCallback::doHandleUnfollow` — `app/Console/Commands/HandleCallback.php` | Không sửa — chỉ xác nhận | Xác nhận nguồn cờ chặn: friend block bot → `is_blocked=1`, `blocked_by=0` (HandleCallback.php:637); admin block friend → `blocked_by=1` (functions.php:8111) |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

> ⚠️ Dev ghi mục 4.1 là **"File thay đổi"** (4 file), không phải list function chuẩn. Bảng dưới đây gán tag `F*` theo function suy từ mục 3 để `/review-tc` map coverage được.

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `ChatController::actionScenarioMyPage` — API `POST /ajax/action_scenario_my_page` (EP-24) | `app/Http/Controllers/ChatController.php` | Direct | Guard mới chặn `action=change`; `action=cancel` đi qua |
| F2 | `ChatController::chatEditRichMenu` — API `POST /basic/chat-edit-rich-menu` (EP-49) | `app/Http/Controllers/ChatController.php` | Direct | Guard mới chặn `rich_menu_id != 0`; `rich_menu_id = 0` đi qua |
| F3 | `ChatController::isBlockedByFriend` (hàm mới) | `app/Http/Controllers/ChatController.php` | Direct | Query đếm trên bảng `conversation` mỗi lần bấm 2 thao tác trên |
| F4 | FE Chat 1:1 — `saveChangeOrStopStep` / `handleSaveEditStep` / `handleSaveEditRichMenu` | `public/js/chats/chat-v2.js` | Direct | Hiện message lỗi từ server |
| F5 | FE My Page — `saveChangeScenario` | `public/js/my_page/my_page.js` | Direct | Hiện message lỗi từ server. ⚠️ Studio REQ-009 nghi ngờ **không màn nào còn nạp file JS này** — cần xác nhận |
| F6 | FE Chi tiết bạn bè — `saveChangeScenario` | `resources/views/basic/friend_detail/index.blade.php` | Direct | Hiện message lỗi từ server |
| F7 | `Basic\ChatController::getBasicInfo` | `app/Http/Controllers/Basic/ChatController.php` | Indirect | Không sửa — nguồn `line_user_id` cho guard |
| F8 | `HandleCallback::doHandleUnfollow` | `app/Console/Commands/HandleCallback.php` | Indirect | Không sửa — nơi ghi cờ `is_blocked=1 / blocked_by=0` |

### 4.2. List data bị update khi fix bug

> Dev khẳng định **không có data bị ghi thêm/sửa/xoá**. Guard chỉ **đọc** thêm 2 cột; tác dụng là **ngăn ghi rác** vào 4 bảng bên dưới cho friend đã chặn.

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `conversation.is_blocked`, `conversation.blocked_by` | **READ** (mới) | Guard đọc theo `bot_id` + `tb_line_user_id`. `is_blocked=1 & blocked_by=0` = friend block bot; `blocked_by=1` = admin block friend (KHÔNG chặn) |
| D2 | `scenario_lineuser` | **KHÔNG ghi nữa** (trước fix có ghi) | Không phát sinh bản ghi kịch bản cho friend đã chặn |
| D3 | `scenario_step_time` | **KHÔNG ghi nữa** | Không phát sinh tin bước đã lên lịch |
| D4 | `bot_line_user.rich_menu_id` | **KHÔNG update nữa** | Rich menu đang gán của friend đã chặn giữ nguyên |
| D5 | `rich_menu_history` | **KHÔNG ghi nữa** | Không phát sinh bản ghi lịch sử rich menu |
| D6 | `scenario.count_follow` (suy từ D2) | **KHÔNG tăng nữa** | Số người đang theo dõi kịch bản không tăng khi thao tác bị chặn |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Chat 1:1 (FA-001)** — tab 基本情報 | F1, F2, F4, D1-D6 | **High** — chặn thao tác bắt đầu step + hiển thị rich menu với friend đã chặn, có báo lỗi |
| T2 | **Step Delivery / Scenario (FA-009)** | F1, D2, D3, D6 | **High** — thao tác bắt đầu/đổi bước thủ công bị chặn; thao tác **dừng bước không đổi** |
| T3 | **Rich Menu (FA-004)** | F2, D4, D5 | **High** — thao tác gán menu thủ công bị chặn; thao tác **ẩn menu không đổi** |
| T4 | **My Page (FA-036)** | F5 | **Medium** — dùng chung API đổi kịch bản nên cũng bị chặn, nay có hiện thông báo lỗi. ⚠️ cần xác nhận màn này còn tồn tại (REQ-009) |
| T5 | **Friend Detail 「友だち詳細」** (outside glossary) | F6 | **Medium** — dùng chung API đổi kịch bản nên cũng bị chặn, nay có hiện thông báo lỗi |

---

## Điểm Dev tự nêu là RỦI RO / CẦN CHỐT (rút gọn từ mục TỰ REVIEW của journal)

1. **Chỉ chặn friend block bot** (`blocked_by=0`). Trường hợp **admin block friend** (`blocked_by=1`) vẫn cho thao tác như cũ. → Nếu BA muốn chặn cả case này thì phải chốt thêm message riêng. **Cần Leader/BA xác nhận.**
2. **Thêm 1 query đếm** trên bảng `conversation` mỗi lần bấm 2 thao tác. Dev đánh giá tải không đáng kể (thao tác thủ công hiếm, lọc theo `bot_id` + `tb_line_user_id`).
3. Hàm kiểm tra đặt **trong controller** (query Eloquent trực tiếp) thay vì tầng service/repository như quy ước code mới — chọn để giữ diff tối thiểu trên controller hơn 6000 dòng.
4. ⚠️ **Dev KHÔNG tái hiện được trên môi trường dev** (MySQL trong container từ chối kết nối). Mức verify duy nhất đã chạy là **lint / syntax check**. Toàn bộ verify hành vi phụ thuộc tester.
5. Mâu thuẫn Studio ghi nhận thêm (không nằm trong journal Dev): thao tác **dừng kịch bản** đi qua được guard mới, nhưng `ChatMessages::changeScenario` được cho là vẫn trả thất bại với mọi hội thoại đang bị chặn trong khi endpoint trả `success=true` → **màn có thể báo thành công mà dữ liệu không đổi**. Cần Leader quyết định có tách bug riêng hay không.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
