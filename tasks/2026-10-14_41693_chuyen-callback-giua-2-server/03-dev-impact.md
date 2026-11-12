# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Thanh Duy Nguyen |
| Commit / Pull Request | `17a1ff385dd79ddf22abec559ae3ab3c1b78da2f` (báo cáo journal 2026-10-05); Studio ghi nhận thêm commit `32d54fc7` ([config MAX_SENT_MESSAGE_ACTION_SERVICE_THREAD](#) — xem REQ-005/REQ-009) |
| Branch | `m_202610_action-service-send-queue_41693` |
| Ngày submit đánh giá | 2026-10-05 |
| Auto-filled | 2026-10-14 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- Ticket là Feature (không phải bug) — Dev ghi "Mục đích" thay cho "Nguyên nhân". Giữ nguyên văn. -->

Job `ActionService` (xử lý bảng `action_line_user`) đang dùng chung queue gửi tin `NORMAL` với callback/postback/scenario/broadcast. Khi job action chạy số lượng lớn (vd 友だちリスト アクション bulk), queue `NORMAL` bị chiếm dụng → tin nhắn callback (ưu tiên realtime) có thể bị dồn/trễ. Mục đích của task: tách luồng gửi tin của job `ActionService` ra queue riêng để job này có thể chuyển sang 1 trong các job chung mà không ảnh hưởng tin callback.

## 2. Cách fix

- `RequestSentQueue` thêm `actionServiceRequestQueue` (queue mới, độc lập với queue `NORMAL`).
- `ActionModel.doAction(ActionLineUser)` gắn cờ `SEND_BY_ACTION_SERVICE_QUEUE` khi tin xuất phát từ action trên bảng `action_line_user`; cờ này **kế thừa** cho action con (tag/friend info chạy lồng trong action cha) → cũng push vào queue riêng.
- `SentMessageService` thêm pool luồng riêng xử lý `ACTION_SERVICE` queue, số luồng load từ config `MAX_SENT_MESSAGE_ACTION_SERVICE_THREAD` (default = 20).
- Retry khi LINE trả 429: tin quay lại **đúng queue gốc** (tin ACTION_SERVICE → retry vào ACTION_SERVICE, tin NORMAL → retry vào NORMAL).
- Tracking: cảnh báo riêng khi tin trong queue ACTION_SERVICE chờ > 1 phút.
- (Theo Studio REQ-009 / commit `32d54fc7`): server không bật `ActionService` (`ENABLE_ACTION_SERVICE=0`) → không khởi động pool ACTION_SERVICE, không xử lý hàng đợi action; tin NORMAL không bị ảnh hưởng.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `ActionModel.doAction(ActionLineUser)` | Gắn cờ `SEND_BY_ACTION_SERVICE_QUEUE` | Chỉ caller duy nhất là `ActionService.doActions` — các caller khác của `ActionModel.doAction` (postback, scenario, `ActionScheduleBotTask`...) **không truyền cờ** → giữ hành vi cũ, vẫn push queue `NORMAL` |

<!-- Dev chỉ liệt kê 1 caller đã check (ActionService.doActions); các caller khác được Dev khẳng định KHÔNG bị ảnh hưởng vì không mang cờ — cần review-tc đối chiếu kỹ caller thật trong diff/Studio dev_impact (quy tắc generic-fix ≥ 3 trigger ở BƯỚC 2, vì ActionModel.doAction là hàm dùng chung). -->

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `ActionModel.doAction` | `ActionModel` | Direct | Gắn cờ `SEND_BY_ACTION_SERVICE_QUEUE` |
| F2 | `ActionModel.isSendByActionServiceQueue` | `ActionModel` | Direct | Hàm mới — check cờ |
| F3 | `ActionModel.buildSubActionMapOption` | `ActionModel` | Direct | Kế thừa cờ cho action con (tag/friend info lồng) |
| F4 | `RequestSentQueue.pushRequestToActionServiceQueue` | `RequestSentQueue` | Direct | Hàm mới — push vào queue riêng |
| F5 | `RequestSentQueue.getRequestFromActionServiceQueue` | `RequestSentQueue` | Direct | Hàm mới — pop khỏi queue riêng |
| F6 | `RequestSentQueue.checkInTimeRetryRequest` | `RequestSentQueue` | Indirect | Sửa để retry 429 quay lại đúng queue gốc |
| F7 | `SentMessageService.startService` | `SentMessageService` | Direct | Khởi động thêm pool luồng cho ACTION_SERVICE |
| F8 | `SentMessageService.startSendMessageThreads` | `SentMessageService` | Direct | Dùng số luồng từ config `MAX_SENT_MESSAGE_ACTION_SERVICE_THREAD` |
| F9 | `SentMessageService.startTrackingQueue` | `SentMessageService` | Direct | Cảnh báo riêng khi tin ACTION_SERVICE chờ > 1 phút |
| F10 | `AppMain.logAllMessageRequestSendTrappedInQueue` | `AppMain` | Indirect | Log số lượng tồn của queue ACTION_SERVICE khi shutdown job |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | Config `MAX_SENT_MESSAGE_ACTION_SERVICE_THREAD` (`config.properties`) | CREATE (config mới, tuỳ chọn) | Default = 20 khi thiếu khoá; hành vi khi giá trị **không hợp lệ** chưa chốt chính thức (theo Studio REQ-005 — "không được làm ngừng gửi tin im lặng", đang chờ Dev xác nhận) |
| D2 | Config `ENABLE_ACTION_SERVICE` | (Suy từ Studio REQ-009, không có trong journal gốc) | Server không bật → không khởi động pool, không xử lý `action_line_user`; **không có trong journal Dev gốc** — cần hỏi lại Dev xác nhận field/giá trị thật |

<!-- Dev gốc (journal) chỉ ghi "không đổi DB". D1/D2 lấy từ Studio dev_impact (requirements REQ-005, REQ-009, commit 32d54fc7) — đánh dấu rõ nguồn khác nhau để review-tc không lẫn với 4.1/4.2 do Dev tự kê. -->

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Action từ bảng `action_line_user` (job ActionService — vd 友だちリスト アクション, admin action) | F1-F5, F7-F9 | High |
| T2 | Action con gắn tag / friend info chạy lồng trong action trên | F3 | High |
| T3 | Gửi tin nhắn callback / postback / scenario / broadcast (phải giữ nguyên queue NORMAL) | F1, F6 | High |
| T4 | Retry khi LINE trả 429 (cả 2 queue) | F6 | Medium |
| T5 | Shutdown / giám sát job (log queue còn tồn, cảnh báo treo > 1 phút) | F9, F10 | Medium |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót) — ⚠️ Dev chỉ xác nhận 1 caller (`ActionService.doActions`), cần hỏi lại danh sách đủ caller khác của `ActionModel.doAction` (postback/scenario/`ActionScheduleBotTask`) đã test thật chưa hay chỉ suy luận từ code
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file) — ⚠️ D1/D2 lấy từ Studio, chưa được Dev xác nhận trực tiếp trên Redmine
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

<!-- ⚠️ INPUT CẦN LƯU Ý: journal Dev gốc không có mục "Nguyên nhân"/"Cách fix" tách biệt rõ (ticket Feature dùng "Mục đích"/"Cách thực hiện"); mục 4.1/4.2/4.3 phần D1/D2/F-list đã bổ sung tham chiếu Studio task_get_context (dev_impact requirements) để không thiếu — Leader cần verify lại với Dev phần bổ sung này trước khi coi là chính thức. -->
