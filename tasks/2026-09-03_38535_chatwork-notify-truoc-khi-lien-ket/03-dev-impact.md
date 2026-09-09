# 03 — Đánh giá ảnh hưởng từ Dev

> Nguồn: Redmine #38535 — journal `133060` ngày **2026-08-26** của **AI LME Fix bug** (hệ thống Auto-fixbug LME). Nội dung dưới đây **paste nguyên văn**, chỉ tách mục theo template.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (hệ thống Auto-fixbug LME) — assign sau fix cho user id 58 |
| Commit / Pull Request | `5fa27b7ca8` (repo `sns-line`) — *không có link Github/Gitlab trong Redmine*. Dashboard: https://dashboard.melonglobal.net/fixbug-lme/?id=38535 |
| Branch | `ai_fixbug_38535` (nhánh gốc `release_step_20260805`, 1 file, đã push) |
| Ngày submit đánh giá | `2026-08-26` |
| Auto-filled | `2026-09-03 by /new-task` |
| Verify của Dev | Mức **lint** — `php -l` no syntax errors; `git diff --stat` = 1 file, 32 insertions(+), 1 deletion(-) |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

> Nguyên văn §1 báo cáo AI:

Khi bot bật thông báo Chatwork nhưng CHƯA liên kết phòng chat, mọi sự kiện vẫn được ghi vào hàng chờ thông báo với cờ 'chưa gửi Chatwork'. Job gửi Chatwork chỉ quét những cấu hình đã có URL phòng chat, nên trước khi liên kết nó bỏ qua bot này và hàng chờ cứ dồn lại. Ngay khi lưu URL phòng chat (liên kết thành công), job thấy toàn bộ hàng chờ cũ (các bản ghi trong 24h) rồi bắn một loạt thông báo của sự kiện đã xảy ra trước đó; màn hình liên kết trước đây không đặt lại hàng chờ và mốc lịch gửi.

## 2. Cách fix

> Nguyên văn §2 báo cáo AI:

Trong màn liên kết Chatwork (lưu URL phòng chat), khi bot chuyển từ CHƯA liên kết sang ĐÃ liên kết thì đánh dấu 'đã gửi' cho toàn bộ thông báo còn tồn đọng của bot, đồng thời đặt lại mốc thời gian gửi Chatwork và ngưỡng đếm lỗi phát hành về thời điểm liên kết — nên job chỉ gửi các sự kiện phát sinh từ sau khi liên kết (áp dụng cho cả admin lẫn nhân viên vì cả hai đều liên kết qua cùng màn này). Đánh dấu theo bot_id đúng như cách job đọc/đánh dấu hàng chờ. Yokoten: 2 chỗ cùng họ chưa sửa (bật lại công tắc thông báo Chatwork và lệnh recover khôi phục URL phòng chat cho admin) — nằm ngoài phạm vi ticket.

> ⚠️ **Yokoten CHƯA sửa (Dev tự khai, ngoài phạm vi ticket)** — 2 luồng cùng họ vẫn có thể tái hiện bug:
> 1. Bật lại công tắc thông báo Chatwork (`saveNotifySettingReceive` / `saveNotifySettings`)
> 2. Lệnh recover khôi phục URL phòng chat cho admin (`RecoverNotifySettingCloneStaff`)

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

> Nguyên văn §3 báo cáo AI ("ĐÃ CHECK FUNCTION / DATA LIÊN QUAN"):

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `NotifySettingController::ajaxSaveUrlChatWork` — `app/Http/Controllers/Basic/NotifySettingController.php` | **Đã sửa** | Điểm lưu URL phòng chat = thời điểm liên kết |
| 2 | `NotifySettingController::skipChatworkNotifyBeforeLink` — cùng file | **Hàm MỚI** | Đánh dấu 'đã gửi' cho hàng chờ tồn đọng theo `bot_id` |
| 3 | `NotifySettingController::saveNotifySettingReceive` / `saveNotifySettings` — cùng file | Không sửa (tham chiếu) | Mẫu xử lý tồn đọng khi đổi công tắc |
| 4 | `insertMobileNotify` — `app/Helpers/functions.php` | Không sửa | Nơi sinh bản ghi thông báo, đặt cờ theo cấu hình từng người dùng |
| 5 | `HandlePushNotifyChatwork` — `linect-service` | Không sửa | Job gửi Chatwork, chỉ quét cấu hình đã có URL phòng chat |
| 6 | `HandlePushNotifyChatwork` — `app/Console/Commands` | Không sửa | Bản artisan cũ cùng logic |
| 7 | `RecoverNotifySettingCloneStaff` — `app/Console/Commands` | Không sửa | Lệnh khôi phục cấu hình admin/nhân viên (nằm trong yokoten chưa sửa) |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

> ⚠️ §4.1 của báo cáo AI **chỉ ghi "File thay đổi"**, không list function. Bảng F1–F6 dưới đây do `/new-task` map từ §3 (không phải Dev viết) — Leader cần xác nhận không sót.

**Nguyên văn §4.1 — File thay đổi:**
- `app/Http/Controllers/Basic/NotifySettingController.php`

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `ajaxSaveUrlChatWork` (endpoint lưu URL phòng chat) | `app/Http/Controllers/Basic/NotifySettingController.php` | Direct | Đã sửa — nguồn §3 · Studio `EP-11` |
| F2 | `skipChatworkNotifyBeforeLink` | `app/Http/Controllers/Basic/NotifySettingController.php` | Direct | **Hàm mới** — nguồn §3 |
| F3 | `saveNotifySettingReceive` / `saveNotifySettings` | cùng file | Indirect | Dùng chung thao tác đánh dấu tồn đọng — **yokoten chưa sửa** |
| F4 | `HandlePushNotifyChatwork` (job linect-service + bản artisan cũ) | `linect-service` / `app/Console/Commands` | Indirect | Consumer hàng chờ — đọc/đánh dấu theo `bot_id` |
| F5 | `insertMobileNotify` | `app/Helpers/functions.php` | Indirect | Producer hàng chờ |
| F6 | `RecoverNotifySettingCloneStaff` | `app/Console/Commands` | Indirect | **Yokoten chưa sửa** |

### 4.2. List data bị update khi fix bug

> Nguyên văn §4.2 báo cáo AI:

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `mobile_notify.status_chat_work` | UPDATE | Các bản ghi đang chờ gửi Chatwork của bot được đánh dấu **đã gửi** tại thời điểm liên kết (**không** đụng cột `status` của app và `status_pc` của PC) |
| D2 | `notify_setting.last_notify_chat_work_time` | UPDATE | Đặt lại về thời điểm liên kết, cho cấu hình của người vừa liên kết |
| D3 | `notify_setting.chat_work_total_msg_error` | UPDATE | Đặt lại (chụp ngưỡng đếm lỗi) về thời điểm liên kết, cho cấu hình của người vừa liên kết |

> §5 báo cáo AI — **RECOVER DATA**: ✔ Không cần recover data.

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

> Nguyên văn §4.3 báo cáo AI:

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Notification Settings (FA-006)** — liên kết Chatwork không còn gửi bù thông báo của sự kiện trước khi liên kết | F1, F2, D1, D2 | *(Dev không ghi mức)* |
| T2 | **Delivery Error List (FA-028)** — cảnh báo lỗi phát hành cũ không bị gửi lại ngay sau khi liên kết Chatwork | F1, D3 | *(Dev không ghi mức)* |

---

## §6 VERIFY của Dev (nguyên văn)

- **Mức**: lint
- **Lệnh**: `php -l app/Http/Controllers/Basic/NotifySettingController.php`: No syntax errors detected; `git diff --stat origin/release_step_20260805...ai_fixbug_38535`: 1 file, 32 insertions(+), 1 deletion(-)
- **Bằng chứng**: Không kết nối được MySQL dev (`host.docker.internal:3306` Connection refused) → **không dump được dữ liệu**; đối chiếu cấu trúc bảng qua `share/db/db-refined` (`notify_setting.notification_room_url` / `last_notify_chat_work_time` / `chat_work_total_msg_error`, `mobile_notify.status_chat_work` đều tồn tại); Đọc job gửi Chatwork (`linect-service HandlePushNotifyChatwork` + `NotifySettingRepository.selectChatworkNotifySetting`): chỉ chọn cấu hình có `notification_room_url IS NOT NULL` rồi đọc mọi `mobile_notify status_chat_work = 0` theo `bot_id` → xác nhận cơ chế dồn hàng chờ khi chưa liên kết

> ⚠️ **Dev CHƯA verify runtime** — chỉ lint + đọc code, không chạy được DB. Toàn bộ hành vi runtime phải do QA chứng minh.

## §TỰ REVIEW (AI) — nguyên văn

Fix đặt đúng tại thời điểm liên kết (lưu URL phòng chat) — chính là điều kiện làm job bắt đầu quét bot. Chỉ chạy khi chuyển từ chưa liên kết sang đã liên kết nên thao tác sửa lại URL của bot đang liên kết không bị mất thông báo đang chờ. Không đụng kênh app/PC.

**Rủi ro / lưu ý khi test (Dev tự nêu):**
- Đánh dấu hàng chờ theo `bot_id`: nếu bot có **nhiều người (admin + nhân viên) cùng liên kết Chatwork**, người liên kết sau sẽ **dọn luôn hàng chờ chưa gửi của người trước** (tối đa 1 chu kỳ lịch gửi). Đây đúng theo cách job đang hoạt động (job cũng đánh dấu đã gửi theo `bot_id` sau mỗi lần push) và là cách duy nhất chặn triệt để việc gửi bù, vì job đọc hàng chờ theo `bot_id`.
- Job phía `linect-service` vẫn đọc/đánh dấu hàng chờ theo `bot_id` (không theo `user_id`) — hạn chế sẵn có của job, ngoài phạm vi sửa web.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3) — ⚠️ §4.1 gốc chỉ có tên file, bảng F1–F6 do `/new-task` map từ §3
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] **Yokoten chưa sửa** (bật lại công tắc Chatwork · `RecoverNotifySettingCloneStaff`) — đã thống nhất với Dev/PO là ngoài phạm vi ticket này?
- [ ] **Hành vi dọn chéo giữa admin ↔ nhân viên cùng bot** — đã đưa PO xác nhận là chấp nhận được? (Dev nêu ở §TỰ REVIEW; Studio ghi thành `REQ-009`)
- [ ] **Độ trễ 1 chu kỳ tần suất** do đặt lại `last_notify_chat_work_time` — đã đưa PO xác nhận? (Studio ghi thành `REQ-013`)
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
