# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Thanh Duy Nguyen` |
| Commit / Pull Request | `<chưa có — chỉ có tên branch, chưa thấy link PR trong journal>` |
| Branch | `m_202609_forward_webhook_40475_improve_query` (merge vào `release-t09-2026`) |
| Ngày submit đánh giá | `2026-10-15` |
| Auto-filled | `2026-10-15 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

- **Kênh 1**: callback_event status `11`/`111` (webhook trùng) bị câu quét loại ra nên `status_sync` mãi `NULL`, tích tụ ở đầu dải `status_sync IS NULL` → mỗi vòng quét đi lại toàn bộ đống đó, chậm dần theo thời gian.
- **Cả 2 kênh** (Kênh 1 = callback_event, Kênh 2 = tag_history / friend_info_history): batch có data (dù chỉ vài row) đều chỉ nghỉ 200ms → lúc đã đuổi kịp vẫn bắn query liên tục vào bảng nóng.

## 2. Cách fix

- **Kênh 1**: câu quét chỉ loại status `0`/`1`/`100`/`101` (chưa / đang xử lý), row `11`/`111` lấy ra rồi đánh `status_sync = 4` (IGNORE) trước khi check setting bot → vẫn không forward webhook trùng (tham chiếu #41514).
- **Cả 2 kênh**: batch đủ 500 nghỉ 200ms, batch thiếu/rỗng nghỉ 1s; `LIMIT` truyền qua param `BATCH_SIZE` thay vì hardcode 500.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `CallbackEventRepository` | Đổi tên `findTop500NotForwardYet` → `findNotForwardYet` | LIMIT giờ truyền qua param `BATCH_SIZE` thay vì hardcode 500 trong tên method |
| 2 | `TagHistoryRepository` | Đổi tên `findTop500ByStatusSyncIsNullOrderByIdAsc` → `findNotForwardYet` | cùng lý do trên (Kênh 2) |
| 3 | `FriendInfoHistoryRepository` | Đổi tên `findTop500ByStatusSyncIsNullOrderByIdAsc` → `findNotForwardYet` | cùng lý do trên (Kênh 2) |
| 4 | Hằng `CALLBACK_STATUS_NOT_FORWARD` | Tách thành `CALLBACK_STATUS_NOT_READY` + `CALLBACK_STATUS_DUPLICATE` | Mỗi tên method/hằng ở trên chỉ có **1 caller** ở 2 Manager (`HandleForwardCallbackEventManager`, `HandleForwardLmeEventManager`) — Dev xác nhận đã update cùng PR, không sót caller ngoài |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `findNotForwardYet` (trước: `findTop500NotForwardYet`) | `CallbackEventRepository` | Direct | Đổi điều kiện WHERE (chỉ loại `0/1/100/101`) + LIMIT theo param `BATCH_SIZE` |
| F2 | `findNotForwardYet` (trước: `findTop500ByStatusSyncIsNullOrderByIdAsc`) | `TagHistoryRepository` | Direct | Đổi tên method + LIMIT theo param `BATCH_SIZE` (logic quét không đổi, không có status 11/111 ở kênh này) |
| F3 | `findNotForwardYet` (trước: `findTop500ByStatusSyncIsNullOrderByIdAsc`) | `FriendInfoHistoryRepository` | Direct | Đổi tên method + LIMIT theo param `BATCH_SIZE` |
| F4 | `startJobPushToQueue`, `addToQueue` | `HandleForwardCallbackEventManager` | Direct | Caller của F1; thêm logic set `status_sync = 4` (IGNORE) cho row `11`/`111` trước khi check setting bot; đổi sleep batch đủ/thiếu (200ms/1s thay cho 2s cố định) |
| F5 | `startJobScanTagHistory`, `startJobScanFriendInfoHistory` | `HandleForwardLmeEventManager` | Direct | Caller của F2/F3; đổi sleep batch đủ/thiếu (200ms/1s thay cho 2s cố định) |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `callback_event.status_sync` | UPDATE | Row status `11`/`111` đang `NULL` → chuyển thành `4` (IGNORE) khi vòng quét chạy qua |
| D2 | Constant `CALLBACK_STATUS_NOT_FORWARD` (code-level, không phải DB) | MIGRATE (refactor hằng số) | Tách thành `CALLBACK_STATUS_NOT_READY` (status `0/1/100/101`) + `CALLBACK_STATUS_DUPLICATE` (status `11/111`) |
| D3 | `LIMIT` câu quét 3 bảng (callback_event, tag_history, friend_info_history): hardcode `500` → truyền qua param `BATCH_SIZE` | UPDATE (code) | Nguồn: mục 2 "Cách thực hiện" — Dev không kê ở 4.2, auto-fill tách ra để map coverage |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Forward webhook Kênh 1 — row status `11`/`111` (webhook trùng, LINE redelivery) | F1, F4, D1 | Medium — row trùng chuyển `status_sync = 4`, bên thứ 3 **không** nhận; cần verify đúng case trùng mới bị IGNORE, không ảnh hưởng event thường |
| T2 | Forward webhook Kênh 1 — row status `0`/`1` (chưa/đang xử lý) | F1, F4 | Low — vẫn `NULL`, forward đủ ở vòng sau khi xử lý xong (status `2`) |
| T3 | Forward webhook Kênh 2 (tag / friend info) — payload, gom lô khi insert nhiều row liên tục (>500) | F2, F3, F5, D3 | Low/Medium — Dev confirm payload + gom lô không đổi, check vẫn forward đủ; cần verify biên khi insert dồn > `BATCH_SIZE` |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
