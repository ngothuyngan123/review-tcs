# [FA-001] Chat 1:1 — API Spec

## Tong quan
- **Ma tinh nang**: FA-001
- **Ten**: Chat 1:1
- **Phan tich boi**: web-analyzer agent
- **Nguon**: Source code Laravel — `Basic\ChatController`, `ChatController`, `Basic\ScheduleSendChatController`, `Basic\BasicController`, `Basic\FriendlistController`, `ChatService`, `ConversationService`

---

## Tong hop Endpoints

| EP | Method | URL | Controller@Action | Mo ta | Man hinh |
|----|--------|-----|-------------------|-------|----------|
| EP-01 | GET | `/basic/chat-v3` | `Basic\ChatController@index` | Trang chinh chat 1:1 (render view) | SCR-CHT-01 |
| EP-02 | GET | `/basic/chat-setting` | `Basic\BasicController@chatSetting` | Trang cai dat chat (render view) | SCR-CHT-02 |
| EP-03 | GET | `/basic/chat/get-friends` | `Basic\ChatController@getFriends` | Lay danh sach ban be co filter, search, pagination | SCR-CHT-01 |
| EP-04 | GET | `/basic/chat/get-basic-info` | `Basic\ChatController@getBasicInfo` | Lay thong tin co ban cua friend (step, rich menu, landing) | SCR-CHT-01 |
| EP-05 | GET | `/basic/refresh_message` | `ChatController@refreshMessage` | Lay lich su tin nhan cua conversation | SCR-CHT-01 |
| EP-06 | GET | `/basic/chat/get-memos-info` | `Basic\ChatController@getMemosInfo` | Lay danh sach memo cua conversation | SCR-CHT-01 |
| EP-07 | GET | `/basic/chat/get-formanswer-info` | `Basic\ChatController@getFormAnswerInfo` | Lay cau tra loi bieu mau cua friend | SCR-CHT-01 |
| EP-08 | POST | `/basic/send-message-v2` | `Basic\ChatController@sendMessage` | Gui tin nhan text (v2, dung ChatService) | SCR-CHT-01 |
| EP-09 | POST | `/basic/send-media-v2` | `Basic\ChatController@sendMedia` | Gui media: image/video/audio/pdf (v2, dung ChatService) | SCR-CHT-01 |
| EP-10 | POST | `/basic/send-template-v2` | `Basic\ChatController@sendTemplate` | Gui tin nhan tu template (v2, dung ChatService) | SCR-CHT-01 |
| EP-11 | POST | `/basic/send-sticker-v2` | `Basic\ChatController@sendSticker` | Gui sticker LINE (v2, dung ChatService) | SCR-CHT-01 |
| EP-12 | POST | `/basic/chat/confirm-message` | `Basic\ChatController@confirmReadMessage` | Danh dau tin nhan da doc/xac nhan | SCR-CHT-01 |
| EP-13 | POST | `/basic/update-status-confirm` | `ChatController@updateStatusConfirm` | Thay doi trang thai doi ung (status) cua conversation | SCR-CHT-01 |
| EP-14 | POST | `/ajax/save-hide-friend` | `ChatController@ajaxSaveHideFriend` | An 1 friend khoi danh sach | SCR-CHT-01 |
| EP-15 | POST | `/ajax/save-hide-friends` | `ChatController@ajaxSaveHideFriends` | An nhieu friends khoi danh sach | SCR-CHT-01 |
| EP-16 | POST | `/ajax/remove-hide-friend` | `Basic\FriendlistController@removeHideFriend` | Hien lai friend da bi an | SCR-CHT-01 |
| EP-17 | POST | `/basic/chat/quick-action` | `Basic\ChatController@quickAction` | Thuc hien quick action cho friend | SCR-CHT-01 |
| EP-18 | POST | `/basic/chat/send_action` | `ChatController@sendActionForUser` | Gui action tu dong cho friend | SCR-CHT-01 |
| EP-19 | POST | `/basic/chat/setting-friend-display-modal-v3` | `Basic\ChatController@settingFriendDisplayModalV3` | Lay thong tin hien thi friend (custom fields, default info) | SCR-CHT-01 |
| EP-20 | POST | `/basic/chat/get-categories-tags` | `Basic\ChatController@getCategoriesTags` | Lay danh sach categories va tags de gan cho friend | SCR-CHT-01 |
| EP-21 | POST | `/basic/chat/remove-tag-line-user` | `Basic\ChatController@removeTagLineUser` | Xoa tag khoi friend | SCR-CHT-01 |
| EP-22 | POST | `/basic/chat/sync-info-from-line` | `Basic\ChatController@syncInfoFromLine` | Dong bo thong tin friend tu LINE API | SCR-CHT-01 |
| EP-23 | POST | `/basic/chat/save-memo` | `Basic\ChatController@saveMemo` | Tao/cap nhat memo cho conversation | SCR-CHT-01 |
| EP-24 | DELETE | `/basic/chat/delete-memo` | `Basic\ChatController@deleteMemo` | Xoa memo | SCR-CHT-01 |
| EP-25 | POST | `/basic/chat/save-sort-memo` | `Basic\ChatController@saveSortMemo` | Sap xep lai thu tu memo | SCR-CHT-01 |
| EP-26 | POST | `/ajax/init-status-chat` | `ChatController@ajaxGetStatusChat` | Lay danh sach trang thai doi ung (all) | SCR-CHT-01, SCR-CHT-02 |
| EP-27 | GET | `/ajax/init-status-chat-v2` | `ChatController@ajaxGetStatusChatV2` | Lay danh sach trang thai doi ung (co pagination) | SCR-CHT-02 |
| EP-28 | POST | `/ajax/save-item-status` | `ChatController@ajaxSaveItemStatus` | Tao/cap nhat 1 trang thai doi ung | SCR-CHT-02 |
| EP-29 | POST | `/ajax/save-item-status-v2` | `ChatController@ajaxSaveItemStatusV2` | Tao/cap nhat nhieu trang thai dong thoi | SCR-CHT-02 |
| EP-30 | POST | `/ajax/save-all-status` | `ChatController@ajaxSaveAllStatus` | Luu toan bo trang thai (bulk save) | SCR-CHT-02 |
| EP-31 | POST | `/ajax/delete-item-status` | `ChatController@ajaxDeleteItemStatus` | Xoa 1 trang thai doi ung | SCR-CHT-02 |
| EP-32 | POST | `/ajax/sort-status-chat` | `ChatController@ajaxSortStatusChat` | Sap xep lai thu tu trang thai | SCR-CHT-02 |
| EP-33 | GET | `/ajax/initial/get-data-setting` | `ChatController@getDataSettingChat` | Lay cai dat chat hien tai (shortcut, shorten URL, auto-confirm...) | SCR-CHT-02 |
| EP-34 | POST | `/ajax/save-data-setting` | `ChatController@saveSettingChat` | Luu cai dat chat | SCR-CHT-02 |
| EP-35 | GET | `/ajax/info_friend_display_chat11` | `ChatController@getInfoDisplayChat` | Lay cai dat hien thi thong tin friend tuy chinh | SCR-CHT-01 |
| EP-36 | POST | `/ajax/init-sticker-chat` | `ChatController@ajaxInitStickerChat` | Lay danh sach sticker packages va stickers | SCR-CHT-01 |
| EP-37 | POST | `/ajax/init-list-bots-profiles` | `ChatController@ajaxGetProfileOfBots` | Lay danh sach profiles (ten gui) cua bot | SCR-CHT-01 |
| EP-38 | POST | `/ajax/get-bot-data` | `Admin\BotController@getBotData` | Lay thong tin bot hien tai | SCR-CHT-01 |
| EP-39 | POST | `/ajax/download-file-chat11` | `ChatController@ajaxDownloadFileChat11` | Download file (image/audio/pdf) tu chat | SCR-CHT-01 |
| EP-40 | POST | `/ajax/get-detail-action-message-chat11` | `ChatController@getDetailActionMessageChat11` | Lay chi tiet template cua tin nhan action/template | SCR-CHT-01 |
| EP-41 | POST | `/ajax/get-detail-action-trigger` | `ChatController@getDetailActionTrigger` | Lay chi tiet nguon trigger cua action message | SCR-CHT-01 |
| EP-42 | POST | `/basic/save-schedule-send` | `Basic\ScheduleSendChatController@saveScheduleSendChat` | Tao/cap nhat lich gui tin nhan hen | SCR-CHT-01 |
| EP-43 | POST | `/ajax/initDataScheduleSendChat` | `Basic\ScheduleSendChatController@initDataScheduleSendChat` | Lay du lieu lich gui hien tai cua conversation | SCR-CHT-01 |
| EP-44 | POST | `/ajax/remove-item-message-schedule-send-chat` | `Basic\ScheduleSendChatController@removeItemMessageScheduleSendChat` | Xoa template khoi lich gui | SCR-CHT-01 |
| EP-45 | POST | `/ajax/sort-template-schedule-send-chat` | `Basic\ScheduleSendChatController@sortScheduleSendChat` | Sap xep template trong lich gui | SCR-CHT-01 |
| EP-46 | POST | `/ajax/update-delay-message-scheduled-send` | `Basic\ScheduleSendChatController@updateDelayMessageScheduleSendChat` | Cap nhat cai dat delay message trong lich gui | SCR-CHT-01 |
| EP-47 | POST | `/basic/cancel-schedule-send-chat` | `Basic\ScheduleSendChatController@cancelScheduleSendChat` | Huy lich gui tin nhan | SCR-CHT-01 |
| EP-48 | POST | `/ajax/get-schedule-send-chat` | `Basic\ScheduleSendChatController@ajaxGetScheduleSendChat` | Kiem tra conversation co lich gui dang cho khong | SCR-CHT-01 |
| EP-49 | POST | `/basic/chat-edit-rich-menu` | `ChatController@chatEditRichMenu` | Thay doi rich menu cho friend | SCR-CHT-01 |

### Middleware chung
Tat ca endpoints web portal dung middleware: `web`, `NotifyChatworkRequestTimeSlow`, `LogRequestMultipart`
Mot so endpoint them: xac thuc session-based (auto qua web middleware)

---

## Chi tiet tung Endpoint

### EP-03: GET `/basic/chat/get-friends`
**Controller**: `Basic\ChatController@getFriends` (`app/Http/Controllers/Basic/ChatController.php:172`)
**Uy quyen den**: `ConversationService@getFriend`
**Muc do tin cay**: **Cao** — doc truc tiep tu code

#### Request params
| Ten | Vi tri | Kieu | Bat buoc | Mo ta |
|-----|--------|------|---------|-------|
| `searchKey` | query | string | Khong | Tu khoa tim kiem theo LINE name hoac system display name |
| `searchTag` | query | string | Khong | Danh sach tag IDs, cach boi dau phay (vd: "1,2,3") |
| `searchStatusOr` | query | string | Khong | Danh sach status IDs (filter OR), cach boi dau phay |
| `searchStatusAnd` | query | string | Khong | Status ID (filter AND) |
| `filterTypeFriend` | query | string | Co | Loai filter: `all`, `unconfirm`, `confirm`, `hide`, `schedule`, `groupChat` |
| `filterFriendOrAnd` | query | string | Khong | Kieu loc: `or` hoac `and` |
| `lineId` | query | integer | Khong | ID cua line user cu the (de select) |
| `page` | query | integer | Co | So trang (bat dau tu 1), moi trang 20 items |
| `botIdCurrent` | query | integer | Khong | Bot ID (mac dinh lay tu session) |

#### Response thanh cong (200)
```json
{
  "success": true,
  "data": {
    "friendList": [
      {
        "line_user_id": "U...",
        "is_blocked": 0,
        "memo": "...",
        "conversation_id": 123,
        "bot_id": 1,
        "last_msg": 1,
        "content": "Noi dung tin nhan cuoi",
        "total_confirm": 0,
        "special_status": 1,
        "is_bookmark": 0,
        "id_status": 5,
        "time_newest_reiceve": 1711234567,
        "line_name": "Ten LINE",
        "name": "Ten LINE",
        "avatar_url": "https://...",
        "view_name": "Ten he thong",
        "real_name": "Ten that",
        "type": 0,
        "name_status": "Dang xu ly",
        "color": "#ff0000",
        "bg_status": "#ffeeee",
        "id": 456,
        "followed_at": "2026-01-01 00:00:00"
      }
    ],
    "line_id": null,
    "name": null,
    "hasMorePage": true
  }
}
```

#### Logic chinh (tu `ConversationService@getFriend`)
- Query tu bang `conversation` JOIN `line_user` JOIN `status_chat`
- Filter theo `filterTypeFriend`:
  - `all`: `is_hide = 0`
  - `unconfirm`: `confirm_count = 1`
  - `confirm`: `confirm_count = 0`
  - `hide`: `is_hide = 1`
  - `schedule`: conversation co trong `schedule_send_chat` voi `status = 0`
  - `groupChat`: `conversation_kind = 1`
- Tim kiem theo `searchKey`: LIKE tren `line_user.name` va `line_user.view_name`
- Filter theo tags: dung `tag_line_user` table, ho tro AND/OR logic
- Sap xep: `is_bookmark DESC`, `last_time_message DESC`
- Phan trang: offset-based, 20 items/page

---

### EP-04: GET `/basic/chat/get-basic-info`
**Controller**: `Basic\ChatController@getBasicInfo` (`app/Http/Controllers/Basic/ChatController.php:227`)
**Muc do tin cay**: **Cao**

#### Request params
| Ten | Vi tri | Kieu | Bat buoc | Mo ta |
|-----|--------|------|---------|-------|
| `line_user_id` | query | integer | Co | ID cua line user |

#### Response thanh cong (200)
```json
{
  "success": true,
  "scenario": {
    "line_user_id": 123,
    "scenario_id": 5,
    "bot_id": 1,
    "name": "Ten step delivery"
  },
  "nextScenario": {
    "send_time": "2026-03-25 10:00:00",
    "stepMessage": { "..." }
  },
  "richMenu": {
    "id": 10,
    "name": "Menu chinh"
  },
  "qr_code_name": "landing page name"
}
```

#### Logic chinh
- Lay step delivery dang chay: `scenario` JOIN `scenario_lineuser` WHERE `is_following = 1`
- Lay step tiep theo: `scenario_step_time` WHERE `status = 0` ORDER BY `send_time ASC`
- Lay rich menu: `bot_line_user.rich_menu_id` → `rich_menus`
- Lay landing (luu nhap): `detail_landing_click` WHERE `action = 2` ORDER BY `id ASC`

---

### EP-05: GET `/basic/refresh_message`
**Controller**: `ChatController@refreshMessage` (`app/Http/Controllers/ChatController.php:2019`)
**Muc do tin cay**: **Cao**

#### Request params
| Ten | Vi tri | Kieu | Bat buoc | Mo ta |
|-----|--------|------|---------|-------|
| `conversation` | query | integer | Co | Conversation ID |
| `line_user_id` | query | integer | Co | Line user ID |
| `page` | query | integer | Khong | So trang (mac dinh 1) |
| `currentYear` | query | integer | Khong | Nam hien tai de query (0 = moi nhat) |
| `offset` | query | integer | Khong | Offset (mac dinh 0) |
| `botIdCurrent` | query | integer | Khong | Bot ID |

#### Response thanh cong (200)
```json
{
  "success": true,
  "data": [
    {
      "id": 1000,
      "msg_kind": 0,
      "type": "text",
      "content": "Noi dung tin nhan",
      "user_id": 5,
      "created_at": "2026-03-24 13:30:00",
      "updated_at": "2026-03-24 13:30:00",
      "is_message_new": 1,
      "quote_token": 0,
      "templates": [],
      "source_messages": null,
      "username": "Admin Name"
    }
  ],
  "more_page": true,
  "currentYear": 0,
  "offset": 20,
  "conversation": { "..." },
  "isHasMsg": true,
  "hasDeleteMessage": 0
}
```

#### Logic chinh
- Query tu `messages_v2s` (bang moi nhat) voi pagination offset-based
- Neu khong du tin nhan → fallback sang bang `messages` (cu), roi sang `messages_2025`, `messages_2024`... (sharded theo nam)
- Moi tin nhan co the co `source_messages` (thong tin nguon: broadcast, action, step...)
- Tin nhan loai template co `list_capture_template_id` → query `capture_template` de lay noi dung
- Sap xep: `messages_v2s.id DESC`
- So luong moi lan: `config('sns-line.post_per_page_message')` (cau hinh)

---

### EP-08: POST `/basic/send-message-v2`
**Controller**: `Basic\ChatController@sendMessage` (`app/Http/Controllers/Basic/ChatController.php:700`)
**Uy quyen den**: `ChatService@chatMessage`
**Muc do tin cay**: **Cao**

#### Request params
| Ten | Vi tri | Kieu | Bat buoc | Mo ta |
|-----|--------|------|---------|-------|
| `to_user` | body | integer | Co | Line user ID nguoi nhan |
| `conversation` | body | integer | Co | Conversation ID |
| `message` | body | string | Co | Noi dung tin nhan text |
| `botIdCurrent` | body | integer | Khong | Bot ID |

#### Response thanh cong (200)
```json
{
  "success": true,
  "message": {
    "type": "text",
    "content": "Noi dung tin nhan",
    "msg_id": 123
  }
}
```

#### Loi co the xay ra
| HTTP | Ma loi | Mo ta |
|------|--------|-------|
| 200 | `success: false` | User bi blocked: 「ブロックしていますので、メッセージが送信できません。」 |
| 200 | `success: false` | Tin nhan rong |
| 200 | `success: false, limit_max: true` | Vuot qua gioi han gui mien phi (1000 tin/free plan) |
| 200 | `success: false` | Loi gui LINE API |

#### Logic chinh (ChatService)
- Kiem tra user khong bi block (`conversation.is_blocked`)
- Kiem tra message khong rong
- Lay profile gui (`profiles_selected_{botId}_{userId}` tu session)
- Tao message qua `MessageService@createMessageV2` → gui LINE API
- Neu thanh cong: tang `free_send_count` cua bot, cap nhat `message_send_count`
- Neu cai dat `confirm_message_user_send` bat: tu dong cap nhat unconfirm count

---

### EP-09: POST `/basic/send-media-v2`
**Controller**: `Basic\ChatController@sendMedia` (`app/Http/Controllers/Basic/ChatController.php:707`)
**Uy quyen den**: `ChatService@sendMedia`
**Muc do tin cay**: **Cao**

#### Request params
| Ten | Vi tri | Kieu | Bat buoc | Mo ta |
|-----|--------|------|---------|-------|
| `to_user` | body | integer | Co | Line user ID nguoi nhan |
| `conversation` | body | integer | Co | Conversation ID |
| `messages` | body | array | Co | Mang cac message objects |
| `botIdCurrent` | body | integer | Khong | Bot ID |

Moi message object trong mang co the la:
- `type`: `image`, `video`, `audio`, `pdf`
- `file`: file upload (FormData)
- Hoac `media_id`: ID tu Media library

#### Logic chinh (ChatService)
- Kiem tra user khong bi block
- Chunk messages thanh nhom 5 (gioi han LINE API)
- Moi nhom gui qua `MessageService@createMultipleMessageV2`
- Image: resize 1040px width, tao thumbnail 240px
- Video: tao thumbnail tu frame dau, tinh duration
- Audio: convert sang M4A neu can, tinh duration
- PDF: luu file, gui dang text link

---

### EP-10: POST `/basic/send-template-v2`
**Controller**: `Basic\ChatController@sendTemplate` (`app/Http/Controllers/Basic/ChatController.php:714`)
**Uy quyen den**: `ChatService@sendTemplate`
**Muc do tin cay**: **Cao**

#### Request params
| Ten | Vi tri | Kieu | Bat buoc | Mo ta |
|-----|--------|------|---------|-------|
| `to_user` | body | integer | Co | Line user ID |
| `conversation` | body | integer | Co | Conversation ID |
| `template_ids` | body | string | Co | Danh sach template IDs, cach boi dau phay |
| `botIdCurrent` | body | integer | Khong | Bot ID |

---

### EP-11: POST `/basic/send-sticker-v2`
**Controller**: `Basic\ChatController@sendSticker` (`app/Http/Controllers/Basic/ChatController.php:721`)
**Uy quyen den**: `ChatService@chatMessage` (cung method gui text, truyen type sticker)
**Muc do tin cay**: **Cao**

#### Request params
| Ten | Vi tri | Kieu | Bat buoc | Mo ta |
|-----|--------|------|---------|-------|
| `to_user` | body | integer | Co | Line user ID |
| `conversation` | body | integer | Co | Conversation ID |
| `message` | body | object | Co | Sticker data (packageId, stickerId) |
| `type` | body | string | Co | Gia tri: `sticker` |

---

### EP-12: POST `/basic/chat/confirm-message`
**Controller**: `Basic\ChatController@confirmReadMessage` (`app/Http/Controllers/Basic/ChatController.php:198`)
**Uy quyen den**: `ConversationService@confirmReadMessage`
**Muc do tin cay**: **Cao**

#### Request params
| Ten | Vi tri | Kieu | Bat buoc | Mo ta |
|-----|--------|------|---------|-------|
| `conversationIds` | body | array | Co | Mang conversation IDs can xac nhan |
| `searchKey` | body | string | Khong | Filter hien tai (de tinh lai count) |
| `searchTag` | body | string | Khong | Filter tags hien tai |
| `searchStatusOr` | body | string | Khong | Filter status hien tai |
| `searchStatusAnd` | body | string | Khong | Filter status AND |
| `lineId` | body | integer | Khong | Line user ID hien tai |
| `filterTypeFriend` | body | string | Khong | Filter type hien tai |

#### Logic chinh
- Goi `ConversationService@confirmReadMessage` de danh dau da doc
- Cap nhat `bots.count_user_unconfirm`

---

### EP-13: POST `/basic/update-status-confirm`
**Controller**: `ChatController@updateStatusConfirm` (`app/Http/Controllers/ChatController.php:2652`)
**Muc do tin cay**: **Cao**

#### Request params
| Ten | Vi tri | Kieu | Bat buoc | Mo ta |
|-----|--------|------|---------|-------|
| `conversationIds` | body | array | Co | Mang conversation IDs |
| `status` | body | mixed | Co | Status moi: `0` (chua xac nhan), `1` (da xac nhan), hoac ID cua `status_chat` |
| `type` | body | string | Khong | Loai chat: `1:1` hoac `group` |
| `botIdCurrent` | body | integer | Khong | Bot ID |

#### Response thanh cong (200)
```json
{
  "success": true,
  "detail": {
    "is_has_msg": 1,
    "special_status": 5,
    "name_status": "Dang xu ly",
    "color": "#ff0000",
    "id_status": 5,
    "total_confirm": 0
  },
  "countUserUnConfirm": 3
}
```

#### Logic chinh
- Voi status = 1 (xac nhan): xoa `unconfirm_message`, set `confirm_count = 0`
- Voi status = 0 hoac custom: cap nhat `is_confirmed` tren message cuoi
- Luu conversation id_status
- Sync Elasticsearch
- Broadcast event `InfoEvent` de cap nhat badge real-time

---

### EP-14: POST `/ajax/save-hide-friend`
**Controller**: `ChatController@ajaxSaveHideFriend` (`app/Http/Controllers/ChatController.php:860`)
**Muc do tin cay**: **Cao**

#### Request params
| Ten | Vi tri | Kieu | Bat buoc | Mo ta |
|-----|--------|------|---------|-------|
| `conversion_id` | body | integer | Co | Conversation ID can an |

#### Logic chinh
- Set `conversation.is_hide = 1`, `datetime_hide = now()`
- Neu co tin chua xac nhan → tu dong xac nhan (xoa `unconfirm_message`, set `confirm_count = 0`)
- Tao message loai `KIND_MESSAGE_HIDE_FRIEND` voi noi dung「非表示しました」
- Cap nhat badge, broadcast `InfoEvent`

---

### EP-16: POST `/ajax/remove-hide-friend`
**Controller**: `Basic\FriendlistController@removeHideFriend` (`app/Http/Controllers/Basic/FriendlistController.php:4276`)
**Muc do tin cay**: **Cao**

#### Request params
| Ten | Vi tri | Kieu | Bat buoc | Mo ta |
|-----|--------|------|---------|-------|
| `lineUserId` | body | string | Co | Line user ID (line_id cua conversation) |

#### Logic chinh
- Set `conversation.is_hide = 0`, `datetime_hide = null`
- Sync Elasticsearch

---

### EP-23: POST `/basic/chat/save-memo`
**Controller**: `Basic\ChatController@saveMemo` (`app/Http/Controllers/Basic/ChatController.php:753`)
**Muc do tin cay**: **Cao**

#### Request params
| Ten | Vi tri | Kieu | Bat buoc | Mo ta |
|-----|--------|------|---------|-------|
| `conversation_id` | body | integer | Co | Conversation ID |
| `type` | body | integer | Co | Loai memo |
| `id` | body | integer | Khong | Memo ID (neu cap nhat, null neu tao moi) |
| `title` | body | string | Co | Tieu de memo |
| `content` | body | string | Co | Noi dung memo |

#### Logic chinh
- Neu co `id`: UPDATE `memos` bang title/content
- Neu khong co `id`: INSERT vao `memos` voi `position = max + 1`
- Tao ban ghi `memo_histories` (ghi lai lich su chinh sua)
- Gioi han lich su: toi da 10 ban ghi history/memo (xoa cu nhat khi vuot)

---

### EP-24: DELETE `/basic/chat/delete-memo`
**Controller**: `Basic\ChatController@deleteMemo` (`app/Http/Controllers/Basic/ChatController.php:805`)
**Muc do tin cay**: **Cao**

#### Request params
| Ten | Vi tri | Kieu | Bat buoc | Mo ta |
|-----|--------|------|---------|-------|
| `id` | body | integer | Co | Memo ID can xoa |

#### Logic chinh
- Xoa memo va toan bo `memo_histories` lien quan

---

### EP-26: POST `/ajax/init-status-chat`
**Controller**: `ChatController@ajaxGetStatusChat` (`app/Http/Controllers/ChatController.php:612`)
**Muc do tin cay**: **Cao**

#### Response thanh cong (200)
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "bot_id": 5,
      "name_status": "Dang xu ly",
      "color": "#ff0000",
      "bg_status": "#ffeeee",
      "bg_choose": "#ff5555",
      "position": 1,
      "is_save": 1
    }
  ]
}
```

---

### EP-28: POST `/ajax/save-item-status`
**Controller**: `ChatController@ajaxSaveItemStatus` (`app/Http/Controllers/ChatController.php:654`)
**Muc do tin cay**: **Cao**

#### Request params
| Ten | Vi tri | Kieu | Bat buoc | Mo ta |
|-----|--------|------|---------|-------|
| `id` | body | integer | Khong | Status ID (null = tao moi) |
| `name_status` | body | string | Co | Ten trang thai |
| `color` | body | string | Co | Ma mau text |
| `bg_status` | body | string | Co | Ma mau background |
| `bg_choose` | body | string | Co | Ma mau khi duoc chon |

#### Validation rules (tu code)
- `name_status` bat buoc, toi da 10 ky tu
- `color` bat buoc

#### Logic chinh
- Neu co `id`: UPDATE status_chat
- Neu khong co `id`: INSERT moi voi `position = 1`, day cac status cu xuong (`position + 1`)

---

### EP-31: POST `/ajax/delete-item-status`
**Controller**: `ChatController@ajaxDeleteItemStatus` (`app/Http/Controllers/ChatController.php:789`)
**Muc do tin cay**: **Cao**

#### Request params
| Ten | Vi tri | Kieu | Bat buoc | Mo ta |
|-----|--------|------|---------|-------|
| `id` | body | integer | Co | Status ID can xoa |

#### Logic chinh
- Xoa `status_chat` ban ghi
- Cap nhat tat ca `conversation` dang dung status nay: set `id_status = null`
- Sync Elasticsearch cho moi conversation bi anh huong

---

### EP-33: GET `/ajax/initial/get-data-setting`
**Controller**: `ChatController@getDataSettingChat` (`app/Http/Controllers/ChatController.php:3930`)
**Muc do tin cay**: **Cao**

#### Response thanh cong (200)
```json
{
  "success": true,
  "data_setting": {
    "confirm_message_button": 0,
    "confirm_message_autoreply": 0,
    "confirm_message_stamp": 0,
    "setting_shortcut": 1,
    "is_shorten_url": 1,
    "confirm_message_user_send": 1,
    "confirm_message_user_block_bot": 0,
    "preview_after_send": 0
  }
}
```

#### Mapping voi UI (SCR-CHT-02)
| Field | Tab | Label JP | Mo ta |
|-------|-----|---------|-------|
| `confirm_message_button` | Tab 2 | 「【〇〇】メッセージ」 | Tu dong xac nhan tin text |
| `confirm_message_stamp` | Tab 2 | 「スタンプ」 | Tu dong xac nhan sticker |
| `confirm_message_autoreply` | Tab 2 | 「自動応答で設定しているキーワード」 | Tu dong xac nhan keyword auto-reply |
| `confirm_message_user_send` | Tab 2 | 「返信時の自動確認済み変更」 | Tu dong xac nhan khi tra loi |
| `confirm_message_user_block_bot` | Tab 2 | 「ブロックされた友だちの自動確認済み変更」 | Tu dong xac nhan khi bi block |
| `setting_shortcut` | Tab 3 | Phim tat gui | 0 = Shift+Enter gui, 1 = Enter gui |
| `is_shorten_url` | Tab 4 | URL rut gon | 0 = tat, 1 = bat |
| `preview_after_send` | Tab 5 | Xem truoc gui | 0 = tat, 1 = bat |

---

### EP-34: POST `/ajax/save-data-setting`
**Controller**: `ChatController@saveSettingChat` (`app/Http/Controllers/ChatController.php:3948`)
**Muc do tin cay**: **Cao**

#### Request params
Body chua cac field tuong ung voi `data_setting` o EP-33. Luu y: controller dung `$request->all()` de update truc tiep vao bang `bots` → co the nhan bat ky field nao cua bots.

---

### EP-36: POST `/ajax/init-sticker-chat`
**Controller**: `ChatController@ajaxInitStickerChat` (`app/Http/Controllers/ChatController.php:640`)
**Muc do tin cay**: **Cao**

#### Request params
| Ten | Vi tri | Kieu | Bat buoc | Mo ta |
|-----|--------|------|---------|-------|
| `package_id` | body | integer | Khong | Sticker package ID (mac dinh = package dau tien) |

#### Response thanh cong (200)
```json
{
  "success": true,
  "stickerPackage": [
    { "id": 1, "name": "Package 1" }
  ],
  "listSticker": [
    { "id": 1, "packageId": 1, "stickerId": "001" }
  ]
}
```

---

### EP-42: POST `/basic/save-schedule-send`
**Controller**: `Basic\ScheduleSendChatController@saveScheduleSendChat` (`app/Http/Controllers/Basic/ScheduleSendChatController.php:30`)
**Muc do tin cay**: **Cao**

#### Request params
| Ten | Vi tri | Kieu | Bat buoc | Mo ta |
|-----|--------|------|---------|-------|
| `sendId` | body | integer | Khong | Schedule ID (null = tao moi) |
| `conversationId` | body | integer | Co | Conversation ID |
| `time_send` | body | string | Co | Gio gui (HH:mm) |
| `date_send` | body | string | Co | Ngay gui (Y-m-d) |

#### Logic chinh
- Neu co `sendId`: UPDATE thoi gian gui, reset `status = 0`
- Neu khong co: INSERT moi vao `schedule_send_chat` voi user_id tu Auth
- `date_time_send` duoc tinh = timestamp cua `date_send + time_send` * 1000 (milliseconds)

---

### EP-47: POST `/basic/cancel-schedule-send-chat`
**Controller**: `Basic\ScheduleSendChatController@cancelScheduleSendChat` (`app/Http/Controllers/Basic/ScheduleSendChatController.php:375`)
**Muc do tin cay**: **Cao**

#### Request params
| Ten | Vi tri | Kieu | Bat buoc | Mo ta |
|-----|--------|------|---------|-------|
| `sendId` | body | integer | Co | Schedule ID |
| `conversationId` | body | integer | Co | Conversation ID |

#### Logic chinh
- Set `schedule_send_chat.status = 2` (cancelled)

---

### EP-18: POST `/basic/chat/send_action`
**Controller**: `ChatController@sendActionForUser` (`app/Http/Controllers/ChatController.php:5527`)
**Muc do tin cay**: **Cao**

#### Request params
| Ten | Vi tri | Kieu | Bat buoc | Mo ta |
|-----|--------|------|---------|-------|
| `lineId` | body | integer | Co | Line user ID |
| `action_id` | body | integer | Co | Action ID can thuc hien |

#### Logic chinh
- Goi `HelperService@sendAction` de thuc hien action (co the bao gom gui tin nhan, gan tag, thay doi step...)
- Tra ve conversation va status moi nhat sau action

---

## Ghi chu chung

### Xac thuc
- Tat ca endpoints yeu cau dang nhap qua session-based authentication (Laravel web middleware)
- Bot ID lay tu session qua helper `getBotId()`
- User ID lay tu `Auth::id()`
- **Muc do tin cay**: **Cao**

### Real-time (WebSocket)
- Sau cac thao tac quan trong (gui tin, thay doi status, an friend), he thong broadcast event:
  - `ChatEvent`: gui tin nhan moi den client qua WebSocket
  - `InfoEvent`: cap nhat badge so tin chua doc
  - `CommontEvent`: cac event chung khac
- **Muc do tin cay**: **Cao** — doc truc tiep tu code `event()` calls

### Gioi han gui tin
- Free plan (`plan_type = 2`): gioi han 1000 tin/thang (`free_send_count`)
- Khi gui thanh cong: `free_send_count += 1`, cap nhat `message_send_count` theo ngay
- **Muc do tin cay**: **Cao**

### URL rut gon
- Khi `bots.is_shorten_url = 1`: URL trong tin nhan text duoc tu dong chuyen thanh short URL
- Xu ly qua `ChatHelper@sendShortUrl` va `ChatHelper@sendShortUrlAutore`
- **Muc do tin cay**: **Cao**

### Bot Profiles (ten gui)
- Admin/Staff chon profile gui (ten + avatar) qua EP-37
- Profile duoc luu trong session: `profiles_selected_{botId}_{userId}`
- Khi gui tin nhan, profile_send duoc luu vao `messages_v2s.profile_send`
- **Muc do tin cay**: **Cao**
