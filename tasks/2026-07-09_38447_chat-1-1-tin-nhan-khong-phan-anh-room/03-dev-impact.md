# 03 — Đánh giá ảnh hưởng từ Dev

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-url>` → Claude parse section "Đánh giá ảnh hưởng" trong Redmine, fill các mục bên dưới. Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — Dev paste nguyên văn đánh giá theo format 4 mục.
>
> **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Thanh Phương |
| Commit / Pull Request | `68b970d7a11a6e72b2c462dc2b805a2d174f542c` (fix gốc: doHandleMessage / doHandlePostbackEvent) · `c94c8e622afd862387204b14096b464e7e49ec2b` (横展開: doHandleVideoPlayComplete / doHandleFollowEvent) |
| Branch | release-t06-2026-step |
| Ngày submit đánh giá | 2026-07-07 |
| Auto-filled | `2026-07-09 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- Dev mô tả root cause. Càng cụ thể càng tốt: file nào, function nào, logic sai ở đâu. -->

- 1 webhook callback từ LINE có thể gộp nhiều event (`parseCallbackEventData` trả về mảng `LineCallback`). Handler duyệt từng event bằng vòng `for` nhưng vài nhánh dùng `return` giữa loop → thoát cả method sau event đầu, làm rớt các event còn lại → tin nhắn không lưu vào phòng chat. Payload không đổi nên bật 『Webhookの再送』 gửi lại vẫn rớt đúng chỗ cũ.
- Cùng pattern return-giữa-loop còn ở `doHandleVideoPlayComplete` (user not-friend) và `doHandleFollowEvent` (user bị bot block).

## 2. Cách fix

<!-- Dev mô tả cách fix. Nếu có snippet code thì càng tốt. -->

- Đổi `return` → `continue` ở các nhánh routing/skip trong vòng `for callbackEvents` (chỉ bỏ qua đúng event lỗi, không abort cả callback):
  - `68b970d7`: `doHandleMessage` (group + ignore source), `doHandlePostbackEvent` (ignore source).
  - `c94c8e62` (横展開): `doHandleVideoPlayComplete` (2 nhánh NOT_FRIEND), `doHandleFollowEvent` (BLOCKED_BY_BOT — continue vẫn chạy `finally releaseKind`).
- Giữ nguyên `return` cho case cố ý: `STATUS_MEDIA_NEW` (defer sang media job) và `return` trong method con per-callback.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Dev liệt kê các nơi đã được check & update khi fix bug (caller functions, data dependencies). -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | 4 method (`doHandleMessage`, `doHandlePostbackEvent`, `doHandleVideoPlayComplete`, `doHandleFollowEvent`) | `return` → `continue` ở nhánh skip | Đều `private`, mỗi cái chỉ 1 caller là switch dispatch trong `startHandleCallbackEvent`; signature không đổi → scope local, không ảnh hưởng caller |
| 2 | Method con per-callback (side-effect) | Không đổi code | Giờ chạy cho **mọi event** trong batch (nhiều lần hơn — đúng ý fix); status set trong loop bị `setStatus(DONE)` cuối method ghi đè cho event skip, nhưng status terminal/không query nên không mất retry |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Mọi function Dev đã sửa HOẶC có thể bị ảnh hưởng gián tiếp. -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `HandlePostbackTask.doHandleMessage` | HandlePostbackTask | Direct | `return` → `continue` (group + ignore source) |
| F2 | `HandlePostbackTask.doHandlePostbackEvent` | HandlePostbackTask | Direct | `return` → `continue` (ignore source) |
| F3 | `HandlePostbackTask.doHandleVideoPlayComplete` | HandlePostbackTask | Direct | 横展開: 2 nhánh NOT_FRIEND |
| F4 | `HandlePostbackTask.doHandleFollowEvent` | HandlePostbackTask | Direct | 横展開: BLOCKED_BY_BOT — continue vẫn chạy `finally releaseKind` |

### 4.2. List data bị update khi fix bug

<!-- Mọi bảng DB, field, cache, config, migration,... bị chạm tới. -->

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | MessagesV2s + UnconfirmMessage + Conversation/ES + push socket | CREATE / UPDATE | Không đổi schema/SQL/config, nhưng đổi hành vi ghi data runtime (mục đích fix): lưu THÊM cho các event trước đây bị rớt |
| D2 | `callback_event.status` của event bị skip (IGNORE_GROUP_MESSAGE / NOT_FRIEND / BLOCKED_BY_BOT) | UPDATE → DONE | Đều terminal, không query → chỉ ảnh hưởng thống kê |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

<!-- Dev suy ra từ 4.1 và 4.2: tính năng end-user nào có nguy cơ regression. -->

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Chat 1:1 và nhóm nhận tin inbound: LINE gộp nhiều tin/1 webhook (hoặc Webhook再送) giờ lưu đủ | F1, D1 | High — Test: gửi liên tiếp nhiều tin → verify đủ tin + badge/preview |
| T2 | Postback: batch có event nguồn khác trước event user → user không còn bị rớt | F2, D1 | Medium — Test: [group/room, user postback] → verify action user chạy |
| T3 | Video play complete: batch có not-friend đứng trước → action của user friend phía sau không bị bỏ | F3, D1 | Medium — Test: batch [NOT_FRIEND, friend VideoPlayComplete] |
| T4 | Follow: batch có user bị block đứng trước → các follow còn lại không bị rớt | F4, D2 | Medium — Test: batch [BLOCKED_BY_BOT, follow hợp lệ] |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
