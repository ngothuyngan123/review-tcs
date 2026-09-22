# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#40051 — Màn hình chat11` |
| Module / Màn hình | Chat 1:1 (1:1チャット, FA-001) — toàn bộ API/ajax của 2 controller `ChatController` + `Basic\ChatController`. Lan sang: Chat Settings, Tag Management, Friend Information (khối info bên phải), Rich Menu, Step Delivery (scenario) khi thao tác **từ màn chat** |

## Mô tả bug (bản dịch tiếng Việt)

Nguyên văn yêu cầu của ticket (tracker **Bug API**):

- Sửa lại http code cho đúng ý nghĩa với các api, ajax
- validate required đầu vào
- Mọi query đều PHẢI ràng buộc theo bot đang đăng nhập

Đây là ticket **rà soát / siết chất lượng API** cho màn chat11, không phải bug do khách hàng báo với 1 ca lỗi cụ thể. Hiện trạng trước fix (theo mục 1 của Dev):

- Các endpoint API/ajax của màn chat 1:1 trả HTTP code **sai ý nghĩa**: lỗi hệ thống (ngoại lệ trong khối `catch`), không tìm thấy bản ghi, và lỗi nghiệp vụ **đều trả 200** (nghĩa là thành công). Màn hình phải tự đoán qua cờ `success` trong thân phản hồi → hệ thống giám sát không thấy lỗi.
- Hầu hết endpoint **nhận dữ liệu thẳng từ request mà không kiểm tra bắt buộc**: thiếu tham số vẫn chạy truy vấn theo giá trị rỗng rồi báo thành công, hoặc gọi thuộc tính trên bản ghi không tồn tại rồi rơi vào `catch`.
- Nhiều query lấy `id` thẳng từ request mà **thiếu điều kiện bot** → lỗ IDOR: thao tác chéo sang dữ liệu của bot khác (danh sách lỗ (a)–(k) ở `03-dev-impact.md` mục 2).

## Steps to reproduce

<!-- Ticket KHÔNG có section "Tái hiện bug" — đây là ticket rà soát API, không có ca lỗi khách hàng cụ thể. -->

## Expected result

<!-- (trống — expected của từng nhóm fix xem 03-dev-impact.md mục 2) -->

## Actual result

<!-- (trống) -->

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #40051 không có attachment. -->

## Ghi chú thêm của Leader

- ⚠️ **Bug không tái hiện được trong Redmine** — ticket chỉ nêu 3 yêu cầu chất lượng API, không có Steps/Expected/Actual. Root cause + cách fix đã được Dev confirm qua 4 journal auto-fixbug (file 03). TCs nên tập trung verify **cách fix** (HTTP code đúng nghĩa · validate required · ràng buộc bot) + **regression** toàn màn chat11.
- **Phạm vi rất rộng**: 61 method ở 2 controller chat11 bị đụng → rủi ro regression cao ở mọi thao tác trong màn chat, kể cả các endpoint **dùng chung với màn khác** (`confirm` = `/basic/rec_message` được gọi từ `chats/common.js`, `mobile/common.js`, `mobile/events.js`, `chat_group.js`).
- **Điểm nóng regression đã từng gãy trong chính ticket này** (journal #136625) — phải test kỹ:
  1. `refreshMessage` với `page=0` — lần gọi ĐẦU TIÊN của màn chat luôn gửi `page=0` (`page: this.current_page++`, khởi tạo 0, reset 0 khi đổi bộ lọc/tìm kiếm). Rule `min:1` → 422 → màn chat **không bao giờ tải được lịch sử tin**, hỏng **im lặng** (khối `$.ajax` của `refresh()` không có nhánh error).
  2. **Hội thoại NHÓM**: `conversation.line_id` là **chuỗi** (`olioa_group_<id>`, hoặc groupId/roomId của LINE). Rule `integer` trên `line_user_id`/`lineId`/`line_id`/`to_user` → 422 → không mở được nhóm (alert tiếng Nhật ở `initFriendInfo` `/ajax/info_friend_display_chat11`) và **không gửi được tin vào nhóm** (`validateSendRequest` dùng chung cho sendMessage/sendMedia/sendTemplate/sendSticker).
- **Quyết định của human về phạm vi ràng buộc bot** (journal #136646 — chốt cuối): dùng `getBotIdInScope()` — bot thao tác chỉ cần **nằm trong danh sách bot user có quyền**, **KHÔNG** bắt buộc trùng bot đang mở. Bản siết chặt hơn (`resolveCurrentBotId`, commit 89a9c0411f) **đã bị revert**. → TC **không** được kỳ vọng 403 khi user thao tác sang bot B mà mình cũng có quyền; chỉ kỳ vọng 403 khi `botIdCurrent` là bot **không thuộc quyền** user đang đăng nhập.
- Không gửi `botIdCurrent` → mặc định rơi về bot trong session (nhánh cố ý giữ; bỏ sẽ 403 hàng loạt).
- 2 hàm PRIVATE `getFriends`/`getFriendsES` **không** trả 403 mà trả giá trị rỗng tự nhiên (`[]` và `false`) — là hàm trả dữ liệu cho `index()`, không phải endpoint.
- **Cố ý KHÔNG sửa** (không đẻ TC bắt lỗi ở các chỗ này): `LineUser::find/where('id',$lineId)` (bảng `line_user` không có cột `bot_id`) · `removeTagLineUserMyPage` (thuộc màn MyPage) · khối `SettingDisplayInfoFriendChat11` đang bị comment · `saveSettingDisplayInfo` bản v1 (code chết).
- **Mức verify của Dev chỉ là `lint`** (php -l + node --check) — chưa chạy test hành vi. Rủi ro lọt bug cao.
- Branch QA checkout: `ai_fixbug_40051` (gốc `release_step_20260805`, commit cuối **b18b55a092**; cây mã bằng đúng commit `1fa9b45bdc`).

## Journal / note từ Redmine (nguyên văn)

> 4 journal đều là báo cáo **AI AUTO-FIXBUG** (tác giả `AI LME Fix bug`, 2026-09-15), cộng dồn trên cùng 1 branch. Bản có hiệu lực cuối là **#136646** (revert về `getBotIdInScope`). Mục 1 / 3 / 4 giống nhau ở cả 4 journal và đã đưa vào `03-dev-impact.md`; dưới đây chép nguyên văn mục **2. CÁCH FIX** của từng vòng để trace tiến trình.

**Journal #136589 — AI LME Fix bug — 2026-09-15 (vòng 1, commit f2e371adbe):**

```
■ 2. CÁCH FIX
Bổ sung theo yêu cầu human: "Mọi query đều PHẢI ràng buộc theo bot đang đăng nhập" (rule ownership-check §4.1 trong .claude/docs/BE-coding-rules.md — chống IDOR). Rà toàn bộ 61 method mà ticket này đã đụng ở 2 controller chat11, sửa theo 2 tầng:

TẦNG 1 — nguồn xác định bot (quan trọng nhất, 17 chỗ). Các endpoint nhận botIdCurrent do CLIENT gửi rồi dùng thẳng làm phạm vi: `if (!empty($request->botIdCurrent)) $bot = $request->botIdCurrent; else $bot = getBotId();`. Chừng nào biến phạm vi còn do client điều khiển thì mọi `where('bot_id', $bot)` phía dưới đều vô nghĩa — đổi 1 con số là thao tác chéo sang bot của người khác. Đã thay hết bằng `getBotIdInScope($request->botIdCurrent)` (hàm CÓ SẴN trên release, đang dùng ở TemplateV2Controller, trả null khi bot không thuộc quyền user đang đăng nhập) + chặn lại. 15 endpoint public trả JSON thì trả 403 qua helper mới `responseBotForbidden()` (đặt cạnh `responseInvalid()` ở cả 2 controller, thông điệp tiếng Nhật). Riêng 2 hàm PRIVATE `getFriends`/`getFriendsES` là hàm trả DỮ LIỆU cho index() chứ không phải endpoint, nên trả về giá trị rỗng tự nhiên của chúng ([] và false — false là sentinel sẵn có của getFriendsES) kèm logInfo, KHÔNG trả JsonResponse (trả response ở đây sẽ bị nhét nguyên object vào khoá 'data' của payload).

TẦNG 2 — các câu query lấy id thẳng từ request mà thiếu điều kiện bot. Đã đối chiếu schema trong /workspace/share/db để chỉ thêm bot_id vào bảng THỰC SỰ có cột đó. Các lỗ nghiêm trọng đã vá: (a) addProfilesBots — `BotsProfiles::where('id',$idProfile)->update($settings)` mà $settings lại GÁN bot_id của mình ⇒ sửa được profile của bot khác và kéo luôn nó về bot mình; (b) deleteProfilesBots — đọc + DELETE chỉ theo id ⇒ xoá profile bot khác; (c) saveSelectedProfileBot — chọn được hồ sơ người gửi của bot khác; (d) memo (Basic): getMemosInfo đọc, saveMemo sửa, deleteMemo xoá, saveSortMemo đổi thứ tự — đều chỉ theo id/conversation_id từ request; (e) updateStatusConfirm / changeStatusSettingCons — `Conversation::whereIn('id',$conversationIds)->get()` là query CHÍNH dẫn cả vòng lặp ghi dữ liệu, không lọc bot; (f) getMessageSocket — `MessagesV2::where('id',$msgId)` đọc trọn nội dung tin nhắn của bot bất kỳ; (g) getBadge — lộ số tin chưa đọc + loại tin của bot khác; (h) ajaxSaveItemStatus — update đã lọc bot nhưng `StatusChat::find()` đọc lại thì không, vẫn trả bản ghi bot khác về client; (i) saveTagLine — `Tags::find()` theo tags_id/tags_delete từ request rồi cộng/trừ count_user_tag ⇒ sửa số liệu tag của bot khác; (j) saveSettingDisplayInfoV2 + saveSettingDisplayInfoItem — xoá/sửa SettingDisplayInfoFriendChat11 và FriendInformationSetting/FriendInformationValue theo id từ request; (k) CaptureTemplate (3 chỗ) và các lượt đọc Conversation theo id từ request (ajaxSaveHideFriend, confirm, changStatus, refreshMessage).

Xử lý null sau khi siết: chỗ nào thân hàm dùng kết quả mà KHÔNG kiểm null thì thêm lối thoát rõ ràng thay vì để rơi thành 500 khó hiểu — changStatus thêm 404 '会話が見つかりません。' (giống confirm đã có), saveTagLine `continue` khi tag không thuộc bot. Các chỗ còn lại đã sẵn `if($conver)` / `if($tagDelete)` nên null là đường an toàn.

CỐ Ý KHÔNG sửa: (1) `LineUser::find/where('id',$lineId)` — bảng line_user KHÔNG có cột bot_id (friend gắn với bot qua bảng nối bot_line_user), siết đúng phải join thêm, vượt phạm vi ticket nên chỉ nêu; (2) `removeTagLineUserMyPage` — thuộc màn MyPage, không nằm trong 61 method ticket này đụng; (3) khối SettingDisplayInfoFriendChat11 đang bị comment trong saveSettingDisplayInfoV2 (code chết); (4) `saveSettingDisplayInfo` (bản v1) — JS chỉ gọi V2/Item nên là code chết, không đụng theo lesson verify-usage-before-editing.
```

**Journal #136625 — AI LME Fix bug — 2026-09-15 (vòng 2, commit 1fa9b45bdc):**

```
■ 2. CÁCH FIX
Vá nốt 3 lỗi BẮT BUỘC mà AI review vòng 4 để lại (ticket đã push nên chỉ THÊM commit 1fa9b45bdc lên branch, không rebase/amend), kèm 1 regression nữa tự phát hiện khi rà.

(1) refreshMessage trả 422 làm màn chat KHÔNG BAO GIỜ tải được lịch sử tin nhắn. Rule đang là 'page' => 'nullable|integer|min:1', trong khi chat11 gửi `page: this.current_page++` với current_page khởi tạo 0 và reset về 0 khi đổi bộ lọc/tìm kiếm — hậu tố ++ nên lần gọi ĐẦU TIÊN luôn gửi page=0; 0 không phải null nên nullable không cứu, min:1 fail. Nặng thêm: khối $.ajax của refresh() không có nhánh error nên hỏng IM LẶNG, người dùng không thấy gì. Đã đổi thành min:0 (thân hàm vốn đã quy 0 về 1 bằng `$request->page ? ... : 1`).

(2) refreshMessage VẪN đọc được tin nhắn của bot khác — đây là chỗ vòng trước tôi sửa THIẾU. Câu `Conversation::where('id',$id_conver)->where('bot_id',$bot_id)` đã đúng, nhưng $conversation null KHÔNG làm hàm dừng (lối thoát sớm duy nhất là empty($lineUser)), còn phần lấy dữ liệu bên dưới vẫn bám vào biến $id_conver THÔ: MessagesV2 ...->where('messages_v2s.conversation_id',$id_conver) và 2 chỗ ->where('conversation_id',$id_conver), không có điều kiện bot nào. Kịch bản khai thác: đăng nhập bot A, gọi /basic/refresh_message với conversation = id hội thoại của bot B + line_user_id là id line_user bất kỳ còn tồn tại + botIdCurrent = bot A (hợp lệ nên qua getBotIdInScope) => trả về trọn lịch sử tin nhắn của bot B. Đã thêm guard: có gửi conversation mà tra không ra trong phạm vi bot thì DỪNG, trả đúng payload rỗng sẵn có (200) — sau guard này $id_conver đã được chứng minh thuộc bot nên mọi query thô bên dưới an toàn. Cố ý KHÔNG chặn khi $id_conver rỗng vì màn hình được phép gọi lúc chưa chọn hội thoại.

(3) Rule integer chặn toàn bộ hội thoại NHÓM. Với nhóm, conversation.line_id là CHUỖI ('olioa_group_<id>' — Admin/BotController.php:1464/1521/2490, hoặc groupId/roomId của LINE), và chat11 gửi chính giá trị đó làm line_user_id/lineId. Ép integer => 422: refreshMessage hỏng im lặng, còn initFriendInfo (/ajax/info_friend_display_chat11) có nhánh error gọi showChatAjaxError nên BẬT alert tiếng Nhật mỗi lần mở một nhóm. Trước ticket này các endpoint đó trả 200 kèm dữ liệu rỗng, nên đây là regression do rule mới. Đã nới 17 rule line_user_id/lineId/line_id/to_user từ integer sang string|max:255 ở cả 2 controller (giữ nguyên required/nullable).

(4) TỰ PHÁT HIỆN khi rà quét — nặng hơn cả 3 lỗi trên và reviewer chưa bắt: `validateSendRequest` (Basic\ChatController, dùng chung cho sendMessage/sendMedia/sendTemplate/sendSticker — 4 endpoint GỬI TIN THẬT của chat11) ép 'to_user' => 'required|integer', trong khi FE gửi `to_user: this.current_friend.line_id` (chat-v2.js:3375/3496/3583/4071) = chuỗi khi là nhóm ⇒ KHÔNG GỬI ĐƯỢC TIN vào bất kỳ hội thoại nhóm nào. Đã nằm trong nhóm 17 rule được nới ở (3). Giữ nguyên 'conversation' => 'required|integer' vì conversation.id là số thật.
```

**Journal #136636 — AI LME Fix bug — 2026-09-15 (vòng 3, commit 89a9c0411f — ĐÃ BỊ REVERT ở vòng 4):**

```
■ 2. CÁCH FIX
Siết ràng buộc bot theo đúng rule human: "phải đúng bot đang mở thì mới gửi được" (commit thêm 89a9c0411f lên branch đã push, không rebase/amend).

VẤN ĐỀ: bản trước dùng getBotIdInScope($request->botIdCurrent) — hàm dùng chung này chỉ đòi bot nằm trong DANH SÁCH bot mà user có quyền, nên user quản lý nhiều bot vẫn thao tác được sang bot B trong khi đang mở bot A. Như vậy là lỏng hơn rule.

ĐÃ KIỂM CHỨNG TRƯỚC KHI SIẾT (để chắc không chặn nhầm luồng hợp lệ): mọi nguồn của botIdCurrent trong chat11 đều do SERVER render ra từ chính session bot — resources/views/basic/chat/index.blade.php:107 (Session::get('current_bot_id')), :108 (Bots::find(getBotId())), resources/views/layout/basic/main.blade.php:38 ($current_bot_id = getBotId()); và public/js/chats/chat-v2.js KHÔNG hề gán lại current_bot_id/botCurrent, cũng không ghi vào input #botIdCurrent (chỉ .val() đọc). Kết luận: không có bộ chuyển bot phía client, luồng hợp lệ KHÔNG BAO GIỜ gửi bot khác bot đang mở ⇒ siết bằng nhau là an toàn.

CÁCH LÀM: thêm helper PRIVATE `resolveCurrentBotId(Request $request)` vào TỪNG controller (ChatController + Basic\ChatController) thay vì sửa getBotIdInScope dùng chung — giữ nguyên hành vi cho TemplateV2Controller/TemplateService đang dùng hàm đó, giới hạn phạm vi ảnh hưởng đúng màn chat11. Helper trả null khi (a) session chưa có bot, hoặc (b) botIdCurrent khác bot đang mở (có logInfo ghi lại để truy vết thao tác chéo bot). Đã thay toàn bộ 17 lời gọi (15 ở ChatController, 2 ở Basic\ChatController). 15 endpoint public vẫn trả 403 qua responseBotForbidden(); riêng 2 hàm private getFriends/getFriendsES vẫn trả giá trị rỗng tự nhiên ([] và false) vì là hàm trả DỮ LIỆU cho index(), không phải endpoint.
```

**Journal #136646 — AI LME Fix bug — 2026-09-15 (vòng 4 — BẢN CÓ HIỆU LỰC, commit b18b55a092):**

```
■ 2. CÁCH FIX
Quay lại dùng getBotIdInScope() theo quyết định của human (commit revert b18b55a092 trên branch đã push, không rewrite lịch sử).

Bối cảnh: bản 89a9c0411f trước đó siết chặt hơn — bắt botIdCurrent phải TRÙNG KHỚP bot đang mở trong session (helper riêng resolveCurrentBotId). Human chốt lại: dùng getBotIdInScope() là đủ. Đã revert nguyên vẹn, xác nhận cây mã trở về ĐÚNG trạng thái của commit 1fa9b45bdc (git diff 1fa9b45bdc HEAD rỗng).

Hành vi hiện tại của 17 điểm xác định bot trong chat11 (15 ở ChatController, 2 ở Basic\ChatController): bot thao tác chỉ cần NẰM TRONG danh sách bot mà user đang đăng nhập có quyền (getListBotId), không bắt buộc trùng bot đang mở; không gửi botIdCurrent thì mặc định về bot trong session. Vẫn chặn được lỗ IDOR gốc là 'gửi thẳng id bot của người khác' — endpoint public trả 403 qua responseBotForbidden(), 2 hàm private getFriends/getFriendsES trả rỗng ([] / false) vì là hàm trả dữ liệu cho index().

Lý do giữ nhánh 'không gửi thì lấy bot session' (đã kiểm chứng bằng code, không suy đoán): nhiều call site KHÔNG gửi botIdCurrent, gồm chính chat11 — updateStatusConfirm() ở public/js/chats/chat-v2.js:1887 chỉ gửi conversationIds/status/type — và các endpoint dùng chung với màn khác, ví dụ confirm (/basic/rec_message) gọi từ public/js/chats/common.js:65, public/js/mobile/common.js, public/js/mobile/events.js, public/js/chats/chat_group.js. Bỏ nhánh này sẽ làm 403 hàng loạt. Về bảo mật cũng không mất gì: không gửi thì rơi về bot của chính user, kẻ tấn công không lợi gì; lỗ hổng chỉ phát sinh khi GỬI id bot của người khác, và đúng nhánh đó đã bị chặn.
```
