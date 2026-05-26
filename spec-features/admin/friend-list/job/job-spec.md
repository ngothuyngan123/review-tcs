# FA-013 Danh sách bạn bè「友だちリスト」 — Job Spec

> **Feature ID:** FA-013
> **Portal:** Admin
> **Ngày tạo:** 2026-03-25
> **Nguồn dữ liệu:** Spring Boot codebase `src/job/linect-service/`

---

## 1. Tổng quan

Tính năng「友だちリスト」tương tác với **2 background jobs** trong Spring Boot:

| # | Job | Mục đích | Trigger từ Web App |
|---|-----|---------|-------------------|
| 1 | **ActionScheduleBotTask** | Thực hiện bulk action cho > 200 users | `sendActionFriend()` tạo record `action_schedules` |
| 2 | **SyncEsTask** | Đồng bộ dữ liệu bạn bè lên Elasticsearch | Mọi thay đổi quan trọng (update tên, delete, hide/unhide) ghi `sync_elasticsearch` |

**Kiểu giao tiếp:** Database Polling Model — Laravel INSERT records vào queue tables, Spring Boot poll và xử lý.

**Tin cậy:** Cao — đọc trực tiếp source code Java.

---

## 2. Queue Tables

### 2.1 `action_schedules` — Bulk Action Queue

**Entity JPA:** `sns.line.models.linedb.entities.ActionSchedules`
**File:** `src/job/linect-service/src/main/java/sns/line/models/linedb/entities/ActionSchedules.java`

**Cột chính:**

| Cột | Kiểu | Mô tả |
|-----|------|-------|
| `id` | long (PK, auto) | ID |
| `name` | String | Tên schedule. Friend list tạo: 「【自動生成】友だち一括アクション」 |
| `bot_id` | Long | FK đến `bots.id` |
| `action_id` | Long | FK đến `actions.id` — action cần thực hiện |
| `next_running_day` | LocalDateTime | Thời gian thực thi tiếp theo |
| `status` | Integer | Trạng thái (state machine) |
| `repeat_type` | String | Kiểu lặp lại: `day`, `week`, `month` |
| `end_date_type` | String | Kiểu kết thúc: `unlimited`, `day_limit`, `times` |
| `end_date` | LocalDate | Ngày kết thúc (khi `end_date_type = day_limit`) |
| `number_of_repetitions` | Integer | Số lần lặp tối đa (khi `end_date_type = times`) |
| `action_count` | Integer | Số lần đã thực hiện |
| `filter_ids` | String | CSV IDs của `filters_v2` records — điều kiện lọc users |
| `day_add` | Integer | Số ngày cộng thêm (repeat daily) |
| `number_week_to_repeat` | Integer | Số tuần giữa mỗi lần lặp |
| `day_of_week_repeat` | String | Ngày trong tuần cần chạy (0=CN, 1=T2...) |
| `number_month_to_repeat` | Integer | Số tháng giữa mỗi lần lặp |
| `date_repeat_after_number_of_month` | String | JSON config lặp theo tháng |
| `skip_date` | String | Ngày bỏ qua |

**State Machine:**

```
STATUS_WAIT_TO_SENT (0) ──poll──→ STATUS_SENDING (1) ──xử lý xong──→ STATUS_RUNNING (0) hoặc STATUS_END (2)
                                                                        ↑
                                                                  (tính next_running_day)
```

| Status | Giá trị | Ý nghĩa |
|--------|---------|---------|
| `STATUS_WAIT_TO_SENT` / `STATUS_RUNNING` | 0 | Chờ xử lý — Spring Boot poll trạng thái này |
| `STATUS_SENDING` | 1 | Đang xử lý |
| `STATUS_END` | 2 | Kết thúc (hết lần lặp, quá end_date, hoặc lỗi) |

**Điều kiện poll:** `status = 0 AND next_running_day <= NOW()`

**Đặc biệt cho Friend List:** Khi `name = '【自動生成】友だち一括アクション'`, sau khi xử lý xong, record được **DELETE** thay vì tính `next_running_day` (one-time execution).

**Tin cậy:** Cao — `ActionSchedules.java`, `ActionScheduleBotTask.java:159-162`

---

### 2.2 `sync_elasticsearch` — Elasticsearch Sync Queue

**Entity JPA:** `sns.line.models.historydb.entities.SyncElasticsearch`
**File:** `src/job/linect-service/src/main/java/sns/line/models/historydb/entities/SyncElasticsearch.java`
**Database:** `historydb` (khác DB chính `linedb`)

**Cột chính:**

| Cột | Kiểu | Mô tả |
|-----|------|-------|
| `id` | Long (PK, auto) | ID |
| `type` | Integer | Loại sync (xem bảng bên dưới) |
| `line_user_id` | Long | FK đến `line_user.id` |
| `bot_id` | Long | FK đến `bots.id` |
| `status` | Integer | Trạng thái sync |
| `data_sync` | String | JSON data cần sync lên ES |
| `time_sync_success` | String | Thời gian sync thành công |
| `message_error` | String | Thông báo lỗi (nếu có) |
| `created_at` | String | Thời gian tạo |

**Type values liên quan Friend List:**

| Type | Giá trị | Mô tả | Trigger từ Web |
|------|---------|-------|----------------|
| `TYPE_LINE_USER` | 1 | Cập nhật thông tin user (tên, avatar) | `mypage()` — khi tên LINE thay đổi |
| `TYPE_DELETE_LINE_USER` | 11 | Xoá user khỏi ES index | `deleteUserBlock()` — cascade delete |
| `TYPE_BOT_LINE_USER` | 0 | Cập nhật bot_line_user data | `unHiddenFriend()` — hide/unhide |
| `TYPE_CONVERSATION` | 2 | Cập nhật conversation | Thay đổi trạng thái conversation |
| `TYPE_TAG` | 3 | Cập nhật tag | Gán/gỡ tag |
| `TYPE_FRIEND_INFO` | 4 | Cập nhật friend info | Thay đổi custom fields |
| `TYPE_DELETE_BOT` | 12 | Xoá toàn bộ bot khỏi ES | Admin xoá bot |

**State Machine:**

```
STATUS_WAIT_SYNC (0) ──poll──→ STATUS_SYNCHRONIZING (1) ──sync──→ STATUS_SYNC_SUCCESS (2)
                                                          │
                                                          └──lỗi──→ STATUS_SYNC_ERROR (3)
```

| Status | Giá trị | Ý nghĩa |
|--------|---------|---------|
| `STATUS_WAIT_SYNC` | 0 | Chờ sync |
| `STATUS_SYNCHRONIZING` | 1 | Đang sync |
| `STATUS_SYNC_SUCCESS` | 2 | Sync thành công |
| `STATUS_SYNC_ERROR` | 3 | Sync lỗi |

**Điều kiện poll:** `status = 0 ORDER BY id ASC LIMIT 200`

**Tin cậy:** Cao — `SyncElasticsearch.java`, `SyncEsTask.java:53`

---

## 3. Task Managers

### 3.1 BotTaskManager — Quản lý ActionSchedule

**File:** `src/job/linect-service/src/main/java/sns/line/task/BotTaskManager.java`
**Feature Flag:** `ENABLE_EVENT` (config: `ENABLE_EVENT=0|1`, mặc định: `0` — tắt)
**Khởi tạo:** `AppMain.run()` → `eventTask.startTask(executorService)` khi `ConfigFile.ENABLE_EVENT = true`

**Polling Logic:**
1. Thread chính: `while(true)` loop quản lý danh sách active bots, dọn bots inactive, sleep `M_1_DAY` (1 ngày)
2. Thread scan action schedule: `while(true)` loop mỗi **5 giây**:
   - Query: `findAllByStatusAndNextRunningDayBefore(STATUS_WAIT_TO_SENT, NOW())`
   - Với mỗi `ActionSchedules` tìm thấy → lấy `Bot` tương ứng
   - Tạo hoặc lấy `ActionScheduleBotTask` cho bot đó (HashMap cache theo bot_id)
   - Gọi `job.startWork(this)` → nếu chưa đang chạy và có task → execute

**Thread Pool:** Dùng `AppMain.getInstance().getExecutorService()` — shared executor service.

**Tin cậy:** Cao — `BotTaskManager.java:110-142`

---

### 3.2 SyncEsTask — Đồng bộ Elasticsearch

**File:** `src/job/linect-service/src/main/java/sns/line/task/SyncEsTask.java`
**Feature Flag:** `ENABLE_SYNC_ES_TASK` (config: `ENABLE_SYNC_ES_TASK=0|1`, mặc định: `1` — bật)
**Khởi tạo:** `AppMain.run()` → `syncEsTask.startJobSyncEs()` khi `ConfigFile.ENABLE_SYNC_ES_TASK = true`

**Polling Logic:**
- **1 thread producer** (`startJobGetEvent`): `while(true)` loop
  - Kiểm tra queue size < `MAX_QUEUE` (10,000)
  - Query: `findTop200ByStatusOrderByIdAsc(STATUS_WAIT_SYNC)` — lấy tối đa 200 records
  - Update tất cả status → `STATUS_SYNCHRONIZING`
  - Push vào in-memory `RequestSyncElasticsearchQueue` (LinkedList)
  - Nếu không có data → sleep **200ms**; nếu queue đầy → sleep **1,000ms**
- **5 threads consumer** (`MAX_THREAD = 5`): `while(true)` loop
  - Poll từ `RequestSyncElasticsearchQueue`
  - Xử lý từng record: upsert/delete document trên ES
  - Nếu không có record → sleep **500ms**
  - Có cơ chế lock theo `kind` (bot_id + line_user_id) để tránh conflict

**Thread Pool:** `Executors.newFixedThreadPool(6)` — 1 producer + 5 consumers, riêng biệt khỏi shared executor.

**Tin cậy:** Cao — `SyncEsTask.java`

---

## 4. Processing Chain

### 4.1 ActionSchedule Processing (Bulk Action > 200 users)

```
BotTaskManager (poll 5s)
  └─→ ActionScheduleBotTask.startWork()
        └─→ ActionScheduleBotTask.run() [async thread]
              │
              ├─ 1. Query: action_schedules WHERE bot_id=? AND status=0 AND next_running_day <= NOW()
              ├─ 2. Kiểm tra bot hết hạn (expiredOver7Day) → nếu hết → status = END, skip
              ├─ 3. Update status → SENDING, tăng action_count
              ├─ 4. Lấy danh sách users từ FilterV2:
              │     LineUserModel.getListLineUserFromFilterV2(filter, "action_schedule", scheduleId, botId)
              │     → Query filters_v2 WHERE parent_id=? AND parent_type='action_schedule'
              │     → Build SQL dynamic với AND/OR conditions
              │     → Return List<LineUser>
              ├─ 5. Lấy ActionDetail từ action_id
              ├─ 6. Lưu history: ActionSchedulesHistory
              ├─ 7. parallelStream().forEach → với mỗi user:
              │     ├─ ActionModel.doActionWithRequestSent(botId, lineUser, actionId, ...)
              │     │   → Thực hiện action: gửi tin nhắn, gán tag, thay đổi rich menu, v.v.
              │     └─ Lưu ActionScheduleLineUser (log từng user đã xử lý)
              ├─ 8. Kiểm tra NotifySetting → gửi mobile notification nếu bật
              │     → ActionLaterService.addLowPriorityTask(...)
              │     → Nội dung: 「{name}が稼働しました（対象人数 {N}人）」
              └─ 9. calculatorNextSchedule():
                    ├─ Nếu name = '【自動生成】友だち一括アクション' → DELETE record (one-time)
                    ├─ Nếu end_date_type = 'times' và đã đủ lần → status = END
                    ├─ Nếu repeat_type = 'day' → tính next_running_day + dayAdd ngày
                    ├─ Nếu repeat_type = 'week' → tìm ngày tiếp theo trong day_of_week_repeat
                    ├─ Nếu repeat_type = 'month' → tính ngày tháng tiếp theo
                    └─ Update status = RUNNING (0), next_running_day = nextRunDate
```

**Tin cậy:** Cao — `ActionScheduleBotTask.java:51-143`, `ActionScheduleBotTask.java:158-332`

---

### 4.2 SyncElasticsearch Processing

```
SyncEsTask.startJobSyncEs()
  ├─ Producer Thread (startJobGetEvent):
  │    while(true):
  │      ├─ Query: sync_elasticsearch WHERE status=0 ORDER BY id LIMIT 200
  │      ├─ Update all → status = SYNCHRONIZING (1)
  │      └─ Push to RequestSyncElasticsearchQueue (in-memory LinkedList, max 10,000)
  │
  └─ Consumer Threads (x5):
       while(true):
         ├─ Poll from RequestSyncElasticsearchQueue
         ├─ tryLockKind() → lock theo key = "{bot_id}_{line_user_id}"
         │   (tránh 2 threads cùng sync 1 user)
         └─ doSyncEs():
              ├─ TYPE_DELETE_LINE_USER (11):
              │   → EsService.deleteDocuments("es_line_user", key)
              ├─ TYPE_DELETE_BOT (12):
              │   → Tìm tất cả LineUser của bot → delete từng document
              ├─ TYPE_LINE_USER (1):
              │   → EsService.upsertDocument() với data_sync JSON
              │   → Tìm tất cả documents cùng line_user_id → update view_name/name
              ├─ Các type khác (0, 2, 3, 4, 5, 6, 7):
              │   → EsService.upsertDocument() với data_sync JSON
              │   → convertData(): chuyển đổi friend_info fields theo type (select/input/point/calendar)
              └─ Update status:
                   ├─ Thành công → STATUS_SYNC_SUCCESS (2), ghi time_sync_success
                   └─ Lỗi → STATUS_SYNC_ERROR (3), ghi message_error
```

**Tin cậy:** Cao — `SyncEsTask.java:39-214`

---

## 5. Services & Helpers

### 5.1 ActionModel.doActionWithRequestSent()

**File:** `src/job/linect-service/src/main/java/sns/line/models/ActionModel.java`
**Gọi bởi:** `ActionScheduleBotTask` (bước 7)

**Logic:**
- Nhận `botId`, `lineUser`, `actionId`, availability check
- Delegate sang `doAction()` — method chính (~700 dòng)
- Xử lý nhiều loại action: gửi tin nhắn LINE, gán/gỡ tag, thay đổi rich menu, cập nhật friend info, trigger scenario, v.v.
- Kiểm tra `isAvailableToSend` trước khi gửi tin nhắn (giới hạn quota LINE API)
- Ghi log `StartActionInfo` với `TriggerStartActionConstants.TYPE_ACTION_SCHEDULE`

**Tin cậy:** Cao — `ActionModel.java:68-77, 84-101`

---

### 5.2 LineUserModel.getListLineUserFromFilterV2()

**File:** `src/job/linect-service/src/main/java/sns/line/models/LineUserModel.java`
**Gọi bởi:** `ActionScheduleBotTask` (bước 4)

**Logic:**
1. Query `filters_v2` theo `parent_id` (= action_schedule.id), `parent_type = 'action_schedule'`
2. Tách thành AND filters và OR filters (theo `operator`)
3. Build native SQL query dynamic:
   - Base: `SELECT line_user.* FROM line_user JOIN bot_line_user ...`
   - AND conditions: `WHERE` clauses kết hợp AND
   - OR conditions: `WHERE` clauses kết hợp OR
   - Filter types: tag, friend_name, day_add_friend, scenario, conversion, qr_code, friend_info, status_chat, affiliate, bot_new_friend, richmenu
4. Execute query → trả về `List<LineUser>`

**Tin cậy:** Cao — `LineUserModel.java:339-415`

---

### 5.3 EsService

**File:** `src/job/linect-service/src/main/java/sns/line/helper/EsService.java`
**Gọi bởi:** `SyncEsTask`

**Methods:**
| Method | Mô tả |
|--------|-------|
| `initClient()` | Khởi tạo Elasticsearch `RestHighLevelClient` |
| `upsertDocument(doc, id, data)` | Insert hoặc update document trên ES |
| `deleteDocuments(doc, id)` | Xoá document khỏi ES index |
| `searchDocuments(doc, query)` | Tìm kiếm documents theo query |
| `insertDocument(doc, id, value)` | Insert document mới |
| `updateDocument(doc, id, data)` | Update document |

**ES Document:** `EsLineUserObjectKey.DOCUMENT_NAME` — index chứa thông tin bạn bè, bao gồm: bot_id, line_user_id, name, view_name, tags, friend_info (custom fields), scenario, conversion, v.v.

**Tin cậy:** Cao — `EsService.java`

---

### 5.4 RequestSyncElasticsearchQueue

**File:** `src/job/linect-service/src/main/java/sns/line/helper/RequestSyncElasticsearchQueue.java`

**Mô tả:** In-memory queue (LinkedList synchronized) trung gian giữa producer và consumer threads của SyncEsTask.

| Property | Giá trị |
|----------|---------|
| Max size | 10,000 records |
| Type | `LinkedList<SyncElasticsearch>` |
| Thread-safe | Synchronized trên `requestQueue` object |

**Tin cậy:** Cao — `RequestSyncElasticsearchQueue.java`

---

### 5.5 ActionLaterService

**File:** `src/job/linect-service/src/main/java/sns/line/helper/ActionLaterService.java`
**Gọi bởi:** `ActionScheduleBotTask` (bước 8 — gửi notification)

**Mô tả:** Service xử lý task ưu tiên thấp/bình thường bằng thread pool riêng.

| Queue | Thread count | Dùng cho |
|-------|-------------|---------|
| Low priority | 5 (mặc định) | Gửi mobile notification, Firebase push |
| Normal priority | 25 (mặc định) | Các task khác |

**Tin cậy:** Cao — `ActionLaterService.java:20-50`

---

## 6. External API Calls

### 6.1 Elasticsearch API (qua RestHighLevelClient)

| Operation | Method | Dùng khi |
|-----------|--------|---------|
| Upsert document | `PUT /es_line_user/_doc/{id}` | Cập nhật thông tin user (tên, tag, friend info...) |
| Delete document | `DELETE /es_line_user/_doc/{id}` | Xoá user khỏi ES |
| Search documents | `POST /es_line_user/_search` | Tìm user theo line_user_id hoặc bot_id |

**Document ID format:** `{bot_id}_{line_user_id}` — tạo bởi `EsLineUserObjectKey.makeId()`

**Tin cậy:** Cao — `EsService.java`, `SyncEsTask.java:104-112`

### 6.2 LINE Messaging API (gián tiếp qua ActionModel)

Khi `ActionScheduleBotTask` xử lý bulk action gửi tin nhắn:
- `POST https://api.line.me/v2/bot/message/push` — gửi tin nhắn tới user
- Các LINE API khác tuỳ loại action (rich menu, v.v.)

**Tin cậy:** Trung bình — suy luận từ `ActionModel.doAction()`, chưa đọc toàn bộ.

### 6.3 Firebase Cloud Messaging (gián tiếp qua notification)

Khi gửi mobile notification sau bulk action:
- `PriorityTask.checkAddNotifyTask()` → Firebase push notification

**Tin cậy:** Trung bình — suy luận từ `ActionLaterService` và `FirebaseMessagingModel` import.

### 6.4 Chatwork API (error reporting)

- `NotifyUtils.sendReportChatwork()` — gửi báo cáo lỗi đến Chatwork room
- Tag user: `[To:6395420][To:7907973]`

**Tin cậy:** Cao — `ActionScheduleBotTask.java:132`, `SyncEsTask.java:126`

---

## 7. Data Flow Diagram

```mermaid
flowchart TD
    subgraph "Laravel Web App"
        A[Admin chọn Bulk Action<br>trên Friend List] --> B{Tổng users > 200?}
        B -->|Có| C[Tạo ActionSchedule record<br>name='【自動生成】友だち一括アクション'<br>next_running_day=NOW()+2s<br>status=0]
        B -->|Không| D[Xử lý trực tiếp<br>HelperService.sendAction]

        E[Admin thay đổi dữ liệu bạn bè<br>- Cập nhật tên<br>- Xoá user<br>- Ẩn/hiện user<br>- Gán/gỡ tag] --> F[Ghi sync_elasticsearch<br>status=0, type=tương ứng]
    end

    subgraph "MySQL Database"
        C --> G[(action_schedules<br>status=0)]
        F --> H[(sync_elasticsearch<br>status=0)]
        C --> I[(filters_v2<br>parent_type='action_schedule')]
    end

    subgraph "Spring Boot — BotTaskManager"
        J[Poll mỗi 5 giây<br>ENABLE_EVENT flag] --> G
        G -->|status=0 AND<br>next_running_day<=NOW| K[ActionScheduleBotTask]
        K --> L[Query FilterV2 → build SQL<br>→ lấy List LineUser]
        L --> M[parallelStream<br>ActionModel.doAction<br>cho từng user]
        M --> N[Lưu history:<br>action_schedule_line_user<br>action_schedules_history]
        N --> O{name = '【自動生成】<br>友だち一括アクション'?}
        O -->|Có| P[DELETE record<br>one-time execution]
        O -->|Không| Q[Tính next_running_day<br>status = RUNNING]
        M --> R[Gửi MobileNotify<br>nếu NotifySetting bật]
    end

    subgraph "Spring Boot — SyncEsTask"
        S[Producer thread<br>ENABLE_SYNC_ES_TASK flag] --> H
        H -->|Top 200, status=0| T[Update status=1<br>Push to in-memory queue]
        T --> U[Consumer threads x5<br>Lock theo bot_id+line_user_id]
        U --> V{Type?}
        V -->|DELETE_LINE_USER| W[ES: Delete document]
        V -->|LINE_USER| X[ES: Upsert + update<br>tất cả docs cùng line_user_id]
        V -->|Khác| Y[ES: Upsert document<br>với data_sync JSON]
        W --> Z[status = SUCCESS/ERROR]
        X --> Z
        Y --> Z
    end

    subgraph "External Services"
        M -.->|LINE API| AA[LINE Messaging API<br>Push message, Rich menu]
        R -.->|Firebase| AB[Firebase Cloud Messaging]
        U -.->|ES API| AC[Elasticsearch Cluster]
        K -.->|Lỗi| AD[Chatwork Notification]
        U -.->|Lỗi| AD
    end
```

---

## 8. Error Handling

### 8.1 ActionScheduleBotTask

| Tình huống | Xử lý |
|-----------|-------|
| Exception trong `run()` | Log error + `NotifyUtils.sendReportChatwork()` tag 2 users → set `statusJob = IDLE` |
| Bot hết hạn > 7 ngày | Set `status = STATUS_END`, skip action, log thông báo |
| Lỗi tính `calculatorNextSchedule` | Log error + `NotifyUtils.sendNotify()` → set `status = STATUS_END` |
| Job treo > 30 phút | `lockWork()` phát hiện → log error + `System.exit(0)` (restart process) |
| `action_id = null` hoặc 0 | Log, lưu history với count=0, vẫn tính next schedule |

**Timeout cơ chế:** `LIMIT_WORKING_TIME = 1,800,000ms` (30 phút). Nếu 1 task chạy quá lâu → process exit và restart.

**Tin cậy:** Cao — `ActionScheduleBotTask.java:129-141, 401-418`

---

### 8.2 SyncEsTask

| Tình huống | Xử lý |
|-----------|-------|
| Exception khi sync | Set `status = STATUS_SYNC_ERROR`, ghi `message_error` + `NotifyUtils.sendReportChatwork()` + sleep 1s |
| Exception khi poll | Log error + sleep 1s, tiếp tục loop |
| Queue đầy (>= 10,000) | Producer sleep 1s, chờ consumers xử lý |
| Lock timeout (> 5 phút) | Release lock, log error, cho phép thread khác xử lý |
| Prepare stop/reboot | Tất cả threads kiểm tra `isPrepareStop()` → return gracefully |

**Lock timeout:** `LOCK_TIME_OUT = 300,000ms` (5 phút) — từ `StoppableTask` base class.

**Tin cậy:** Cao — `SyncEsTask.java:121-129, 242-272`

---

## 9. Liên kết với Web App

### 9.1 Bulk Action → ActionSchedule

| Hành động trên Web | Controller Method | Queue Table | Điều kiện | Job xử lý |
|--------------------|-------------------|-------------|-----------|-----------|
| Bulk action「アクション選択」khi > 200 users | `sendActionFriend()` (:863-1286) | `action_schedules` | Tạo record mới, `next_running_day = NOW() + 2s` | `BotTaskManager` → `ActionScheduleBotTask` |

**Chi tiết tạo record:**
- `name`: 「【自動生成】友だち一括アクション」
- `end_date_type`: `'times'`, `number_of_repetitions`: 1 (chạy 1 lần)
- `filter_ids`: CSV IDs của `filters_v2` records (lưu filter conditions hiện tại)
- `action_id`: ID action được chọn

**Kết quả sau xử lý:**
- Mỗi user trong danh sách được thực hiện action (gửi tin, gán tag, v.v.)
- Record `action_schedules` bị DELETE (vì name = auto-generated)
- History lưu trong `action_schedules_history` và `action_schedule_line_user`
- Nếu `NotifySetting` bật → gửi mobile notification

---

### 9.2 Data Changes → SyncElasticsearch

| Hành động trên Web | Controller Method | Type | data_sync |
|--------------------|-------------------|------|-----------|
| Mở chi tiết bạn bè (tên LINE thay đổi) | `mypage()` (:1609-1730) | `TYPE_LINE_USER` (1) | `{name, view_name, ...}` |
| Xoá bạn bè | `deleteUserBlock()` (:3219-3617) | `TYPE_DELETE_LINE_USER` (11) | null |
| Ẩn/hiện bạn bè | `unHiddenFriend()` (:4228-4275) | `TYPE_BOT_LINE_USER` (0) | `{is_hide: 0/1}` |
| Gán tag (từ chi tiết hoặc bulk) | `saveTag()` (:1287-1351) | `TYPE_TAG` (3) | `{tag data}` |
| Cập nhật thông tin tuỳ chỉnh | Inline trong `mypage` AJAX | `TYPE_FRIEND_INFO` (4) | `{friend_info values}` |

**Kết quả sau xử lý:**
- Document trên Elasticsearch được cập nhật/xoá
- Hỗ trợ tìm kiếm nhanh bạn bè trên giao diện (ES-backed search)

---

## 10. Bảng tổng hợp Files

| File | Vai trò |
|------|---------|
| `task/BotTaskManager.java` | Task Manager — poll `action_schedules` mỗi 5s, quản lý `ActionScheduleBotTask` per bot |
| `task/ActionScheduleBotTask.java` | Xử lý action schedule: lấy users từ FilterV2, thực hiện action, tính next schedule |
| `task/SyncEsTask.java` | Task Manager + Processing — poll `sync_elasticsearch`, producer-consumer pattern, sync ES |
| `task/StoppableTask.java` | Base class — lock mechanism, thread counter, stop signal |
| `helper/RequestSyncElasticsearchQueue.java` | In-memory queue giữa producer và consumer của SyncEsTask |
| `helper/EsService.java` | Elasticsearch client — CRUD operations trên ES |
| `helper/ActionLaterService.java` | Priority queue service — xử lý mobile notification async |
| `models/ActionModel.java` | Thực hiện action cho user (gửi tin, gán tag, thay đổi rich menu...) |
| `models/LineUserModel.java` | Build SQL từ FilterV2 → lấy danh sách users phù hợp |
| `models/linedb/entities/ActionSchedules.java` | JPA Entity — bảng `action_schedules` |
| `models/linedb/entities/FilterV2.java` | JPA Entity — bảng `filters_v2`, filter conditions |
| `models/linedb/entities/ActionScheduleLineUser.java` | JPA Entity — log từng user đã xử lý |
| `models/linedb/entities/ActionSchedulesHistory.java` | JPA Entity — history mỗi lần chạy schedule |
| `models/historydb/entities/SyncElasticsearch.java` | JPA Entity — bảng `sync_elasticsearch` |
| `models/linedb/repository/ActionSchedulesRepository.java` | JPA Repository — query action_schedules |
| `models/historydb/repository/SyncElasticsearchRepository.java` | JPA Repository — query sync_elasticsearch |
| `ConfigFile.java` | Feature flags: `ENABLE_EVENT`, `ENABLE_SYNC_ES_TASK` |
| `AppMain.java` | Entry point — khởi tạo task managers theo feature flags |

---

## 11. Ghi chú bổ sung

### Feature Flag ENABLE_EVENT mặc định tắt
`ConfigFile.ENABLE_EVENT` có giá trị mặc định `false` (0). Điều này có nghĩa `BotTaskManager` (và do đó `ActionScheduleBotTask`) **chỉ chạy khi được cấu hình bật** trong `config.properties`. Tuy nhiên, Laravel vẫn tạo `action_schedules` records bình thường — records sẽ được xử lý khi flag được bật.

**Tin cậy:** Cao — `ConfigFile.java:86`

### Parallel Processing trong ActionScheduleBotTask
Bước 7 sử dụng `lineUsers.parallelStream().forEach()` — xử lý song song tất cả users trong 1 batch. Điều này có thể gây tải cao trên LINE API nếu danh sách users lớn.

**Tin cậy:** Cao — `ActionScheduleBotTask.java:86`

### SyncEsTask dùng database riêng
Bảng `sync_elasticsearch` nằm trong `historydb` (không phải `linedb` chính). Entity thuộc package `models.historydb.entities`.

**Tin cậy:** Cao — package path `models.historydb.entities.SyncElasticsearch`
