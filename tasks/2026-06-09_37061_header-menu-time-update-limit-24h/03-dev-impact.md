# 03 — Đánh giá ảnh hưởng từ Dev

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-url>` → Claude parse section "Đánh giá ảnh hưởng" trong Redmine, fill các mục bên dưới. Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — Dev paste nguyên văn đánh giá theo format 4 mục.
>
> **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Tuấn Anh Trần` (assigned_to) |
| Commit / Pull Request | `<chưa có>` |
| Branch | `<chưa rõ>` |
| Ngày submit đánh giá | `2026-06-08` |
| Auto-filled | `2026-06-09 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- Dev mô tả root cause. Càng cụ thể càng tốt: file nào, function nào, logic sai ở đâu. -->

- Chưa lưu lại thời gian get limit.

## 2. Cách fix

<!-- Dev mô tả cách fix. Nếu có snippet code thì càng tốt. -->

- Lưu thời gian get limit vào bot.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Dev liệt kê các nơi đã được check & update khi fix bug (caller functions, data dependencies). -->

> ⚠️ Dev không ghi rõ nội dung mục 3 trong Redmine (chỉ để tiêu đề). Tham chiếu mục 4.1 cho list function liên quan. Leader hỏi lại Dev nếu cần xác nhận đã check đủ caller.

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | | | |
| 2 | | | |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Mọi function Dev đã sửa HOẶC có thể bị ảnh hưởng gián tiếp. -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `fetchInfoBot()` | `app/Http/Controllers/Admin/UserController.php` | Direct | |
| F2 | `summaryMessageSend()` | `app/Http/Controllers/Basic/BasicController.php` | Direct | |
| F3 | `step2CheckFriend()` | `app/Http/Controllers/Admin/BotController.php` | Direct | |

### 4.2. List data bị update khi fix bug

<!-- Mọi bảng DB, field, cache, config, migration,... bị chạm tới. -->

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | Dev ghi: **Không có** | — | (Lưu ý: cách fix là "lưu thời gian get limit vào bot" → có khả năng có field thời gian được ghi vào bảng `bot`. Leader xác nhận lại với Dev — có vẻ mâu thuẫn với "Không có".) |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

<!-- Dev suy ra từ 4.1 và 4.2: tính năng end-user nào có nguy cơ regression. -->

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Fetch info bot trên header (hiển thị thời gian cập nhật limit) | F1 | Medium |
| T2 | Màn Summary message send | F2 | Medium |
| T3 | Change bot | F1, F3 | Medium |
| T4 | Add bot | F1, F3 | Medium |
| T5 | Click btn load lại thông tin bot | F1 | Medium |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót) — **mục 3 Redmine để trống, cần hỏi Dev**
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file) — **"Không có" mâu thuẫn với cách fix "lưu vào bot", xác nhận lại**
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
