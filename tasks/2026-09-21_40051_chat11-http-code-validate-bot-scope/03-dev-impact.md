# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (auto-fixbug) — assignee ticket: Đoàn Thị Bích Hảo |
| Commit / Pull Request | Không có link PR. Commit cuối cùng có hiệu lực: **b18b55a092** (revert). Lịch sử: `f2e371adbe` → `1fa9b45bdc` → `89a9c0411f` → `b18b55a092` (cây mã = `1fa9b45bdc`). Dashboard: https://dashboard.melonglobal.net/fixbug-lme/?id=40051 |
| Branch | `ai_fixbug_40051` (nhánh gốc `release_step_20260805`) — repo `sns-line` |
| Ngày submit đánh giá | 2026-09-15 (4 journal cùng ngày: #136589 · #136625 · #136636 · #136646) |
| Auto-filled | `2026-09-21 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại 4 journal auto-fixbug từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

> ⚠️ **Lưu ý khi verify**: Redmine #40051 **không có section "Đánh giá ảnh hưởng" trong description**. Toàn bộ nội dung dưới đây lấy từ **4 journal auto-fixbug**. Các journal cộng dồn: mục 1 / 3 / 4 giống nhau ở cả 4 vòng, chỉ mục **2. Cách fix** khác nhau → mục 2 bên dưới gộp cả 4 vòng theo thứ tự, và **đánh dấu rõ vòng 3 đã bị revert**.

---

## 1. Nguyên nhân

(nguyên văn — giống nhau ở cả 4 journal)

> Các endpoint API/ajax của màn chat 1:1 trả HTTP code sai ý nghĩa: lỗi hệ thống (ngoại lệ trong khối catch), không tìm thấy bản ghi, và lỗi nghiệp vụ đều trả 200 (nghĩa là thành công), màn hình phải tự đoán qua cờ success trong thân phản hồi nên giám sát không thấy lỗi. Ngoài ra hầu hết endpoint nhận dữ liệu thẳng từ request mà không kiểm tra bắt buộc: thiếu tham số vẫn chạy truy vấn theo giá trị rỗng rồi báo thành công, hoặc gọi thuộc tính trên bản ghi không tồn tại rồi rơi vào catch.

---

## 2. Cách fix

### 2.1 Vòng 1 — commit `f2e371adbe` (journal #136589): siết ràng buộc bot, 2 tầng

Rà toàn bộ **61 method** ticket này đụng ở 2 controller chat11.

**TẦNG 1 — nguồn xác định bot (17 chỗ).** Trước fix: `if (!empty($request->botIdCurrent)) $bot = $request->botIdCurrent; else $bot = getBotId();` → biến phạm vi do **client điều khiển** nên mọi `where('bot_id', $bot)` phía dưới vô nghĩa (đổi 1 con số = thao tác chéo sang bot người khác). Đã thay hết bằng `getBotIdInScope($request->botIdCurrent)` (hàm có sẵn trên release, đang dùng ở `TemplateV2Controller`; trả `null` khi bot không thuộc quyền user đang đăng nhập).
- **15 endpoint public** → trả **403** qua helper mới `responseBotForbidden()` (đặt cạnh `responseInvalid()` ở cả 2 controller, thông điệp tiếng Nhật).
- **2 hàm PRIVATE** `getFriends` / `getFriendsES` → trả giá trị rỗng tự nhiên (`[]` và `false` — `false` là sentinel sẵn có của `getFriendsES`) kèm `logInfo`, **KHÔNG** trả `JsonResponse` (sẽ bị nhét nguyên object vào khoá `data` của payload).

**TẦNG 2 — query lấy id thẳng từ request mà thiếu điều kiện bot.** Chỉ thêm `bot_id` vào bảng **thực sự có cột đó** (đối chiếu schema `/workspace/share/db`). Các lỗ đã vá:

| Mã | Điểm sửa | Lỗ hổng trước fix |
|---|---|---|
| (a) | `addProfilesBots` | `BotsProfiles::where('id',$idProfile)->update($settings)` mà `$settings` GÁN `bot_id` của mình ⇒ sửa profile bot khác **và kéo nó về bot mình** |
| (b) | `deleteProfilesBots` | Đọc + DELETE chỉ theo `id` ⇒ xoá profile bot khác |
| (c) | `saveSelectedProfileBot` | Chọn được hồ sơ người gửi của bot khác |
| (d) | `getMemosInfo` / `saveMemo` / `deleteMemo` / `saveSortMemo` (Basic) | Đọc / sửa / xoá / đổi thứ tự memo chỉ theo `id`/`conversation_id` từ request |
| (e) | `updateStatusConfirm` / `changeStatusSettingCons` | `Conversation::whereIn('id',$conversationIds)->get()` là query CHÍNH dẫn cả vòng lặp ghi dữ liệu, không lọc bot |
| (f) | `getMessageSocket` | `MessagesV2::where('id',$msgId)` ⇒ đọc trọn nội dung tin nhắn của bot bất kỳ |
| (g) | `getBadge` | Lộ số tin chưa đọc + loại tin của bot khác |
| (h) | `ajaxSaveItemStatus` | UPDATE đã lọc bot nhưng `StatusChat::find()` đọc lại thì không ⇒ vẫn trả bản ghi bot khác về client |
| (i) | `saveTagLine` | `Tags::find()` theo `tags_id`/`tags_delete` rồi cộng/trừ `count_user_tag` ⇒ **sửa số liệu tag của bot khác** |
| (j) | `saveSettingDisplayInfoV2` + `saveSettingDisplayInfoItem` | Xoá/sửa `SettingDisplayInfoFriendChat11` và `FriendInformationSetting`/`FriendInformationValue` theo id từ request |
| (k) | `CaptureTemplate` (3 chỗ) + đọc `Conversation` theo id từ request ở `ajaxSaveHideFriend`, `confirm`, `changStatus`, `refreshMessage` | Không lọc bot |

**Xử lý null sau khi siết**: `changStatus` thêm **404** `'会話が見つかりません。'` (giống `confirm` đã có); `saveTagLine` `continue` khi tag không thuộc bot; các chỗ còn lại đã sẵn `if($conver)` / `if($tagDelete)`.

**CỐ Ý KHÔNG sửa**: (1) `LineUser::find/where('id',$lineId)` — bảng `line_user` không có cột `bot_id` (gắn bot qua bảng nối `bot_line_user`), siết đúng phải join thêm → vượt phạm vi ticket, chỉ nêu; (2) `removeTagLineUserMyPage` — thuộc màn MyPage; (3) khối `SettingDisplayInfoFriendChat11` đang bị comment trong `saveSettingDisplayInfoV2` (code chết); (4) `saveSettingDisplayInfo` bản v1 (code chết — JS chỉ gọi V2/Item).

### 2.2 Vòng 2 — commit `1fa9b45bdc` (journal #136625): vá 3 lỗi review + 1 regression tự phát hiện

| # | Điểm sửa | Nội dung |
|---|---|---|
| (1) | `refreshMessage` rule `page` | `'nullable\|integer\|min:1'` làm màn chat **KHÔNG BAO GIỜ tải được lịch sử tin**: chat11 gửi `page: this.current_page++` (khởi tạo 0, reset 0 khi đổi bộ lọc/tìm kiếm) → lần gọi đầu luôn `page=0`; `0` không phải null nên `nullable` không cứu, `min:1` fail → 422. Nặng thêm: `$.ajax` của `refresh()` **không có nhánh error** → hỏng **im lặng**. Đã đổi `min:0` (thân hàm vốn quy 0 về 1 bằng `$request->page ? ... : 1`) |
| (2) | `refreshMessage` guard bot | Vòng 1 sửa THIẾU: `Conversation::where('id',$id_conver)->where('bot_id',$bot_id)` đúng, nhưng `$conversation` null **không làm hàm dừng** (lối thoát sớm duy nhất là `empty($lineUser)`), phần lấy dữ liệu bên dưới vẫn bám `$id_conver` THÔ (`MessagesV2 ... where('messages_v2s.conversation_id',$id_conver)` + 2 chỗ `where('conversation_id',$id_conver)`). **Kịch bản khai thác**: đăng nhập bot A → gọi `/basic/refresh_message` với `conversation` = id hội thoại bot B + `line_user_id` = id line_user bất kỳ còn tồn tại + `botIdCurrent` = bot A (hợp lệ) ⇒ trả trọn lịch sử tin nhắn bot B. Đã thêm guard: gửi `conversation` mà tra không ra trong phạm vi bot thì DỪNG, trả payload rỗng sẵn có (**200**). Cố ý KHÔNG chặn khi `$id_conver` rỗng (màn hình được phép gọi lúc chưa chọn hội thoại) |
| (3) | 17 rule `line_user_id` / `lineId` / `line_id` / `to_user` | Rule `integer` **chặn toàn bộ hội thoại NHÓM** — với nhóm `conversation.line_id` là CHUỖI (`olioa_group_<id>`, hoặc groupId/roomId của LINE) và chat11 gửi chính giá trị đó. Ép `integer` ⇒ 422: `refreshMessage` hỏng im lặng, `initFriendInfo` (`/ajax/info_friend_display_chat11`) có nhánh error gọi `showChatAjaxError` nên **bật alert tiếng Nhật mỗi lần mở một nhóm**. Trước ticket này các endpoint đó trả 200 + dữ liệu rỗng ⇒ **regression do rule mới**. Đã nới `integer` → `string\|max:255` ở cả 2 controller (giữ nguyên required/nullable) |
| (4) | `validateSendRequest` (Basic) — **tự phát hiện** | Dùng chung cho `sendMessage`/`sendMedia`/`sendTemplate`/`sendSticker` (4 endpoint GỬI TIN THẬT) ép `'to_user' => 'required\|integer'`, trong khi FE gửi `to_user: this.current_friend.line_id` (chat-v2.js:3375/3496/3583/4071) = chuỗi khi là nhóm ⇒ **KHÔNG GỬI ĐƯỢC TIN vào bất kỳ hội thoại nhóm nào**. Đã nằm trong nhóm 17 rule nới ở (3). Giữ nguyên `'conversation' => 'required\|integer'` vì `conversation.id` là số thật |

### 2.3 Vòng 3 — commit `89a9c0411f` (journal #136636): ⚠️ ĐÃ BỊ REVERT

Siết `botIdCurrent` phải **TRÙNG KHỚP** bot đang mở trong session bằng helper private `resolveCurrentBotId(Request $request)` ở từng controller (thay 17 lời gọi). **Bản này đã bị revert ở vòng 4 — KHÔNG còn hiệu lực, KHÔNG viết TC theo hành vi này.**

### 2.4 Vòng 4 — commit `b18b55a092` (journal #136646): **BẢN CÓ HIỆU LỰC**

Revert nguyên vẹn về `getBotIdInScope()` theo quyết định human ("dùng `getBotIdInScope()` là đủ"). `git diff 1fa9b45bdc HEAD` rỗng.

**Hành vi chốt của 17 điểm xác định bot (15 ở `ChatController`, 2 ở `Basic\ChatController`):**
- Bot thao tác chỉ cần **NẰM TRONG danh sách bot user đang đăng nhập có quyền** (`getListBotId`) — **KHÔNG** bắt buộc trùng bot đang mở.
- **Không gửi `botIdCurrent`** → mặc định về bot trong session. Nhánh này cố ý giữ vì nhiều call site không gửi: `updateStatusConfirm()` (chat-v2.js:1887 chỉ gửi `conversationIds`/`status`/`type`), và các endpoint dùng chung với màn khác như `confirm` (`/basic/rec_message`) gọi từ `chats/common.js:65`, `mobile/common.js`, `mobile/events.js`, `chat_group.js`. Bỏ nhánh này sẽ **403 hàng loạt**.
- Gửi `botIdCurrent` = bot **không thuộc quyền** ⇒ endpoint public trả **403** (`responseBotForbidden()`); 2 hàm private `getFriends`/`getFriendsES` trả rỗng (`[]` / `false`).

---

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

(nguyên văn mục 3 — giống nhau ở cả 4 journal)

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `ChatController::ajaxGetStatusChat` / `ajaxGetStatusChatV2` / `ajaxInitStickerChat` (app/Http/Controllers/ChatController.php) | Sửa | Trong 61 method chat11 bị rà |
| 2 | `ChatController::ajaxSaveItemStatus` / `ajaxDeleteItemStatus` | Sửa | Lỗ (h) — `StatusChat::find()` đọc lại không lọc bot |
| 3 | `ChatController::ajaxSaveBookMark` / `ajaxSaveBookMarkConversation` / `ajaxSaveHideFriend` / `ajaxSaveHideFriends` | Sửa | Lỗ (k) — đọc `Conversation` theo id từ request |
| 4 | `ChatController::addProfilesBots` / `ajaxGetProfileOfBots` / `deleteProfilesBots` / `saveSelectedProfileBot` / `reGetProfileBot` | Sửa | Lỗ (a)(b)(c) — hồ sơ người gửi |
| 5 | `ChatController::refreshMessage` / `getMessageSocket` / `getBadge` | Sửa | Lỗ (f)(g) + guard + rule `page` `min:0` |
| 6 | `ChatController::confirm` / `updateStatusConfirm` / `changStatus` / `changeStatusSettingCons` | Sửa | Lỗ (e)(k) + `changStatus` thêm 404 |
| 7 | `ChatController::getCategories` / `getTagInCat` / `saveTagLine` | Sửa | Lỗ (i) — `count_user_tag` của bot khác |
| 8 | `ChatController::getInfoDisplayChat` / `saveSettingDisplayInfoItem` / `saveSettingDisplayInfoV2` / `ajaxEditSystemName` | Sửa | Lỗ (j) — setting hiển thị friend info |
| 9 | `ChatController::chatEditRichMenu` / `sendActionForUser` | Sửa | Rich menu + action từ màn chat |
| 10 | `ChatController::ajaxDownloadFileChat11` / `getDetailActionMessageChat11` / `getDetailMessSendAll` / `getDetailActionTrigger` | Sửa | Trong 61 method chat11 bị rà |
| 11 | `Basic\ChatController::ajaxGetDataForEditStep` / `ajaxGetDataForEditRichMenu` | Sửa | Step delivery + rich menu |
| 12 | `Basic\ChatController::getFriends` / `confirmReadMessage` / `quickAction` / `getBasicInfo` | Sửa | `getFriends` là hàm PRIVATE → trả `[]` thay vì 403 |
| 13 | `Basic\ChatController::settingFriendDisplayModalV3` / `removeTagLineUser` / `getCategoriesTags` / `getFormAnswerInfo` | Sửa | Khối friend info bên phải màn chat |
| 14 | `Basic\ChatController::sendMessage` / `sendMedia` / `sendTemplate` / `sendSticker` | Sửa | Dùng chung `validateSendRequest` — lỗi (4) vòng 2 |
| 15 | `Basic\ChatController::getMemosInfo` / `saveMemo` / `deleteMemo` / `saveSortMemo` | Sửa | Lỗ (d) — memo |
| 16 | `Basic\ChatController::syncInfoFromLine` / `confirmMessage` | Sửa | Đồng bộ thông tin từ LINE |
| 17 | `ChatService::chatMessage` / `sendMedia` / `sendTemplate` (app/Services/ChatService.php) | **KHÔNG sửa** | Chỉ ĐỌC để xác định phạm vi |
| 18 | `ConversationService::confirmReadMessage` / `quickAction` / `confirmMessage` (app/Services/ConversationService.php) | **KHÔNG sửa** | Chỉ ĐỌC |

---

## 4. Đánh giá ảnh hưởng

> ⚠️ Journal của Dev ghi mục **4.1 là "File thay đổi"** (không phải list function) và **4.2 "Data ảnh hưởng" = Không có**. Bảng dưới giữ nguyên nội dung Dev kê, chỉ gán mã `F*` / `D*` / `T*` theo quy ước repo.

### 4.1. List function bị ảnh hưởng

(Dev kê theo **file thay đổi** — chi tiết function xem mục 3)

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `ChatController` — 15 endpoint public + toàn bộ method chat11 (status chat, bookmark, hide friend, profile bot, refresh/socket/badge, confirm/changStatus, tag, setting display info, rich menu, action, download file, detail action) | `app/Http/Controllers/ChatController.php` | Direct | Nơi tập trung fix: 15/17 lời gọi `getBotIdInScope` + `responseBotForbidden()` + validate required + đổi HTTP code |
| F2 | `Basic\ChatController` — getFriends, gửi tin/media/template/sticker, memo, quick action, confirm read, friend display modal, tag, form answer, sync info from LINE, edit step / edit rich menu | `app/Http/Controllers/Basic/ChatController.php` | Direct | 2/17 lời gọi `getBotIdInScope` (đều là hàm private `getFriends`/`getFriendsES` → trả rỗng, không 403). Chứa `validateSendRequest` dùng chung 4 endpoint gửi tin |
| F3 | Config `sns-line` | `config/sns-line.php` | Direct | Dev không mô tả chi tiết thay đổi ⇒ **Input thiếu** — cần hỏi Dev key nào đổi (nghi là message lỗi / mã HTTP) |
| F4 | Xử lý lỗi ajax phía client (mới) | `public/js/chats/ajax-error.js` | Direct | File xử lý lỗi mới; **chỉ nạp ở màn chat11**, cố ý KHÔNG thêm vào `common.js` (2 màn chat cũ `chat_basic`, `chat_group` không nạp file này → tránh lỗi hàm chưa định nghĩa) |
| F5 | Logic ajax màn chat11 | `public/js/chats/chat-v2.js` | Direct | Gọi `showChatAjaxError`; nơi phát sinh `page: this.current_page++` và `to_user: this.current_friend.line_id` |
| F6 | View màn chat | `resources/views/basic/chat/index.blade.php` | Direct | Nạp `ajax-error.js`; nguồn render `botIdCurrent` (dòng 107/108) |
| F7 | `getBotIdInScope()` (hàm dùng chung, có sẵn trên release) | helper chung | Indirect | **KHÔNG sửa** hàm này (vòng 3 từng tránh sửa để không đụng `TemplateV2Controller`/`TemplateService`; vòng 4 revert về dùng lại nguyên bản) ⇒ không kỳ vọng regression ở màn Template |
| F8 | `common.js` (`public/js/chats/common.js`) + `mobile/common.js` + `mobile/events.js` + `chat_group.js` | JS các màn chat cũ / mobile | Indirect | **KHÔNG sửa**, nhưng gọi endpoint `confirm` (`/basic/rec_message`) đã bị siết ⇒ vùng regression cần test dù không đụng code |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | — | — | **Dev kê: "Không có - chỉ đổi mã HTTP trả về và thêm kiểm tra đầu vào, không thay đổi câu lệnh ghi dữ liệu nào"** |

> ⚠️ **Điểm cần Leader lưu ý khi review coverage**: mục 4.2 Dev kê "không có data ảnh hưởng", **nhưng mục 2 (TẦNG 2) lại thêm điều kiện `bot_id` vào các câu UPDATE/DELETE thật** — `BotsProfiles`, `SettingDisplayInfoFriendChat11`, `FriendInformationSetting`/`FriendInformationValue`, `Tags.count_user_tag`, memo, `Conversation` (status/confirm), `StatusChat`, `CaptureTemplate`. Không đổi **câu lệnh ghi** nhưng đổi **phạm vi bản ghi bị ghi** ⇒ vẫn là vùng cần TC verify (đặc biệt `Tags.count_user_tag` — số liệu hiển thị) và cần cảnh báo Dev kê thiếu.

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **1-on-1 Chat (FA-001)** — toàn bộ API/ajax màn chat 1:1: tải danh sách bạn bè, tải lịch sử tin, gửi tin/ảnh/mẫu tin/nhãn dán, đánh dấu đã đọc, ghi chú, đổi trạng thái hội thoại, ghim, ẩn bạn bè, hồ sơ người gửi | F1, F2, F4, F5, F6 | **High** — 61 method bị đụng; đã có 2 regression thật xảy ra trong quá trình fix (page=0, hội thoại nhóm) |
| T2 | **Chat Settings (chat-setting)** — lưu cài đặt chat + quản lý danh sách trạng thái hội thoại hiển thị trong màn chat | F1 (`ajaxGetStatusChat*`, `ajaxSaveItemStatus`, `ajaxDeleteItemStatus`) | Medium |
| T3 | **Tag Management (FS-tag)** — gắn/gỡ nhãn cho bạn bè ngay trong màn chat (**endpoint dùng chung với màn chi tiết bạn bè và trang thông tin bạn bè**) | F1 (`saveTagLine`, `getCategories`, `getTagInCat`), F2 (`removeTagLineUser`, `getCategoriesTags`) | **High** — dùng chung nhiều màn + đụng `count_user_tag` |
| T4 | **Friend Information (friend-info)** — khối thông tin bạn bè bên phải màn chat: đồng bộ thông tin từ LINE, sửa tên hệ thống, lưu cài đặt hiển thị mục thông tin | F1 (`getInfoDisplayChat`, `saveSettingDisplayInfoV2/Item`, `ajaxEditSystemName`), F2 (`syncInfoFromLine`, `settingFriendDisplayModalV3`, `getFormAnswerInfo`) | Medium |
| T5 | **Rich Menu (FA-004)** — đổi menu hình ảnh của bạn bè từ màn chat | F1 (`chatEditRichMenu`), F2 (`ajaxGetDataForEditRichMenu`) | Medium |
| T6 | **Step Delivery (scenario)** — đổi/dừng kịch bản bước của bạn bè từ màn chat | F2 (`ajaxGetDataForEditStep`), F1 (`sendActionForUser`) | Medium |
| T7 | **Hội thoại NHÓM + màn chat cũ (`chat_basic`, `chat_group`) + app mobile admin** | F8 — endpoint `confirm` (`/basic/rec_message`) dùng chung; rule `line_id` chuỗi `olioa_group_<id>` | **High** — Dev **KHÔNG kê ở 4.3** nhưng journal #136625 chứng minh đây là vùng đã gãy 2 lần; `ajax-error.js` cố ý không nạp ở 2 màn cũ ⇒ lỗi ở đó vẫn hỏng im lặng |

---

## 5. Recover data

✔ Không cần recover data (Dev kê ở cả 4 journal).

## 6. Mức verify của Dev

| Mục | Nội dung |
|---|---|
| Mức | **`lint`** (chưa có test hành vi / unit / e2e) |
| Lệnh | `php -l` cho toàn bộ tệp PHP đã sửa: không lỗi cú pháp · `node --check` cho `chat-v2.js` + `ajax-error.js`: không lỗi cú pháp · Đối chiếu từng rule bắt buộc với dữ liệu màn hình thực sự gửi lên (đọc payload trong `chat-v2.js`/`common.js`) để không khai bắt buộc nhầm |
| Bằng chứng | Các tham số màn hình **cố ý gửi rỗng** đã xác minh và khai cho phép rỗng: `status` khi bỏ chọn trạng thái (radio giá trị rỗng trong `chat_basic.blade.php`), `conversation` khi chưa chọn hội thoại (`refreshMessage` đã có nhánh trả rỗng sẵn), `id` khi thêm mới ghi chú/trạng thái · Đã xác minh `public/js/chats/right_side/*.js` **KHÔNG** được nạp ở bất kỳ blade nào (mã chết) · Đã xác minh `common.js` còn được nạp bởi 2 màn chat cũ (`chat_basic`, `chat_group`) — **KHÔNG** nạp tệp xử lý lỗi mới ở đó nên KHÔNG thêm lời gọi hàm mới vào `common.js` |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code — **chú ý vòng 3 đã revert, chỉ test theo vòng 4**
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3) — **Dev kê 4.1 là "file thay đổi", không phải function**
- [ ] Mục 4.2 không thiếu data — **Dev kê "không có" nhưng TẦNG 2 đổi phạm vi bản ghi bị UPDATE/DELETE → cần hỏi lại Dev**
- [ ] Mục 4.3 cover được cả happy path lẫn edge case — **thiếu hội thoại NHÓM / màn chat cũ / app mobile admin (T7 do Leader bổ sung, không phải Dev kê)**
- [ ] `config/sns-line.php` đổi key gì — **Dev không mô tả, cần hỏi**
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
