# [FA-001] Chat 1:1 — Logic Spec

## Tong quan
- **Ma tinh nang**: FA-001
- **Ten**: Chat 1:1
- **Phan tich boi**: web-analyzer agent
- **Nguon**: Source code Laravel

---

## 1. Controllers & Actions

### 1.1 `Basic\ChatController`
**File**: `app/Http/Controllers/Basic/ChatController.php` (914 dong)
**Namespace**: `App\Http\Controllers\Basic`
**Dependencies**: `ConversationService`, `ChatService`, `Category` model

| Method | Route | Logic chinh | Side effects |
|--------|-------|-------------|-------------|
| `index()` | GET `/basic/chat-v3` | Render view chat chinh. Nhan `line_id` hoac `friend_id` tu query de pre-select friend | Khong |
| `getFriends()` | GET `/basic/chat/get-friends` | Uy quyen den `ConversationService@getFriend`. Tra ve danh sach + hasMorePage | Khong |
| `confirmReadMessage()` | POST `/basic/chat/confirm-message` | Uy quyen den `ConversationService@confirmReadMessage`. Cap nhat `bots.count_user_unconfirm` | Update `bots` |
| `quickAction()` | POST `/basic/chat/quick-action` | Uy quyen den `ConversationService@quickAction` | Tuy loai action |
| `getBasicInfo()` | GET `/basic/chat/get-basic-info` | Lay step delivery, rich menu, landing (luu nhap) cua friend | Khong |
| `settingFriendDisplayModalV3()` | POST `/basic/chat/setting-friend-display-modal-v3` | Lay toan bo custom fields + default fields cho friend display. Tra ve danh sach nhom (未分類, 基本情報, 国内住所, custom groups) voi gia tri hien tai cua tung field | Khong |
| `removeTagLineUser()` | POST `/basic/chat/remove-tag-line-user` | Xoa tag khoi friend: `tagLineUser::delete()`, giam `tags.count_user_tag` | Delete `tag_line_user`, Update `tags` |
| `getCategoriesTags()` | POST `/basic/chat/get-categories-tags` | Lay tat ca categories + tags voi thong tin `is_selected` cho friend cu the | Khong |
| `getFormAnswerInfo()` | GET `/basic/chat/get-formanswer-info` | Lay cau tra loi form cua friend, nhom theo thang, filter theo nam | Khong |
| `sendMessage()` | POST `/basic/send-message-v2` | Uy quyen den `ChatService@chatMessage` | GUI LINE API, insert `messages_v2s` |
| `sendMedia()` | POST `/basic/send-media-v2` | Uy quyen den `ChatService@sendMedia` | GUI LINE API, upload file, insert `messages_v2s` |
| `sendTemplate()` | POST `/basic/send-template-v2` | Uy quyen den `ChatService@sendTemplate` | GUI LINE API, insert `messages_v2s` |
| `sendSticker()` | POST `/basic/send-sticker-v2` | Uy quyen den `ChatService@chatMessage` (type=sticker) | GUI LINE API, insert `messages_v2s` |
| `getMemosInfo()` | GET `/basic/chat/get-memos-info` | Lay danh sach memos cua conversation, kem `memo_histories` va `staff_info` | Khong |
| `saveMemo()` | POST `/basic/chat/save-memo` | Tao/cap nhat memo. Tao `memo_histories` (toi da 10/memo) | Insert/Update `memos`, Insert `memo_histories` |
| `deleteMemo()` | DELETE `/basic/chat/delete-memo` | Xoa memo va toan bo histories | Delete `memos`, `memo_histories` |
| `saveSortMemo()` | POST `/basic/chat/save-sort-memo` | Cap nhat position cho danh sach memo | Update `memos.position` |
| `syncInfoFromLine()` | POST `/basic/chat/sync-info-from-line` | Goi LINE API lay thong tin moi nhat cua friend (name, avatar). Cap nhat `line_user` | Goi LINE API, Update `line_user` |

**Muc do tin cay**: **Cao** — doc truc tiep tu source code

---

### 1.2 `ChatController` (root)
**File**: `app/Http/Controllers/ChatController.php` (6505 dong)
**Namespace**: `App\Http\Controllers`
**Dependencies**: `BotRepositoryInterface`, `LineUserRepositoryInterface`, `ChatService`, `HelperService`, `MessageV2RepositoryInterface`, `ChatHelper` (app binding)

| Method | Route | Logic chinh | Side effects |
|--------|-------|-------------|-------------|
| `ajaxGetStatusChat()` | POST `/ajax/init-status-chat` | Lay toan bo `status_chat` cua bot hien tai, sap xep theo `position ASC` | Khong |
| `ajaxGetStatusChatV2()` | GET `/ajax/init-status-chat-v2` | Giong V1 nhung co pagination (`per_page` param, mac dinh 100) | Khong |
| `ajaxInitStickerChat()` | POST `/ajax/init-sticker-chat` | Lay toan bo `sticker_package` + `sticker` cua package duoc chon | Khong |
| `ajaxSaveItemStatus()` | POST `/ajax/save-item-status` | Tao hoac cap nhat 1 status. Khi tao moi: day toan bo status cu xuong 1 bac (`position + 1`), dat moi o `position = 1` | Insert/Update `status_chat` |
| `ajaxSaveItemStatusV2()` | POST `/ajax/save-item-status-v2` | Tao/cap nhat nhieu status dong thoi tu mang `data` | Insert/Update `status_chat` |
| `ajaxSaveAllStatus()` | POST `/ajax/save-all-status` | Luu toan bo danh sach status (bulk). Validation: `name_status` bat buoc va <= 10 ky tu, `color` bat buoc | Insert/Update `status_chat` |
| `ajaxDeleteItemStatus()` | POST `/ajax/delete-item-status` | Xoa status. Reset `id_status = null` cho tat ca conversation dang dung status nay. Sync Elasticsearch | Delete `status_chat`, Update `conversation`, Insert `sync_elasticsearch` |
| `ajaxSortStatusChat()` | POST `/ajax/sort-status-chat` | Sap xep lai status theo mang `order` (cap nhat `position`) | Update `status_chat.position` |
| `ajaxSaveHideFriend()` | POST `/ajax/save-hide-friend` | An friend: set `is_hide = 1`. Tu dong xac nhan tin chua doc. Tao message「非表示しました」(`KIND_MESSAGE_HIDE_FRIEND`). Cap nhat badge | Update `conversation`, Delete `unconfirm_message`, Insert `messages_v2s`, Broadcast `InfoEvent` |
| `ajaxSaveHideFriends()` | POST `/ajax/save-hide-friends` | An nhieu friends dong thoi (tuong tu V1 nhung nhan mang `conversationIds`) | Tuong tu EP-14 cho nhieu conversations |
| `refreshMessage()` | GET `/basic/refresh_message` | Lay lich su tin nhan tu nhieu bang: `messages_v2s` → `messages` → `messages_{year}` (sharded). Pagination offset-based | Khong |
| `sendMessage()` | POST (legacy, khong dung) | **Luu y**: Method nay co `return` truoc logic xu ly → **luon tra ve loi**. Day la endpoint V1 da deprecated. Frontend dung V2 (`Basic\ChatController@sendMessage`) | Khong |
| `sendMedia()` | POST (legacy) | Gui media V1. Xu ly upload file truc tiep (image resize, video thumbnail, audio convert). Dung `createMessage()` helper global | Upload file, Goi LINE API |
| `updateStatusConfirm()` | POST `/basic/update-status-confirm` | Thay doi trang thai doi ung. Xu ly 3 loai: `0` (chua xac nhan), `1` (da xac nhan), custom status ID. Cap nhat `conversation`, sync Elasticsearch, broadcast event | Update `conversation`, `messages`, Delete `unconfirm_message`, Insert `sync_elasticsearch`, Broadcast `ChatEvent` + `InfoEvent` |
| `getDataSettingChat()` | GET `/ajax/initial/get-data-setting` | Lay cai dat chat tu `bots` table. Tra ve 8 truong cai dat | Khong |
| `saveSettingChat()` | POST `/ajax/save-data-setting` | Luu cai dat chat. **Canh bao**: dung `$request->all()` de update `bots` → co the nhan bat ky field nao | Update `bots` |
| `getInfoDisplayChat()` | GET `/ajax/info_friend_display_chat11` | Lay cai dat hien thi thong tin friend (custom display) tu `setting_display_info_friend_chat11` | Khong |
| `ajaxGetProfileOfBots()` | POST `/ajax/init-list-bots-profiles` | Lay danh sach profiles gui cua bot. Neu chua co profile mac dinh → tu tao tu `bots` info. Luu profile da chon vao session | Insert `bots_profiles` (neu chua co), Update session |
| `sendActionForUser()` | POST `/basic/chat/send_action` | Goi `HelperService@sendAction`. Tra ve conversation + status moi | Tuy action: co the gui tin, gan tag, thay doi step... |
| `ajaxDownloadFileChat11()` | POST `/ajax/download-file-chat11` | Download file chat (image/audio/pdf). Tra ve base64 encoded data | Khong |
| `getDetailActionMessageChat11()` | POST `/ajax/get-detail-action-message-chat11` | Lay chi tiet templates cua tin nhan action/template. Giai ma `capture_template` | Khong |
| `getDetailActionTrigger()` | POST `/ajax/get-detail-action-trigger` | Lay chi tiet nguon trigger cua action (add friend, tap URL, form, auto reply, step...) | Khong |
| `chatEditRichMenu()` | POST `/basic/chat-edit-rich-menu` | Thay doi rich menu cho friend | Update `bot_line_user.rich_menu_id` |

**Muc do tin cay**: **Cao**

---

### 1.3 `Basic\ScheduleSendChatController`
**File**: `app/Http/Controllers/Basic/ScheduleSendChatController.php` (417 dong)
**Namespace**: `App\Http\Controllers\Basic`

| Method | Route | Logic chinh | Side effects |
|--------|-------|-------------|-------------|
| `saveScheduleSendChat()` | POST `/basic/save-schedule-send` | Tao/cap nhat lich gui. `date_time_send` = timestamp * 1000 (ms). Status 0 = cho gui | Insert/Update `schedule_send_chat` |
| `initDataScheduleSendChat()` | POST `/ajax/initDataScheduleSendChat` | Lay du lieu lich gui hien tai cua conversation (status -1 hoac 0). Load template chi tiet | Khong |
| `removeItemMessageScheduleSendChat()` | POST `/ajax/remove-item-message-schedule-send-chat` | Xoa template khoi lich gui (cap nhat `template_ids`) | Update `schedule_send_chat` |
| `sortScheduleSendChat()` | POST `/ajax/sort-template-schedule-send-chat` | Sap xep lai thu tu template trong lich gui | Update `schedule_send_chat.template_ids` |
| `updateDelayMessageScheduleSendChat()` | POST `/ajax/update-delay-message-scheduled-send` | Bat/tat delay message cho lich gui | Update `schedule_send_chat.is_delay_message` |
| `createMessageByTemplate()` | (chua co route rieng, goi tu view) | Them template vao lich gui. Xu ly logic QuickReply button phai o cuoi | Insert/Update `schedule_send_chat` |
| `cloneScheduleSendByTemplate()` | (chua co route rieng, goi tu view) | Clone template va them vao lich gui | Clone `template`, Update `schedule_send_chat` |
| `cancelScheduleSendChat()` | POST `/basic/cancel-schedule-send-chat` | Huy lich gui: set `status = 2` | Update `schedule_send_chat` |
| `ajaxGetScheduleSendChat()` | POST `/ajax/get-schedule-send-chat` | Kiem tra conversation co lich gui dang cho (status = 0) | Khong |

**Muc do tin cay**: **Cao**

---

### 1.4 `Basic\BasicController@chatSetting`
**File**: `app/Http/Controllers/Basic/BasicController.php:2710`
**Logic**: Chi render view `basic.chat_setting` — khong co logic backend. Toan bo logic cai dat o frontend goi cac AJAX endpoints (EP-26 den EP-34).

---

## 2. Models Eloquent

| Model | DB Table | Connection | Relationships | Ghi chu |
|-------|----------|------------|---------------|---------|
| `Conversation` | `conversation` | mysql | hasMany→`GroupMembers`, hasOne→`LineUser` | Bang chinh luu trang thai hoi thoai |
| `ConversationReplicate` | `conversation` | mysql_db_replicate | Tuong tu Conversation | Read replica, dung khi tim kiem co keyword |
| `LineUser` | `line_user` | mysql | hasMany→`BotLineUser`, `ScenarioLineuser`, `tagLineUser`, `DetailUrlClick`, `ScenarioStepTime` | Thong tin nguoi dung LINE |
| `BotLineUser` | `bot_line_user` | mysql | hasOne→`LineUser`, hasOne→`Bots` | Lien ket bot-user, chua `rich_menu_id`, `is_blocked` |
| `StatusChat` | `status_chat` | mysql | — | Trang thai doi ung tuy chinh |
| `Memos` | `memos` | mysql | — | Ghi chu cho conversation |
| `MemoHistories` | `memo_histories` | mysql | — | Lich su chinh sua memo |
| `MessagesV2` | `messages_v2s` | mysql_message | hasOne→`SourceMessage` | Tin nhan moi (tu 2023+) |
| `Messages` | `messages` | mysql_message | — | Tin nhan cu (truoc khi migrate) |
| `Messages2020`...`Messages2025` | `messages_2020`...`messages_2025` | mysql_message | — | Tin nhan sharded theo nam |
| `MessagesConversationMapping` | `messages_conversation_mapping` | mysql_message | — | Mapping conversation → year co du lieu |
| `SourceMessage` | `source_messages` | mysql_message | — | Thong tin nguon gui tin (broadcast, action, step...) |
| `CaptureTemplate` | `capture_template` | mysql | — | Template da capture (luu tru noi dung gui) |
| `ScheduleSendChat` | `schedule_send_chat` | mysql | — | Lich gui tin nhan |
| `Template` | `template` | mysql | hasMany→`TmpButton` | Mau tin nhan |
| `Tags` | `tags` | mysql | belongsTo→`Category`, hasMany→`tagLineUser` | Tag (nhan) |
| `tagLineUser` | `tag_line_user` | mysql | belongsTo→`Tags` | Lien ket tag-user |
| `Category` | `category` | mysql | hasMany→`Tags` | Nhom tags, templates, scenarios... |
| `Sticker` | `sticker` | mysql | — | Sticker LINE |
| `StickerPackage` | `sticker_package` | mysql | — | Nhom sticker |
| `BotsProfiles` | `bots_profiles` | mysql | — | Profile gui tin (ten + avatar) |
| `Bots` | `bots` | mysql | hasMany→`BotLineUser` | Thong tin bot (chua cai dat chat) |
| `FriendInformationSetting` | `friend_information_setting` | mysql | — | Cai dat custom fields cho friend info |
| `FriendInformationValue` | `friend_information_value` | mysql | — | Gia tri custom fields cua tung friend |
| `SettingDisplayInfoFriendChat11` | `setting_display_info_friend_chat11` | mysql | — | Cai dat hien thi thong tin friend trong chat 1:1 |
| `UnconfirmMessage` | `unconfirm_message` | mysql | hasOne→`Conversation` | Tin nhan chua xac nhan |
| `SyncElasticsearch` | `sync_elasticsearch` | mysql | — | Queue dong bo Elasticsearch |
| `FormAnswerResult` | `form_answer_result` | mysql | hasMany→`FormAnswerDetail` | Ket qua tra loi form |

**Muc do tin cay**: **Cao** — doc tu `models.md` index va truc tiep import trong controllers

---

## 3. Services / Repositories

### 3.1 `ChatService`
**File**: `app/Services/ChatService.php`
**Dependencies**: `BotRepositoryInterface`, `LineUserRepositoryInterface`, `MessageService`, `TemplateRepositoryInterface`, `TemplateService`, `MessageV2RepositoryInterface`, `SourceMessageRepositoryInterface`, `CaptureTemplateRepositoryInterface`, `BotLineUserRepositoryInterface`

**Methods chinh:**

| Method | Mo ta | Logic |
|--------|-------|-------|
| `chatMessage($request)` | Gui tin text/sticker (V2) | Kiem tra block → lay profile → tao message data → goi `MessageService@createMessageV2` → tang free_send_count → cap nhat unconfirm count neu bat |
| `sendMedia($request)` | Gui media (V2) | Kiem tra block → setMessage → chunk thanh nhom 5 → goi `MessageService@createMultipleMessageV2` |
| `sendTemplate($request)` | Gui template (V2) | Tuong tu sendMedia nhung cho templates |
| `setMessage($request, ...)` | Helper tao message object | Xu ly type (text/image/video/audio/pdf/sticker), tao structure phu hop LINE API |

**Muc do tin cay**: **Cao**

### 3.2 `ConversationService`
**File**: `app/Services/ConversationService.php`
**Dependencies**: `ConversationRepositoryInterface`, `BotRepositoryInterface`, `HelperService`, `MessageService`, `LineUserRepositoryInterface`, `MessageV2RepositoryInterface`

**Methods chinh:**

| Method | Mo ta | Logic |
|--------|-------|-------|
| `getFriend($request)` | Lay danh sach friends | Query `conversation` JOIN `line_user` JOIN `status_chat`. Filter theo type (all/unconfirm/confirm/hide/schedule/groupChat). Tim kiem LIKE tren name/view_name. Filter theo tags (AND/OR). Sap xep bookmark desc → last_time_message desc. Pagination 20/page |
| `confirmReadMessage($request)` | Danh dau da doc | Cap nhat trang thai xac nhan cho conversations |
| `quickAction($request)` | Quick action | Thuc hien action nhanh cho friend |

**Muc do tin cay**: **Cao** — doc truc tiep code

### 3.3 `HelperService`
**File**: `app/Services/HelperService.php`
**Su dung boi**: `ChatController@sendActionForUser`

| Method | Mo ta |
|--------|-------|
| `sendAction($actionId, $lineId, $botId, ...)` | Thuc hien action tu dong: co the gui tin nhan, gan tag, thay doi step delivery, chuyen rich menu... |

**Muc do tin cay**: **Trung binh** — chua doc truc tiep noi dung method, suy luan tu cach goi

### 3.4 `MessageService`
**File**: `app/Services/MessageService.php`
**Su dung boi**: `ChatService`, `ConversationService`

| Method | Mo ta |
|--------|-------|
| `createMessageV2(...)` | Tao tin nhan V2: luu vao `messages_v2s`, gui qua LINE API, cap nhat conversation |
| `createMultipleMessageV2(...)` | Gui nhieu tin nhan (chunk 5 theo gioi han LINE API) |

**Muc do tin cay**: **Trung binh** — suy luan tu context goi

---

## 4. Form Requests / Validation

**Khong su dung FormRequest classes** cho tinh nang Chat 1:1. Validation duoc thuc hien truc tiep trong controller/service:

| Endpoint | Rule | Code |
|----------|------|------|
| EP-08 (send message) | `message` khong duoc rong | `ChatService@chatMessage` line 81: `if (empty($request->message))` |
| EP-08 (send message) | User khong bi block | `ChatService@chatMessage` line 77: check `conversation.is_blocked = 1` |
| EP-28 (save status) | `name_status` bat buoc | `ChatController@ajaxSaveAllStatus` line 734 |
| EP-28 (save status) | `name_status` <= 10 ky tu | `ChatController@ajaxSaveAllStatus` line 737: `mb_strlen($item->name_status) > 10` |
| EP-28 (save status) | `color` bat buoc | `ChatController@ajaxSaveAllStatus` line 740 |

**Muc do tin cay**: **Cao** — doc truc tiep tu code

---

## 5. Events / Listeners / Queued Jobs

### Events (Broadcast)

| Event | Class | Mo ta | Trigger boi |
|-------|-------|-------|-------------|
| `ChatEvent` | `App\Events\ChatEvent` | Gui tin nhan moi den client qua WebSocket | Khi co tin nhan moi (gui/nhan) |
| `InfoEvent` | `App\Events\InfoEvent` | Cap nhat badge so tin chua doc | `updateStatusConfirm`, `ajaxSaveHideFriend`, `ajaxDeleteItemStatus` |
| `CommontEvent` | `App\Events\CommontEvent` | Event chung | Cac thao tac khac |
| `LeaveRoom` | `App\Events\LeaveRoom` | Roi phong chat | Khi roi group chat |

### Queued Jobs
**Truc tiep trong Chat 1:1**: Khong phat hien queued job. Tuy nhien:
- `ScheduleSendChat` (lich gui) co `status` field, **can background job (Spring Boot) de thuc su gui** khi den thoi diem. Field `date_time_send` (timestamp ms) duoc dung de xac dinh thoi gian gui.
- `SyncElasticsearch::insertElasticsearch()` insert ban ghi de **background job dong bo** sang Elasticsearch

**Ghi chu cho job-analyzer**: Can tim trong Spring Boot:
1. Job xu ly `schedule_send_chat` (status = 0, `date_time_send` <= now)
2. Job xu ly `sync_elasticsearch` queue

**Muc do tin cay**: **Cao** (phat hien tu code), **Trung binh** (doi voi Spring Boot jobs — chua xac nhan)

---

## 6. Authorization (Policies, Gates)

**Khong su dung Laravel Policies/Gates** cho tinh nang Chat 1:1. Authorization duoc xu ly:

1. **Session-based**: Middleware `web` kiem tra dang nhap
2. **Bot scoping**: Moi query deu filter theo `bot_id = getBotId()` tu session → dam bao chi truy cap du lieu cua bot hien tai
3. **Staff permissions**: Khong phat hien kiem tra quyen Staff trong code Chat 1:1 — **co the Staff co toan quyen chat neu duoc gan menu** (can xac nhan voi phan quan ly Staff)

**Muc do tin cay**: **Cao** (viec thieu authorization check la chinh xac theo code)

---

## 7. Business Rules (tong hop tu code)

### BR-01: Luu nhap (流入経路)
- Khi hien thi thong tin friend, he thong tra cuu bang `detail_landing_click` voi `action = 2` (friend add)
- Lay `landing.name` lam ten luu nhap
- **File**: `Basic\ChatController@getBasicInfo:256`
- **Muc do tin cay**: **Cao**

### BR-02: Sap xep friend list
- Mac dinh: `is_bookmark DESC`, `last_time_message DESC`
- Friend duoc bookmark (ghim) luon o dau danh sach
- **File**: `ConversationService@getFriend:185`
- **Muc do tin cay**: **Cao**

### BR-03: Filter friend list — logic chuyen doi
- Khi tim kiem co keyword (`searchKey` khong rong): dung `ConversationReplicate` (read replica) thay vi `Conversation` chinh → giam tai master DB
- **File**: `ConversationService@getFriend:96-100`
- **Muc do tin cay**: **Cao**

### BR-04: Tag filter AND/OR
- **OR**: Friend phai co IT NHAT 1 tag trong danh sach (`whereIn tag_id, havingRaw COUNT > 0`)
- **AND**: Friend phai co TAT CA tags trong danh sach (`havingRaw COUNT = len_arr`)
- **File**: `ConversationService@getFriend:162-170`
- **Muc do tin cay**: **Cao**

### BR-05: An friend — tu dong xac nhan
- Khi an friend, tat ca tin nhan chua xac nhan se tu dong duoc xac nhan
- He thong tao tin nhan he thong「非表示しました」(`msg_kind = KIND_MESSAGE_HIDE_FRIEND`)
- **File**: `ChatController@ajaxSaveHideFriend:876-897`
- **Muc do tin cay**: **Cao**

### BR-06: Xoa status — cascade
- Khi xoa status, tat ca conversation dang su dung status nay se bi reset ve `id_status = null`
- Dong thoi sync Elasticsearch cho tung conversation bi anh huong
- **File**: `ChatController@ajaxDeleteItemStatus:799-810`
- **Muc do tin cay**: **Cao**

### BR-07: Gioi han gui mien phi
- Bot free plan (`plan_type = 2`): gioi han 1000 tin/thang
- Khi `free_send_count >= 1000` → tra loi loi「配信数上限に達しています」
- Moi tin gui thanh cong: `free_send_count += 1`
- **File**: `ChatService@chatMessage:95-103`
- **Muc do tin cay**: **Cao**

### BR-08: Tu dong xac nhan khi tra loi
- Neu cai dat `bots.confirm_message_user_send = 1` (EP-33/34):
  - Khi Admin/Staff gui tin tra loi → he thong tu dong cap nhat so tin chua xac nhan
  - `count_user_unconfirm` duoc tinh lai qua helper `totalUserConfirmMessage()`
- **File**: `ChatService@chatMessage:104-110`
- **Muc do tin cay**: **Cao**

### BR-09: Block check truoc khi gui
- Truoc khi gui bat ky tin nhan nao (text/media/template/sticker), he thong kiem tra `conversation.is_blocked = 1`
- Neu bi block → tra loi loi「ブロックしていますので、メッセージが送信できません。」
- **File**: `ChatService@chatMessage:76-79`, `ChatService@sendMedia:139-142`
- **Muc do tin cay**: **Cao**

### BR-10: Message sharding theo nam
- Tin nhan duoc luu vao cac bang khac nhau theo nam: `messages_v2s` (moi nhat), `messages` (cu), `messages_2020`...`messages_2025`
- Khi lay lich su: query `messages_v2s` truoc → fallback `messages` → fallback `messages_{year}` tu moi den cu
- `messages_conversation_mapping` cho biet conversation co du lieu o nam nao
- **File**: `ChatController@refreshMessage:2075-2210`
- **Muc do tin cay**: **Cao**

### BR-11: Lich gui tin nhan (Schedule Send)
- Lich gui co 3 trang thai: `status = -1` (moi tao, chua set thoi gian), `0` (dang cho gui), `2` (da huy)
- Template duoc luu dang CSV IDs trong `template_ids`
- `date_time_send` luu dang timestamp * 1000 (milliseconds) de Spring Boot xu ly
- Viec thuc su gui tin nhan do **Spring Boot background job** dam nhan (khong phai Laravel)
- **File**: `ScheduleSendChatController@saveScheduleSendChat:30-56`
- **Muc do tin cay**: **Cao**

### BR-12: Validation ten trang thai
- Ten trang thai (`name_status`) bat buoc va toi da 10 ky tu (Unicode, dung `mb_strlen`)
- Mau sac (`color`) bat buoc
- Thong bao loi bang tieng Nhat:「ステータス必ず指定してください。」,「ステータス名は10文字以下にしてください。」,「カラー必ず指定してください。」
- **File**: `ChatController@ajaxSaveAllStatus:734-741`
- **Muc do tin cay**: **Cao**

### BR-13: Memo history — gioi han 10
- Moi memo chi luu toi da 10 ban ghi history
- Khi vuot qua → xoa ban ghi cu nhat (`orderBy id ASC, limit 1, delete`)
- History ghi lai `staff_id` va `action_type` (new/edit)
- **File**: `Basic\ChatController@saveMemo:785-793`
- **Muc do tin cay**: **Cao**

### BR-14: Profile gui tin
- Admin/Staff co the chon profile gui (ten + avatar) khac nhau
- Profile mac dinh tu bot info (`bots.bot_image`, `bots.view_name`)
- Neu chua co profile → tu dong tao 1 profile mac dinh
- Profile duoc chon luu trong session, dinh kem vao moi tin nhan gui (`messages_v2s.profile_send`)
- **File**: `ChatController@ajaxGetProfileOfBots:1070-1132`
- **Muc do tin cay**: **Cao**

### BR-15: URL rut gon tu dong
- Khi `bots.is_shorten_url = 1` va gui tin text:
  - URL trong tin nhan duoc chuyen thanh URL rut gon qua `ChatHelper@sendShortUrl`
  - Cho phep theo doi thong ke truy cap (FA-023 URL Analysis)
- **File**: `ChatController@sendMessage:1951-1964`
- **Muc do tin cay**: **Cao**

### BR-16: Sync thong tin tu LINE
- Khi user bam sync, he thong goi LINE API `getInfoFromLine` hoac `getInfoGroupFromLine`
- Cap nhat `line_user.name`, `line_user.avatar_url`, `line_user.status_message`
- **File**: `Basic\ChatController@syncInfoFromLine:846-884`
- **Muc do tin cay**: **Cao**

### BR-17: Custom friend info display
- Admin co the tuy chinh fields hien thi trong panel thong tin friend
- Cau hinh luu trong `setting_display_info_friend_chat11`
- Co 2 loai: `type = 0` (default fields: ten, email, SDT, ngay sinh...) va `type = 1` (custom fields tu `friend_information_setting`)
- Sap xep theo `order ASC`
- **File**: `ChatController@getInfoDisplayChat:3961-4028`, `Basic\ChatController@settingFriendDisplayModalV3:278-496`
- **Muc do tin cay**: **Cao**

---

## 8. Ghi chu bo sung

### Cac tinh nang lien quan (cross-reference)
| Tinh nang | Lien ket | Mo ta |
|-----------|---------|-------|
| SC-001 | Template Selector | Chon template khi gui tin nhan |
| SC-002 | Tag Selector | Chon tag khi gan tag nhanh |
| SC-004 | Action Selector | Chon action khi thuc hien action |
| SC-005 | Media Selector | Chon media khi gui hinh anh/video |
| SC-007 | Schedule Send | Dialog hen gio gui |
| FA-010 | Template Management | Quan ly mau tin nhan |
| FA-011 | Form Creation | Tao bieu mau (hien thi ket qua trong tab 4) |
| FA-015 | Friend Info Management | Quan ly custom fields (hien thi trong tab 2) |
| FA-023 | URL Analysis | Phan tich URL rut gon |

### Endpoint deprecated (V1 → V2)
| V1 (khong dung nua) | V2 (dang dung) | Ghi chu |
|---------------------|----------------|---------|
| `ChatController@sendMessage` | `Basic\ChatController@sendMessage` | V1 luon tra loi loi (co `return` truoc logic) |
| `ChatController@sendMedia` | `Basic\ChatController@sendMedia` | V2 dung `ChatService` |
| `ChatController@getFriends` (private) | `Basic\ChatController@getFriends` | V2 dung `ConversationService` |

### Helper functions quan trong (global)
| Function | File | Mo ta |
|----------|------|-------|
| `getBotId()` | `app/Helpers/functions.php` | Lay bot ID tu session |
| `getCurrentUser()` | `app/Helpers/functions.php` | Lay user ID hien tai |
| `createMessage(...)` | `app/Helpers/ChatMessages.php` | Tao va gui tin nhan (V1) |
| `returnResponseSendMessage(...)` | `app/Helpers/ChatMessages.php` | Format response gui tin (V1) |
| `returnResponseSendMessageV2(...)` | `app/Helpers/ChatMessages.php` | Format response gui tin (V2) |
| `totalUserConfirmMessage($botId)` | `app/Helpers/functions.php` | Dem so user chua xac nhan |
| `updateMessageSendCount(...)` | `app/Helpers/functions.php` | Cap nhat so tin da gui theo ngay |
| `updateBadge($bot)` | `app/Helpers/functions.php` | Cap nhat badge so tin chua doc |
| `notifyChatworkChat11($message)` | `app/Helpers/functions.php` | Gui thong bao loi den Chatwork |
| `addLogUserAction($action)` | `app/Helpers/functions.php` | Ghi log hanh dong user |

**Muc do tin cay**: **Cao** — xac dinh tu `use` statements va goi truc tiep trong code
