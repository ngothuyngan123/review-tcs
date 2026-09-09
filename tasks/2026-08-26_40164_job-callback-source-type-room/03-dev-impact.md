# 03 — Đánh giá ảnh hưởng từ Dev

> Nguồn: Redmine #40164 — **journal #133002** của Thanh Duy Nguyen (2026-08-26T02:58:39Z). Paste nguyên văn, không diễn giải lại.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Thanh Duy Nguyen` |
| Commit / Pull Request | `2cd86fc6eccf3f5993cc7b6e9dfebdf7a420ba8e` |
| Branch | `m_202608_callback_room_40164` (base: `release-t07-2026`) |
| Ngày submit đánh giá | `2026-08-26` |
| Auto-filled | `2026-08-26 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- nguyên văn Redmine -->

- Job callback chỉ nhận source.type là user và group; LineCallbackSource không có field roomId nên webhook từ room (multi-person chat tạo trước LINE v10.17.0) bị Jackson drop id.

## 2. Cách fix

<!-- nguyên văn Redmine -->

- Thêm TYPE_ROOM + field roomId vào LineCallbackSource, thêm getGroupOrRoomId() (ưu tiên groupId rồi tới roomId) và isSourceRoom/isSourceGroupOrRoom ở LineCallback; mọi chỗ trong HandlePostbackTask lấy id nhóm đều đổi sang getGroupOrRoomId() kèm guard rỗng.
	- Room route chung luồng group nhưng phân nhánh API: member profile dùng /v2/bot/room/{roomId}/member/{userId}; room không có Group Summary nên lấy tên 5 member đầu (qua /v2/bot/room/{roomId}/members/ids) nối bằng ", " làm tên room, lấy không được thì để rỗng và không throw.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- nguyên văn Redmine -->

- checkAddGroup, updateGroupMember đổi signature (thêm param isRoom) — grep toàn repo chỉ có 3 callsite, đều trong HandlePostbackTask (doHandleJoinGroup, checkAddGroupFriend) và đã update hết.
	- LineCallback.getGroupId() sửa thành null-safe, các caller cũ giữ nguyên behavior với group; không có module nào ngoài HandlePostbackTask dùng LineCallback.

**Bảng hóa từ nguyên văn ở trên (không thêm nội dung mới):**

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `checkAddGroup`, `updateGroupMember` (HandlePostbackTask) | Đổi signature — thêm param `isRoom` | Phân nhánh endpoint room vs group |
| 2 | 3 callsite: `doHandleJoinGroup`, `checkAddGroupFriend` (đều trong `HandlePostbackTask`) | Đã update hết theo signature mới | Dev grep toàn repo chỉ có 3 callsite |
| 3 | `LineCallback.getGroupId()` | Sửa thành null-safe | Caller cũ giữ nguyên behavior với group |
| 4 | Module ngoài `HandlePostbackTask` dùng `LineCallback` | Không có | Dev khẳng định không có module nào khác dùng |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- nguyên văn Redmine -->

- LineCallbackSource.isRoom, LineCallbackSource.getGroupOrRoomId (mới)
            - LineCallback.isSourceRoom, LineCallback.isSourceGroupOrRoom, LineCallback.getRoomId, LineCallback.getGroupOrRoomId (mới), LineCallback.getGroupId (null-safe)
            - ILineService.getRoomMemberProfile, ILineService.getRoomMemberIds (mới)
            - HandlePostbackTask.updateRoomLineProfile, HandlePostbackTask.getRoomMemberName (mới)
            - HandlePostbackTask.doHandleJoinGroup, doHandleLeaveGroup, doHandleMessage, handleMessageGroup, checkAddGroupFriend, updateGroupMember, checkAddGroup (sửa)

**Bảng hóa (tag F) từ nguyên văn ở trên — không thêm nội dung mới:**

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `LineCallbackSource.isRoom` | LineCallbackSource | Direct | mới |
| F2 | `LineCallbackSource.getGroupOrRoomId` | LineCallbackSource | Direct | mới |
| F3 | `LineCallback.isSourceRoom` | LineCallback | Direct | mới |
| F4 | `LineCallback.isSourceGroupOrRoom` | LineCallback | Direct | mới |
| F5 | `LineCallback.getRoomId` | LineCallback | Direct | mới |
| F6 | `LineCallback.getGroupOrRoomId` | LineCallback | Direct | mới |
| F7 | `LineCallback.getGroupId` | LineCallback | Direct | sửa — null-safe |
| F8 | `ILineService.getRoomMemberProfile` | ILineService | Direct | mới |
| F9 | `ILineService.getRoomMemberIds` | ILineService | Direct | mới |
| F10 | `HandlePostbackTask.updateRoomLineProfile` | HandlePostbackTask | Direct | mới |
| F11 | `HandlePostbackTask.getRoomMemberName` | HandlePostbackTask | Direct | mới |
| F12 | `HandlePostbackTask.doHandleJoinGroup` | HandlePostbackTask | Direct | sửa |
| F13 | `HandlePostbackTask.doHandleLeaveGroup` | HandlePostbackTask | Direct | sửa |
| F14 | `HandlePostbackTask.doHandleMessage` | HandlePostbackTask | Direct | sửa |
| F15 | `HandlePostbackTask.handleMessageGroup` | HandlePostbackTask | Direct | sửa |
| F16 | `HandlePostbackTask.checkAddGroupFriend` | HandlePostbackTask | Direct | sửa |
| F17 | `HandlePostbackTask.updateGroupMember` | HandlePostbackTask | Direct | sửa — thêm param `isRoom` |
| F18 | `HandlePostbackTask.checkAddGroup` | HandlePostbackTask | Direct | sửa — thêm param `isRoom` |

### 4.2. List data bị update khi fix bug

<!-- nguyên văn Redmine -->

- Không có — không đổi schema, không migration, không sửa config. Room dùng chung line_user.type = 1 và conversation.conversation_kind = 1 của group, phân biệt bằng prefix line_id (R... = room, C... = group).

**Bảng hóa (tag D) từ nguyên văn ở trên — không thêm nội dung mới:**

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | *(không có schema change / migration / config change)* | — | Dev khẳng định: không đổi schema, không migration, không sửa config |
| D2 | `line_user.type` = 1, `conversation.conversation_kind` = 1 | *(dùng chung với group, không đổi)* | Room phân biệt với group bằng **prefix `line_id`**: `R...` = room, `C...` = group |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

<!-- nguyên văn Redmine -->

- Chat trong room: nhắn text / sticker / ảnh trong room, check message vào đúng hội thoại và callback_event = 2 (DONE), không còn status 10.
            - Join / Leave room: mời OA vào room thì tạo line_user (line_id bắt đầu R) + conversation kind 1; kick OA thì conversation is_blocked = 1.
            - Tên hội thoại room: bot verified/premium thì tên = 5 member đầu nối bằng ", "; bot thường LINE trả 403 thì tên rỗng và chỉ log, không được để row error.
            - Regression group chat: tên group vẫn lấy từ Group Summary, profile member vẫn gọi endpoint /group/, luồng cũ không đổi.
            - Regression chat 1-1 và push/reply: message user thường và gửi tin từ màn hình chat (push to = line_id) chạy như cũ.

**Bảng hóa (tag T) từ nguyên văn ở trên — không thêm nội dung mới:**

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Chat trong room (text / sticker / ảnh) — vào đúng hội thoại, `callback_event = 2` (DONE), không còn status 10 | F14, F15, D2 | `<Dev không ghi mức>` |
| T2 | Join / Leave room — mời OA vào room tạo `line_user` (`line_id` bắt đầu `R`) + `conversation` kind 1; kick OA → `conversation.is_blocked = 1` | F12, F13, F18, D2 | `<Dev không ghi mức>` |
| T3 | Tên hội thoại room — bot verified/premium: tên = 5 member đầu nối `", "`; bot thường LINE trả 403 → tên rỗng, chỉ log, không để row error | F8, F9, F10, F11 | `<Dev không ghi mức>` |
| T4 | **Regression** group chat — tên group vẫn lấy từ Group Summary, profile member vẫn gọi endpoint `/group/`, luồng cũ không đổi | F7, F17, F18 | `<Dev không ghi mức>` |
| T5 | **Regression** chat 1-1 và push/reply — message user thường + gửi tin từ màn hình chat (push `to` = `line_id`) chạy như cũ | F14, F7 | `<Dev không ghi mức>` |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

<!-- Điểm Leader nên hỏi lại Dev (từ chênh lệch giữa description Redmine và đánh giá ảnh hưởng — /new-task chỉ nêu, KHÔNG kết luận):
- Description yêu cầu xử lý `memberJoined` / `memberLeft` và `postback` trong room, nhưng mục 4.1/4.3 của Dev KHÔNG nhắc tới 2 nhánh này.
- Description yêu cầu mục 5 "UI / Admin (màn hình quản lý hội thoại)"; mục 4.3 của Dev không liệt kê màn Chat admin.
- Mục 4.3 không ghi mức High/Medium/Low cho từng tính năng.
-->
