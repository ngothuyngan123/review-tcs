# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Thanh Duy Nguyen` (tác giả Journal #136170) |
| Commit / Pull Request | `7b0c7762`, `da2030ef` |
| Branch | `m_202609_fix_lock_conversation_40768` → `release-t08-2026` |
| Ngày submit đánh giá | `2026-09-12` (Journal #136170) |
| Auto-filled | `2026-09-12 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- Nguyên văn từ Redmine #40768 Journal #136170 -->

- Web `WssvWeb2025` chạy bulk `UPDATE conversation WHERE id IN (~6150 id)` full-scan ~50 triệu row, giữ X-lock 87-95s (41 lần trong 10 ngày 01-10/09) → `UPDATE conversation` trong `HandlePostbackTask.updateLastMessage` chờ quá `innodb_lock_wait_timeout` 50s, ném `CannotAcquireLockException`.
- `updateLastMessage` được gọi bên trong `replyCallback.accept` của `checkAutoReply` nên exception nhảy thẳng xuống catch ngoài, bỏ qua vòng `doActionAutoReplyAccept` (bước gửi auto reply thật). `AutoReplyHistory` đã save ở transaction riêng trước đó nên không gửi bù. Log 09/09 có 3 lần `#checkAutoReply Exception` (bot 49501, 109213, 50104) nằm trọn trong cửa sổ web giữ lock 12:00:29-12:01:57.

## 2. Cách fix

<!-- Nguyên văn từ Redmine #40768 Journal #136170 -->

- Bọc `try/catch` riêng cho **10 chỗ** ghi bảng `conversation` để lock timeout không abort luồng phía sau — quan trọng nhất là bước gửi auto reply và notify chat 1:1; mỗi catch log đủ param đã truyền vào query để recover thủ công từ log.
- Set `hasReply.setHasCallback(true)` **trước khi** gọi `replyCallback.accept` để catch không gọi `accept` lần 2 (trước đây gây insert trùng `unconfirm_message` và chờ lock thêm 1 lượt 50s).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Nguyên văn từ Redmine #40768 Journal #136170 -->

- Chỉ thêm `try/catch` + log trong thân hàm, **không đổi signature / return type / thứ tự gọi** của hàm nào.
- Grep caller: `updateLastMessage` 3 caller (L1568, 1744, 1927), `checkAutoReply` 2 caller (L1706, 1781), `checkAddGroup` 2 caller (L527, 801) — đều trong cùng file, tham số không đổi → không ảnh hưởng caller, scope local.

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `HandlePostbackTask.updateLastMessage` — 3 caller: L1568, L1744, L1927 | Thêm `try/catch` + log, không đổi signature | Caller cùng file, tham số không đổi → scope local |
| 2 | `HandlePostbackTask.checkAutoReply` — 2 caller: L1706, L1781 | Thêm `try/catch` + log; set `hasReply.setHasCallback(true)` trước `replyCallback.accept` | Chặn gọi `accept` lần 2 → tránh insert trùng `unconfirm_message` + chờ lock 2 lượt |
| 3 | `HandlePostbackTask.checkAddGroup` — 2 caller: L527, L801 | Thêm `try/catch` + log, không đổi signature | Caller cùng file, tham số không đổi → scope local |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Nguyên văn mục 4.1 Redmine — đánh tag F* theo quy ước repo -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `handleMessage` | `HandlePostbackTask` | Direct | Nhóm xử lý tin nhắn đến + auto reply |
| F2 | `checkAutoReply` | `HandlePostbackTask` | Direct | Nhóm xử lý tin nhắn đến + auto reply — điểm fix chính (`setHasCallback(true)` trước `accept`) |
| F3 | `updateLastMessage` | `HandlePostbackTask` | Direct | Nhóm xử lý tin nhắn đến + auto reply — hàm ném `CannotAcquireLockException` |
| F4 | `checkAddOldFriend` | `HandlePostbackTask` | Direct | Nhóm follow/unfollow |
| F5 | `doHandleFollowEvent` | `HandlePostbackTask` | Direct | Nhóm follow/unfollow |
| F6 | `doHandleUnFollowEvent` | `HandlePostbackTask` | Direct | Nhóm follow/unfollow |
| F7 | `checkAddGroup` | `HandlePostbackTask` | Direct | Nhóm join/leave group |
| F8 | `doHandleLeaveGroup` | `HandlePostbackTask` | Direct | Nhóm join/leave group |
| F9 | `readDataCSVV1` | `HandleImportCsvTask` | Direct | Import CSV set trạng thái đã đọc |

### 4.2. List data bị update khi fix bug

<!-- Nguyên văn mục 4.2 Redmine -->

**Không có** — chỉ thêm `try/catch` + log, không đổi SQL / DDL / config / constant / field entity.

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| — | *(không có)* | — | Dev khẳng định không đổi SQL / DDL / config / constant / field entity |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

<!-- Nguyên văn mục 4.3 Redmine — đánh tag T* theo quy ước repo -->

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Auto reply** — nhắn keyword cho bot lúc `conversation` đang bị web lock, check auto reply vẫn gửi được, không rớt như bug cũ | F1, F2, F3 | High |
| T2 | **Chat 1:1 + notify** — check tin đến vẫn lên danh sách chat và vẫn có notify app/PC khi update `conversation` lỗi | F1, F3 | High |
| T3 | **Follow/unfollow** — test block rồi follow lại, check `is_blocked` / `is_old_friend` đúng, welcome message + scenario start vẫn chạy | F4, F5, F6 | Medium |
| T4 | **Join/leave group** — test bot bị kick khỏi group/room rồi add lại, check trạng thái blocked của `conversation` | F7, F8 | Medium |
| T5 | **Import CSV set trạng thái đã đọc** — import lúc `conversation` bị lock, check không dừng giữa file | F9 | Medium |

---

## 5. Commit / Branch (nguyên văn Redmine mục 5)

- `m_202609_fix_lock_conversation_40768` → `release-t08-2026` (commit `7b0c7762`, `da2030ef`)

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

> ⚠️ **Điểm Leader cần soi khi review** (không phải nội dung Dev viết — ghi chú của `/new-task`):
> - Mục 2 nói **"10 chỗ ghi bảng `conversation`"** nhưng mục 4.1 chỉ liệt kê **9 function** → cần đối chiếu lại: 1 chỗ nằm trong function đã kê hay có function thứ 10 chưa kê?
> - Đây là **generic fix dạng bọc `try/catch`** — theo rule generic-fix, cần cover **≥ 3 trigger** khác nhau + **≥ 1 fallback lỗi lạ** (không chỉ `CannotAcquireLockException`).
> - Mục 4.2 ghi "không có data bị update" nhưng fix **chấp nhận mất dữ liệu có kiểm soát** (`conversation.last_message` không được cập nhật khi catch) → thực tế **có** ảnh hưởng dữ liệu quan sát được ở màn chat 1:1, cần TC verify hệ quả này.
