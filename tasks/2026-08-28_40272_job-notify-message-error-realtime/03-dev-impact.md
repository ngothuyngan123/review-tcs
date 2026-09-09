# 03 — Đánh giá ảnh hưởng từ Dev

> **Nguồn**: Redmine #40272 — **journal #133203** (Văn Dũng Đinh, 2026-08-27T06:51:56Z).
> Dev đánh số mục hơi khác template: **`1. Mục đích`** (≙ mục 1 Nguyên nhân) · **`2. Cách thực hiện`** (≙ mục 2 Cách fix) · `3.` · `4.1/4.2/4.3` · `5. Commit / Branch`.
> Text trong các bảng bên dưới **giữ nguyên văn**, chỉ gắn tag `F* / D* / T*`. Bản gốc chưa cắt ghép ở cuối file.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Văn Dũng Đinh` |
| Commit / Pull Request | App + PC: `06cd8fb6`, `ad10a531` · Chatwork: `be829f69` — merge `m_202608_notify-pc-msg-error_39543_improve` → `release-t08-2026` |
| Branch | `m_202608_notify-pc-msg-error_39543_improve` |
| Ngày submit đánh giá | `2026-08-27` (journal #133203) |
| Auto-filled | `2026-08-28 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

> Dev ghi dưới tiêu đề **"1. Mục đích"** (nguyên văn):

- Nhánh realtime (notification_schedule / schedule_pc / schedule_chat_work = 0) đang count message_error của từng notify_setting mỗi vòng 60s ở cả 3 job -> query nặng, và việc bắn notify phụ thuộc counter app_total_msg_error / pc_total_msg_error / chat_work_total_msg_error nên dễ lệch (user confirm lỗi cũ xong, có lỗi mới vẫn không bắn) hoặc bắn lặp.
- Đổi sang xác định bot vừa phát sinh lỗi bằng mốc message_error.id, chỉ bắn notify đúng bot đó.

## 2. Cách fix

> Dev ghi dưới tiêu đề **"2. Cách thực hiện"** (nguyên văn):

- Thêm 3 cột mốc riêng cho 3 job vào job_config_daily (last_id_message_error_notify_app / _pc / _chat_work); mỗi vòng lấy MAX(message_error.id) rồi lấy DISTINCT bot_id trong khoảng (lastId, maxId] để lọc bot cần bắn, duyệt xong cả list mới lưu mốc mới.
- App + PC: tách createMsgErrorNotify (realtime) + buildMsgErrorNotify ra khỏi doPushNotify (bỏ tham số pushPendingNotify); MonitorCalendarBookingTask đổi save() cả entity sang updateBookingLastId() để không ghi đè các cột mốc mới.
- Chatwork: tách pushPendingNotify / createMsgErrorNotify / buildContentNotify / updateNextSchedule / pushNextScheduleDefault ra khỏi run(). Khác app + PC ở chỗ chatwork không có job realtime riêng nên nhánh realtime vẫn phải flush notify pending mỗi vòng, chỉ bỏ UPDATE notify_setting khi không có gì để gửi. Fix kèm: notify quá 24h chỉ bỏ qua chứ không markChatworkDone giữa vòng lặp nữa (hàm này update theo cả (bot_id, user_id) nên đánh dấu luôn notify mới chưa gửi, chatwork trả 429 là mất notify).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `doPushNotify` — `HandlePushMessageNotifyService:80`, `HandlePushNotifyPc:80` | Đổi signature (bỏ `pushPendingNotify`); đã update cả 2 caller | "method private, mỗi class đúng 1 caller nội bộ ở nhánh schedule — đã update cả 2 …, không có caller ngoài" |
| 2 | Các method tách mới ở `HandlePushNotifyChatwork` | Signature không đổi | "cũng private, class chỉ được new 1 chỗ tại AppMain.startHandlePushNotifyChatwork (AppMain:853), signature không đổi" |
| 3 | `MonitorCalendarBookingTask.monitorSalonCalendar` | Chuyển `save()` full-column → UPDATE theo cột (`updateBookingLastId()`) | "job_config_daily (1 bản ghi id = 1) dùng chung 4 job: đã rà toàn bộ 4 callsite … nên 3 cột mốc không ghi đè lẫn nhau" |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `startJobNotify` / `doPushNotify` / `createMsgErrorNotify` / `buildMsgErrorNotify` | `HandlePushMessageNotifyService` / `HandlePushNotifyPc` | Direct | Nguyên văn Dev: "HandlePushMessageNotifyService / HandlePushNotifyPc: startJobNotify / doPushNotify / createMsgErrorNotify / buildMsgErrorNotify" |
| F2 | `run` / `pushPendingNotify` / `createMsgErrorNotify` / `buildContentNotify` / `updateNextSchedule` / `pushNextScheduleDefault` | `HandlePushNotifyChatwork` | Direct | |
| F3 | `startJobNotify` / `doPushNotify` / `createMsgErrorNotify` / `buildMsgErrorNotify` | `HandlePushNotifyPc` | Direct | Dev liệt kê **trùng** với nửa PC của F1 — giữ nguyên như Dev ghi |
| F4 | `updateLastIdMessageErrorNotifyApp` / `updateLastIdMessageErrorNotifyPc` / `updateLastIdMessageErrorNotifyChatwork` / `updateBookingLastId` | `JobConfigDailyRepository` | Direct | |
| F5 | `findMaxId` / `findDistinctBotIdByIdBetween` + entity `JobConfigDaily` (3 field mới) | `MessageErrorRepository` / `JobConfigDaily` | Direct | |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `job_config_daily.last_id_message_error_notify_app` · `.last_id_message_error_notify_pc` · `.last_id_message_error_notify_chat_work` | MIGRATE | "cần ALTER TABLE thêm 3 cột … (bigint, nullable)" — SQL nguyên văn ở dưới |
| D2 | 3 cột mốc trên (ghi lại sau mỗi vòng job) | UPDATE | "duyệt xong cả list mới lưu mốc mới" (mục 2) |
| D3 | `job_config_daily` (bản ghi `id = 1`, dùng chung 4 job) — ghi qua `updateBookingLastId()` thay cho `save()` full-column | UPDATE | "3 cột mốc không ghi đè lẫn nhau" (mục 3) |
| D4 | `notify_setting` — nhánh realtime Chatwork "chỉ bỏ UPDATE notify_setting khi không có gì để gửi" | UPDATE | Từ mục 2 (Chatwork) |
| D5 | Notify quá 24h ở Chatwork: **không** còn gọi `markChatworkDone` giữa vòng lặp | UPDATE (đã bỏ) | "hàm này update theo cả (bot_id, user_id) nên đánh dấu luôn notify mới chưa gửi, chatwork trả 429 là mất notify" |

**SQL migration (nguyên văn Dev):**

```sql
ALTER TABLE `job_config_daily`
  ADD COLUMN `last_id_message_error_notify_app`       BIGINT NULL DEFAULT NULL AFTER `lesson_booking_last_id`,
  ADD COLUMN `last_id_message_error_notify_pc`        BIGINT NULL DEFAULT NULL AFTER `last_id_message_error_notify_app`,
  ADD COLUMN `last_id_message_error_notify_chat_work` BIGINT NULL DEFAULT NULL AFTER `last_id_message_error_notify_pc`;
```

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

> ⚠️ Dev **KHÔNG ghi** mức High/Medium/Low cho mục 4.3 → cột "Nguy cơ regression" để Leader đánh giá, **không tự suy diễn**.

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Notify 配信エラー realtime **app** (`notification_schedule = 0`): "tạo message_error mới cho 1 bot, check chỉ bot đó nhận push 1 lần (mobile_notify.status = 100), bot khác không bị bắn" | F1, F4, F5, D1, D2 | `<Dev không ghi — Leader đánh giá>` |
| T2 | Notify 配信エラー realtime **PC** (`schedule_pc = 0`): "tương tự, check push web về đúng user (user_id null -> admin bot) và status_pc = 1, không bắn lặp mỗi phút" | F1, F3, F4, F5, D1, D2 | `<Dev không ghi — Leader đánh giá>` |
| T3 | Notify 配信エラー realtime **Chatwork** (`schedule_chat_work = 0`): "tương tự, check chỉ room của bot đó nhận 1 message, bot khác không bị bắn và không lặp lại mỗi phút" | F2, F4, F5, D1, D2, D4 | `<Dev không ghi — Leader đánh giá>` |
| T4 | Notify 配信エラー **theo schedule** cả 3 kênh (15p/30p/1/3/6/12/24h): "chạy lại 1 vòng, check nội dung notify + badge + push các bản ghi pending + counter *_total_msg_error giữ nguyên như trước" | F1, F2, F3 | `<Dev không ghi — Leader đánh giá>` |
| T5 | Notify **chatwork các loại khác** (add friend, QR code, chat 1-1, メッセージ配信, action schedule, ASP, conversion): "check nội dung message gửi lên room không đổi, notify tạo quá 24h vẫn bị bỏ qua; setting chưa liên kết room / bot hết hạn thì bị đẩy lịch 15 phút" | F2, D5 | `<Dev không ghi — Leader đánh giá>` |
| T6 | **Deploy lần đầu (mốc = 0)**: "vòng chạy đầu của cả 3 job chỉ ghi nhận MAX(id), check KHÔNG bắn notify cho toàn bộ message_error cũ" | D1, D2, F5 | `<Dev không ghi — Leader đánh giá>` |

---

## 5. Commit / Branch (mục Dev tự thêm ngoài template)

| Trường | Giá trị (nguyên văn) |
|---|---|
| 5.1 Commit hoặc pull request | `m_202608_notify-pc-msg-error_39543_improve -> release-t08-2026` · App + PC: 2 commit `06cd8fb6`, `ad10a531` · Chatwork: 1 commit `be829f69` |
| 5.2 Branch hiện tại của task | `m_202608_notify-pc-msg-error_39543_improve` |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

### Điểm cần hỏi lại Dev / Leader chốt (phát hiện khi auto-fill)

- [ ] **4.3 thiếu mức nguy cơ regression** — Dev không ghi High/Medium/Low cho T1–T6.
- [ ] **F3 trùng F1** (nửa PC) — xác nhận Dev không định ghi một class khác bị sót.
- [ ] **Rollout của D1 (ALTER TABLE)** — thứ tự migration vs deploy code không ghi ở mục 4.2, trong khi T6 phụ thuộc giá trị mốc ở vòng chạy đầu.

---

## Nguyên văn journal #133203 (chưa cắt ghép — để trace ngược)

```
1. Mục đích
	- Nhánh realtime (notification_schedule / schedule_pc / schedule_chat_work = 0) đang count message_error của từng notify_setting mỗi vòng 60s ở cả 3 job -> query nặng, và việc bắn notify phụ thuộc counter app_total_msg_error / pc_total_msg_error / chat_work_total_msg_error nên dễ lệch (user confirm lỗi cũ xong, có lỗi mới vẫn không bắn) hoặc bắn lặp.
	- Đổi sang xác định bot vừa phát sinh lỗi bằng mốc message_error.id, chỉ bắn notify đúng bot đó.

2. Cách thực hiện
	- Thêm 3 cột mốc riêng cho 3 job vào job_config_daily (last_id_message_error_notify_app / _pc / _chat_work); mỗi vòng lấy MAX(message_error.id) rồi lấy DISTINCT bot_id trong khoảng (lastId, maxId] để lọc bot cần bắn, duyệt xong cả list mới lưu mốc mới.
	- App + PC: tách createMsgErrorNotify (realtime) + buildMsgErrorNotify ra khỏi doPushNotify (bỏ tham số pushPendingNotify); MonitorCalendarBookingTask đổi save() cả entity sang updateBookingLastId() để không ghi đè các cột mốc mới.
	- Chatwork: tách pushPendingNotify / createMsgErrorNotify / buildContentNotify / updateNextSchedule / pushNextScheduleDefault ra khỏi run(). Khác app + PC ở chỗ chatwork không có job realtime riêng nên nhánh realtime vẫn phải flush notify pending mỗi vòng, chỉ bỏ UPDATE notify_setting khi không có gì để gửi. Fix kèm: notify quá 24h chỉ bỏ qua chứ không markChatworkDone giữa vòng lặp nữa (hàm này update theo cả (bot_id, user_id) nên đánh dấu luôn notify mới chưa gửi, chatwork trả 429 là mất notify).

3. Đã check và sửa các function sử dụng đến function/data vừa sửa
	- doPushNotify đổi signature (bỏ pushPendingNotify): method private, mỗi class đúng 1 caller nội bộ ở nhánh schedule — đã update cả 2 (HandlePushMessageNotifyService:80, HandlePushNotifyPc:80), không có caller ngoài. Các method tách mới ở HandlePushNotifyChatwork cũng private, class chỉ được new 1 chỗ tại AppMain.startHandlePushNotifyChatwork (AppMain:853), signature không đổi.
	- job_config_daily (1 bản ghi id = 1) dùng chung 4 job: đã rà toàn bộ 4 callsite, chuyển MonitorCalendarBookingTask.monitorSalonCalendar sang UPDATE theo cột thay vì save() full-column nên 3 cột mốc không ghi đè lẫn nhau.

4. Đánh giá ảnh hưởng
	4.1 List function
		- HandlePushMessageNotifyService / HandlePushNotifyPc: startJobNotify / doPushNotify / createMsgErrorNotify / buildMsgErrorNotify
		- HandlePushNotifyChatwork: run / pushPendingNotify / createMsgErrorNotify / buildContentNotify / updateNextSchedule / pushNextScheduleDefault
        - HandlePushNotifyPc.startJobNotify / doPushNotify / createMsgErrorNotify / buildMsgErrorNotify
		- JobConfigDailyRepository.updateLastIdMessageErrorNotifyApp / updateLastIdMessageErrorNotifyPc / updateLastIdMessageErrorNotifyChatwork / updateBookingLastId
		- MessageErrorRepository.findMaxId / findDistinctBotIdByIdBetween + entity JobConfigDaily (3 field mới)
	4.2 List những data bị update khi fix bug
		- Bảng job_config_daily: cần ALTER TABLE thêm 3 cột last_id_message_error_notify_app, last_id_message_error_notify_pc, last_id_message_error_notify_chat_work (bigint, nullable).
		- ALTER TABLE `job_config_daily`
		  ADD COLUMN `last_id_message_error_notify_app`       BIGINT NULL DEFAULT NULL AFTER `lesson_booking_last_id`,
		  ADD COLUMN `last_id_message_error_notify_pc`        BIGINT NULL DEFAULT NULL AFTER `last_id_message_error_notify_app`,
		  ADD COLUMN `last_id_message_error_notify_chat_work` BIGINT NULL DEFAULT NULL AFTER `last_id_message_error_notify_pc`;.
	4.3 Dựa vào 2 mục trên list những tính năng sẽ ảnh hưởng
		- Notify 配信エラー realtime app (notification_schedule = 0): tạo message_error mới cho 1 bot, check chỉ bot đó nhận push 1 lần (mobile_notify.status = 100), bot khác không bị bắn.
		- Notify 配信エラー realtime PC (schedule_pc = 0): tương tự, check push web về đúng user (user_id null -> admin bot) và status_pc = 1, không bắn lặp mỗi phút.
		- Notify 配信エラー realtime Chatwork (schedule_chat_work = 0): tương tự, check chỉ room của bot đó nhận 1 message, bot khác không bị bắn và không lặp lại mỗi phút.
		- Notify 配信エラー theo schedule cả 3 kênh (15p/30p/1/3/6/12/24h): chạy lại 1 vòng, check nội dung notify + badge + push các bản ghi pending + counter *_total_msg_error giữ nguyên như trước.
		- Notify chatwork các loại khác (add friend, QR code, chat 1-1, メッセージ配信, action schedule, ASP, conversion): check nội dung message gửi lên room không đổi, notify tạo quá 24h vẫn bị bỏ qua; setting chưa liên kết room / bot hết hạn thì bị đẩy lịch 15 phút.
		- Deploy lần đầu (mốc = 0): vòng chạy đầu của cả 3 job chỉ ghi nhận MAX(id), check KHÔNG bắn notify cho toàn bộ message_error cũ.

5. Commit / Branch
	5.1 Commit hoặc pull request
		- m_202608_notify-pc-msg-error_39543_improve -> release-t08-2026
		- App + PC: 2 commit 06cd8fb6, ad10a531. Chatwork: 1 commit be829f69.
	5.2 Branch hiện tại của task
		- m_202608_notify-pc-msg-error_39543_improve
```
