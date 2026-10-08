# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI Auto-fixbug LME (tự động, không có Dev người trực tiếp sửa — xem journal #139877)` |
| Commit / Pull Request | `commit e8a74f3123 trên branch ai_fixbug_41885 (không có link PR riêng, chỉ có branch/commit nêu trong báo cáo)` |
| Branch | `ai_fixbug_41885` (nhánh gốc `release_step_20260930_v2`) |
| Ngày submit đánh giá | `2026-10-03` |
| Auto-filled | `2026-10-03 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine (journal #139877) và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

⚠️ **Nguồn**: nội dung dưới đây lấy từ **journal #139877** (báo cáo AI auto-fixbug, sau khi fix đã triển khai) — KHÔNG lấy từ phần "Nguyên nhân" / "Hướng fix đề xuất" trong description gốc (đó là phân tích/đề xuất ban đầu của AI Reader, trước khi fix). Bảng chi tiết dòng code + caller ở phần "Ghi chú" mục 4.2 bên dưới được bổ sung thêm từ description gốc vì journal không liệt kê lại.

⚠️ **Dev chưa test runtime được** (mục 6 VERIFY của journal): chỉ chạy `php -l` (lint) + `git diff --stat`, KHÔNG connect được dev DB (`host.docker.internal:3306 Connection refused`) nên KHÔNG tái hiện được bug / verify fix bằng runtime thật. Leader cần coi đây là input **chưa qua kiểm chứng thực thi**, TCs phải tự chạy full flow để verify, không dựa vào "Dev đã test".

---

## 1. Nguyên nhân

Ở bước 2 kết nối bot (`step2Check`), nếu đã có bot tạm cùng `admin_id` + `channel_id` thì hệ thống dùng lại bot cũ (theo Task #36409), nhưng các dữ liệu mặc định phía sau (trạng thái chat, 3 mục thông tin bạn bè ở chat 1-1, cài đặt khi thêm bạn, profile mặc định, liên kết nhân viên) vẫn được tạo **vô điều kiện** nên mỗi lần chạy lại bước 2 sinh thêm 1 bộ trùng. Fix #40599 trước đó mới chặn trùng riêng cài đặt thông báo (`notify_setting`).

## 2. Cách fix

Trong `step2Check` (nhánh tạo bot, có dùng lại bot tạm) chỉ tạo dữ liệu mặc định **khi bot chưa có**, theo đúng pattern của `finalizeBot`:
- `status_chat` — chỉ tạo bộ mặc định khi bot chưa có status nào.
- `setting_display_info_friend_chat11` — chỉ tạo khi bot chưa có dòng `type=0`.
- `bots_profiles` — chỉ insert khi bot chưa có profile `is_default=1` của cặp (bot_id, user_id).
- `add_friend_setting` — đổi sang `firstOrCreate(['bot_id' => $bot_id])`.
- `user_bot` — đổi sang `firstOrCreate` theo (bot_id, user_id).

Kèm sửa kiểm tra `bots_tutorial` từ cột `id` sang `bot_id` (refix vòng 1) — hệ quả phụ: bot mới kết nối qua bước 2 nay **luôn** có dòng tutorial (trước đây có thể thiếu nếu id tutorial của bot khác trùng số với bot_id).

> Tự review của AI (v1): bổ sung report cho đầy đủ, không đổi code.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `BotController::step2Check` (app/Http/Controllers/Admin/BotController.php) | **Có** — thêm guard tồn tại trước khi tạo từng loại dữ liệu mặc định + sửa check `bots_tutorial` theo `bot_id` | Nơi phát sinh bug, nhánh tạo bot dùng lại bot tạm |
| 2 | `BotController::finalizeBot` | Không — chỉ đối chứng | Đã làm đúng pattern guard `hasSettings`/`hasProfile` từ trước, dùng làm mẫu để fix `step2Check` |
| 3 | `BotController::preCreateBot` (EP-17, nhánh `existingBot`) | Không — chỉ kiểm tra | Nhánh idempotent tương tự, xác nhận không bị ảnh hưởng bởi thay đổi |
| 4 | `BotController::changeNewBotStep1` | Không — chỉ kiểm tra | Mẫu guard `AddFriendSetting count==0` đã có từ trước, dùng đối chứng |
| 5 | `BotController::botChange` / `saveOlioa` / `saveChangeBot` / `saveBotAfterLogin` | Không | Luôn `insertGetId` bot **mới** (không có nhánh dùng lại bot tạm) → không bị bug này, xác nhận không cần sửa |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `BotController::step2Check` — nhánh tạo bot, dùng lại bot tạm (`!isset($request->id)`, có `is_deleted=2` cùng admin+channel) | app/Http/Controllers/Admin/BotController.php (gốc dòng ~5731-5889 theo branch `release_step_20260930_v2`) | Direct | API `/admin/step2-check`. Bot mới lần đầu (không có bot tạm trùng) — hành vi KHÔNG đổi |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `status_chat` | CREATE (có điều kiện: chỉ khi bot chưa có status nào) | Trước fix: dòng 5804-5812, mỗi lần chạy lại thêm 1 bộ status mặc định. Caller đọc bị ảnh hưởng: `Api/ChatController:485,5982`; `Basic/BroadcastController:100`; `Basic/ActionScheduleController:142` |
| D2 | `setting_display_info_friend_chat11` (`type=0`) | CREATE (có điều kiện: chỉ khi chưa có dòng type=0) | Trước fix: dòng 5731-5740, mỗi lần chạy lại thêm 3 dòng type=0 (LINE名/友だち追加日時/システム表示名). Caller đọc: `Basic/ChatController:941, 5859` |
| D3 | `add_friend_setting` | `firstOrCreate(['bot_id'=>...])` | Trước fix: dòng 5814, mỗi lần chạy lại thêm 1 dòng. Không lộ UI (mọi nơi đọc dùng `->first()`) — chỉ là rác DB, nhưng vẫn cần verify không tăng số dòng |
| D4 | `bots_profiles` (`is_default=1`) | CREATE (có điều kiện: chỉ khi chưa có profile is_default=1 của cặp bot_id+user_id) | Trước fix: dòng 5877-5883, mỗi lần chạy lại thêm 1 profile mặc định. Caller đọc: `Api/ChatController:3793` |
| D5 | `user_bot` (bảng liên kết nhân viên) | `firstOrCreate` theo (bot_id, user_id) | Trước fix: dòng 5886-5889 tạo vô điều kiện, nhưng luồng hiện tại (v5) gửi `ids=[]` nên thực tế KHÔNG phát sinh trùng qua đường step2Check hiện hành. ⚠️ Luồng cũ (`public/js/admin/add_bot/steps.js`, `public/js/admin/step_add_bot.js`) có gửi ids thì CÓ THỂ bị — Dev chưa xác nhận luồng cũ còn dùng hay không. `firstOrCreate` KHÔNG xét `is_deleted` (bot tạm không có thao tác xoá nhân viên nên Dev đánh giá không ảnh hưởng) |
| D6 | `bots_tutorial` | Guard đổi từ check theo cột `id` sang theo `bot_id` | Hệ quả phụ ngoài phạm vi bug gốc: bot kết nối qua bước 2 (mọi trường hợp, không riêng kịch bản lặp) nay **luôn** có dòng tutorial — trước đây có thể bị thiếu nếu id tutorial của bot khác trùng số với bot_id. Dev note: chỗ `where(id, $bot_id)->update` ở luồng khác (dòng 6913) KHÔNG bị đụng |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Add New Account (FA-032) — bước 2 kết nối bot (PC接続 wizard) | F1 | High — đúng trọng tâm fix, phải verify cả case bot mới lần đầu (không đổi hành vi) và case gọi lại trên bot tạm |
| T2 | Chat 1:1 (FA-001) — danh sách trạng thái chat + khung thông tin bạn bè (LINE名/友だち追加日時/システム表示名) | D1, D2 | High — hiển thị trực tiếp cho end-user, dễ thấy nếu còn lặp |
| T3 | Broadcast (FA-008) — filter theo trạng thái chat (一斉配信) | D1 | Medium |
| T4 | Tutorial cho bot mới (hiện hướng dẫn sau khi kết nối) | D6 | Medium — hệ quả phụ ngoài phạm vi bug gốc, Dev note "cần retest màn tutorial sau khi kết nối" |
| T5 | ActionSchedule (アクション予約) — filter theo trạng thái chat | D1 (từ bảng "Nơi đọc bị ảnh hưởng" trong description gốc: `Basic/ActionScheduleController:142`) | Medium — ⚠️ **KHÔNG nằm trong mục 4.3 của journal fix report**, chỉ xuất hiện ở phân tích ban đầu (description). Cần hỏi lại Dev xem màn ActionSchedule filter trạng thái chat còn bị ảnh hưởng theo đúng cách T3 (Broadcast) không, trước khi loại khỏi phạm vi test |

> ⚠️ **Recover data (production)**: dữ liệu trùng đã phát sinh từ TRƯỚC khi có fix này vẫn còn tồn đọng trên production, CHƯA được Recover data. Cần SQL riêng (xem `01-bug-task.md` → Ghi chú thêm của Leader), giữ bản ghi id nhỏ nhất mỗi nhóm, xoá bản thừa — status_chat/bots_profiles thừa có thể đã được tham chiếu (conversation status đã gán, profile đã được chọn gửi tin) nên phải chuyển tham chiếu về bản giữ lại trước khi xoá.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót) — **đặc biệt**: hỏi lại luồng cũ `steps.js`/`step_add_bot.js` (D5) còn dùng không
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng — **đặc biệt**: xác nhận lại T5 (ActionSchedule) có thuộc phạm vi hay không
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
