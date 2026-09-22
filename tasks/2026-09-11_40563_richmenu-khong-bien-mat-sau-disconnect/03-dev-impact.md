# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Thanh Duy Nguyen` |
| Commit / Pull Request | `2b262555c39d1bb802a072b7659a7bbfea81bc9d` (fix gốc) · `a9b4f89c` (fix bổ sung sau review: retry-safe token + abort khi getBotInfo fail) |
| Branch | `m_202609_changebot_fix_old_accesstoken_40563` |
| Ngày submit đánh giá | `2026-09-11` (Journal #135941) |
| Auto-filled | `2026-09-11 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

- `ChangeBotJob` port từ PHP `BotController::changeNewBotStep1` truyền **nhầm token**: DELETE richmenu (`ChangeBotJob.java:500`) dùng access token channel **MỚI** trong khi `rich_menus.rich_menu_id` do channel **CŨ** cấp → LINE trả **404** (log production `#deleteRichMenu status=404`, 3/3 dòng), richmenu cũ không bị xóa nên friend của OA cũ vẫn thấy.
- Bản Java còn **thiếu 2 bước** có trong PHP: xóa LIFF app tạm trên Login channel mới và ngắt webhook của channel cũ.

## 2. Cách fix

- Tách `recreateRichmenusOnLine` thành **2 token** (DELETE dùng token cũ, create/upload/alias dùng token mới), bổ sung `disconnectOldChannelWebhook` + `deleteTempBotLiffApps`/`deleteOldBotLiffApps`, thêm log status + response body cho mọi call LINE/Google API.
- Token channel cũ lấy từ **snapshot bất biến** trong `schedule_change_bots` (`channel_id`/`channel_secret`/`channel_id_line_login`/`channel_secret_line_login`) thay vì `bots.channel_access_token` để đúng cả khi admin flip status `4 → 1` chạy lại; kèm **guard same-channel**, **fallback 2 token** khi xóa richmenu/LIFF, và `getBotInfo` trả `null` + **abort** thay vì ghi rỗng vào `bots`.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

**3 thay đổi API:**

| # | Function / File | Thay đổi | Lý do |
|---|---|---|---|
| 1 | `BotRepository.findTempBotIdForChangeBot` | Đổi tên + return type → `findTempBotForChangeBot` (`Long` → `BotChangeBotTempView`) | Cần thêm 2 cột `liff_app_id`, `liff_app_id_booking` để dọn LIFF app cũ |
| 2 | `private recreateRichmenusOnLine` (ChangeBotJob) | Thêm param `oldChannelAccessToken` | DELETE richmenu phải dùng token channel cũ |
| 3 | `private getBotInfo` (ChangeBotJob) | Đổi return từ `BotInfo` rỗng → `null` | Để job abort thay vì ghi rỗng vào `bots` |

**Kết quả grep toàn `src/main/java`:**

- Mỗi method đúng **1 caller** (`ChangeBotJob.java:113` / `263` / `223`) đã update; **0 reference** tên cũ `findTempBotIdForChangeBot`.
- 3 client `RichMenuApiClient` / `LiffApiClient` / `GoogleCalendarStopWatchClient` giữ nguyên signature và chỉ được `new` trong `ChangeBotJob` → **không ảnh hưởng feature khác**.

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `ChangeBotJob.step1Recreate` | `ChangeBotJob.java` | Direct | Bước dựng lại richmenu |
| F2 | `ChangeBotJob.recreateRichmenusOnLine`, `ChangeBotJob.deleteOldRichMenu` | `ChangeBotJob.java` | Direct | Tách 2 token (DELETE = token cũ, create/upload/alias = token mới) |
| F3 | Nhóm method **mới** dọn channel cũ: `getWebhookEndpoint`, `disconnectOldChannelWebhook`, `deleteTempBotLiffApps`, `deleteOldBotLiffApps`, `isSameChannelId` | `ChangeBotJob.java` | Direct (mới thêm) | Bù 2 bước PHP còn thiếu + guard same-channel |
| F4 | Nhóm sửa cách gọi API + log: `generateAccessToken`, `setWebhookEndpoint`, `getBotInfo` | `ChangeBotJob.java` | Direct | `getBotInfo` → trả `null` + abort |
| F5 | `BotRepository.findTempBotForChangeBot` | `BotRepository` | Direct | Đổi tên + return `BotChangeBotTempView` |
| F6 | File **mới** `BotChangeBotTempView.java` | `src/main/java/sns/line/models/linedb/repository/view/` | Direct (mới) | Projection thay cho `Long` |
| F7 | `ChangeBotConstants` (2 constant retry) | `ChangeBotConstants` | Direct | Tham số retry `getBotInfo` |
| F8 | `RichMenuApiClient` / `LiffApiClient` / `GoogleCalendarStopWatchClient` | các client LINE/Google | Indirect | Thêm `readBody` + log response body; **signature giữ nguyên** |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | **DB: KHÔNG có** | — | Không có migration/DDL/config/entity field nào đổi. Native `@Query` trong `BotRepository` chỉ **SELECT thêm 2 cột sẵn có** (`liff_app_id`, `liff_app_id_booking`) và trả projection thay vì `Long`; 2 constant mới chỉ là tham số retry. |
| D2 | **State trên LINE — richmenu channel cũ** | DELETE | ⚠️ **Không rollback được**. Từ giờ richmenu trên channel cũ bị **xóa THẬT** thay vì 404. |
| D3 | **State trên LINE — LIFF app** | DELETE | ⚠️ **Không rollback được**. 2 LIFF app của bot trên Login channel **cũ** + 2 app **tạm** trên Login channel **mới** bị xóa thật. |
| D4 | **State trên LINE — webhook endpoint channel cũ** | UPDATE | ⚠️ **Không rollback được**. Bị ghi đè về `/line/callback/add` — **chỉ khi** endpoint đang trỏ về hệ thống mình. |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Change bot + rich menu** — test chạy hết **6 step**, richmenu cũ mất khỏi OA cũ (friend OA cũ không còn thấy menu), richmenu tạo lại đủ trên OA mới, `rich_menu_id` trong DB + alias + tap area mở đúng LIFF form/booking | F1, F2, D2 | High |
| T2 | **LIFF app** — test change bot **2-3 lần liên tiếp**: Login channel cũ không còn app cũ, Login channel mới không leak app tạm, link form/booking vẫn mở bình thường | F3, F5, D3 | High |
| T3 | **Webhook OA cũ** — sau khi đổi xong: add friend / nhắn vào OA cũ **không** sinh friend-message mới, bot mới vẫn nhận webhook (task check connect không set `is_connected = 2`), KH tự set webhook sang bên thứ 3 thì **không bị đụng tới** | F3, F4, D4 | High |
| T4 | **Chạy lại job** (admin flip `schedule_change_bots.status` từ `4` về `1`) — richmenu/LIFF do lần chạy trước tạo trên channel mới **vẫn bị dọn**, webhook của chính bot vừa đổi **không bị ghi đè**, và khi `getBotInfo` lỗi thì job **abort giữ nguyên** `line_id`/`view_name`/`bot_image` chứ không ghi rỗng | F3, F4, F7 | High |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

---

## Ghi chú Leader (không phải nội dung Dev)

- ⚠️ **RULE-08 / môi trường**: mục 4.2 là **state thật trên LINE**, không rollback được (xóa richmenu, xóa LIFF app, ghi đè webhook). Test ở local/staging không kết luận được cho production — cần cân nhắc phạm vi ENV cho TC nhóm này.
- ⚠️ **Dữ liệu tồn đọng ngoài phạm vi fix**: bot đã đổi LOA **trước** khi có fix vẫn còn richmenu mồ côi trên OA cũ; fix **không tự dọn** → cần thống kê phạm vi và bàn giao vận hành dọn tay (Studio REQ-014).
- ⚠️ Mục 3 ghi "mỗi method đúng 1 caller" — đây là hàm `private` trong cùng class + 1 repository method, **phù hợp** với rule hàm dùng chung phải có danh sách caller.
