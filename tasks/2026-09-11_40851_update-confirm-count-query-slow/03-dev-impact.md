# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (hệ thống Auto-fixbug LME) — assignee Redmine: Ngô Thúy Ngần |
| Commit / Pull Request | commit `0b0bc81b12` (repo `sns-line`) — không có link PR trong ticket. Session AI: https://claude-admin.melonglobal.net/?project=implement-task-small-lme&tab=events&session=a50cdef9-c1b4-4aba-8966-4d65f1a0b921 · Dashboard: https://dashboard.melonglobal.net/implement-task-small-lme/?id=40851 |
| Branch | `ai_small_40851` (nhánh gốc `release_step_20260805`, 1 file thay đổi, đã push) |
| Ngày submit đánh giá | 2026-09-11 (Journal #135819) |
| Auto-filled | `2026-09-11 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Câu lệnh chậm 95 giây trong log đến từ API "đánh dấu đã đọc toàn bộ hội thoại theo bot" (app gọi qua đường dẫn `make-read-all-message-by-bot`). Code cũ nạp **TOÀN BỘ** id hội thoại chưa bị chặn của bot từ PHP rồi chạy đúng một câu xoá và một câu cập nhật với danh sách id khổng lồ. Danh sách id quá dài khiến MySQL bỏ qua tối ưu theo khoá chính và **quét gần như toàn bộ bảng hội thoại** (hơn 50 triệu dòng đã đọc, 0 dòng trả về), đồng thời **khoá rất nhiều dòng** trong một lần ghi. Code cũ còn ghi đè cả hội thoại vốn đã ở trạng thái đã đọc nên khối lượng ghi lớn hơn mức cần thiết.

## 2. Cách fix

Sửa hàm xử lý API đánh dấu đã đọc toàn bộ hội thoại theo tài khoản trong bộ điều khiển chat của nhóm API:

1. Thay cách nạp toàn bộ id hội thoại rồi chạy một câu cập nhật khổng lồ bằng **xử lý theo lô 1000 hội thoại** — mỗi lô chỉ một câu xoá bản ghi chưa xác nhận và một câu cập nhật giới hạn id, **duyệt tiến theo id** (`chunkById`, sort tăng dần theo khoá chính, `limit 1000`) nên không lặp lại và không bỏ sót.
2. Thêm **điều kiện lọc**: chỉ lấy hội thoại thực sự còn lệch trạng thái đã đọc **hoặc** còn bản ghi chưa xác nhận → không ghi đè lại các hội thoại vốn đã đọc.

**Hành vi nghiệp vụ giữ nguyên.**

**Quét ngang (Dev tự khai)**: hai hàm cùng tính năng bên nhóm API và nhóm Mobile dùng vòng lặp từng hội thoại (kiểu chậm khác) nên **để ngoài phạm vi ticket này**.

> ⚠️ Ghi chú của Leader — điểm cần soi khi review TC:
> - Fix dùng lại **cùng khuôn mẫu đã được duyệt ở ticket #39257** (chức năng tương đương bên **web**).
> - Mức verify của Dev chỉ là **lint** + dựng SQL bằng Illuminate Capsule; **không kết nối được DB dev** để chạy thật.
> - Dev đề nghị reviewer **xác nhận index** trên `conversation` theo cột bot trên môi trường thật (repo không có danh sách index).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `makeReadAllMessageByBot` — `app/Http/Controllers/Api/ChatController.php` | **CÓ SỬA** — chuyển sang xử lý theo lô 1000 + thêm điều kiện lọc hội thoại còn lệch trạng thái | Chính là hàm sinh ra câu update chậm trong slow query log |
| 2 | `makeReadMessageAll` — `app/Http/Controllers/Api/ChatController.php` | Không sửa | Cùng tính năng nhưng dùng vòng lặp từng hội thoại (kiểu chậm khác) — Dev để ngoài phạm vi ticket |
| 3 | `makeReadMessageByIds` — `app/Http/Controllers/Api/ChatController.php` | Không sửa | Đã check, đánh dấu đã đọc theo danh sách id do client truyền — không sinh danh sách id khổng lồ |
| 4 | `makeReadMessageAll` — `app/Http/Controllers/Mobile/ChatMobileController.php` | Không sửa | Cùng tính năng bên nhóm Mobile, vòng lặp từng hội thoại — Dev để ngoài phạm vi ticket |
| 5 | `ConversationService::confirmReadMessage` — `app/Services/ConversationService.php` | Không sửa | Đường ghi trạng thái đã đọc dùng chung — đã check, không đổi |
| 6 | `updateLastMessage` — `app/Helpers/functions.php` | Không sửa | Hàm dùng chung cập nhật last message / trạng thái — đã check, không đổi |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

> Dev khai mục 4.1 dưới dạng **"File thay đổi"** (chỉ 1 file). Bảng dưới ánh xạ về function theo mục 3.

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `makeReadAllMessageByBot` — API `make-read-all-message-by-bot` (đánh dấu đã đọc toàn bộ hội thoại theo bot, gọi từ mobile app) | `app/Http/Controllers/Api/ChatController.php` | **Direct** | File DUY NHẤT được thay đổi trong branch `ai_small_40851` |
| F2 | `ConversationService::confirmReadMessage` | `app/Services/ConversationService.php` | Indirect | Đã check, không sửa — dùng chung đường ghi trạng thái đã đọc |
| F3 | `updateLastMessage` | `app/Helpers/functions.php` | Indirect | Đã check, không sửa |
| F4 | `makeReadMessageAll` (API) · `makeReadMessageAll` (Mobile) · `makeReadMessageByIds` (API) | `Api/ChatController.php` · `Mobile/ChatMobileController.php` | **Ngoài phạm vi (không sửa)** | Cùng tính năng đánh dấu đã đọc — Dev khai chủ động loại khỏi ticket. Vẫn là vùng **regression** cần verify không bị ảnh hưởng |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `conversation.confirm_count` · `conversation.status_last_message` · `conversation.has_status_0/1/2/3/5/7/8/9` | UPDATE | Vẫn được đặt về trạng thái đã đọc như cũ, **chỉ khác là bỏ qua dòng đã đúng trạng thái** |
| D2 | `conversation.updated_at` | UPDATE | **Thay đổi hành vi quan sát được**: không còn bị đẩy mới ở các hội thoại vốn đã đọc |
| D3 | `unconfirm_message` (theo `conversation_id`) | DELETE | Vẫn xoá theo hội thoại, chỉ chia thành **nhiều lô nhỏ** (1000/lô) thay vì 1 câu xoá duy nhất |
| D4 | `bots.count_user_unconfirm` · `bots.last_time_count_user_confirm` | UPDATE | Giữ nguyên như cũ |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **1-on-1 Chat (FA-001)** — chức năng đánh dấu đã đọc toàn bộ hội thoại của một tài khoản **từ ứng dụng di động** | F1, D1, D3 | **High** (đường code trực tiếp bị sửa) |
| T2 | **Chat / Talk Management (FA-002)** — số lượng hội thoại chưa đọc và huy hiệu (badge) thông báo tính lại sau khi đánh dấu đã đọc | F1, D1, D4 | Medium |
| T3 | Sắp xếp / lọc danh sách hội thoại theo `updated_at` (nếu màn hình Chat dùng cột này để sort) | D2 | Medium — `updated_at` không còn được đẩy mới ở hội thoại vốn đã đọc, có thể đổi thứ tự hiển thị so với trước |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
