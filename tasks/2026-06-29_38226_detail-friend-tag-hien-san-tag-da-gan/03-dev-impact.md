# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-filled từ Redmine #38226 (journal đánh giá ảnh hưởng của Ngọc Ánh, 2026-06-26) bằng `/new-task`.
> **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs.

> ⚠️ **Đánh giá ảnh hưởng từ Dev khá sơ sài** — mục 1 (Nguyên nhân) và mục 3 (caller đã check) để trống; mục 4 không tách 4.1/4.2/4.3 chi tiết. Leader nên hỏi lại Dev nếu cần trace code trước khi giao TC.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Hạnh Nguyễn` (assigned_to) — đánh giá ảnh hưởng do `Ngọc Ánh` viết |
| Commit / Pull Request | `<chưa có>` |
| Branch | `hot-fix-release/friend-info-26062026` |
| Ngày submit đánh giá | `2026-06-26` |
| Auto-filled | `2026-06-29 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- Nguyên văn từ Dev (mục 1) -->

`<Input thiếu — Dev để trống mục "1. Nguyên nhân" trong Redmine>`

(Suy từ Tái hiện/Cách fix: logic JS frontend của tab Tag mặc định render các folder ở trạng thái đóng dropdown, không tự xổ folder đang chứa tag được gắn.)

## 2. Cách fix

<!-- Nguyên văn từ Dev (mục 2) -->

Sửa js phía frontend.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Nguyên văn từ Dev (mục 3) -->

`<Input thiếu — Dev để trống mục "3" trong Redmine>`

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | | | |

---

## 4. Đánh giá ảnh hưởng

<!-- Nguyên văn từ Dev (mục 4): "UI màn /basic/friendlist/my_page tab tag. Ko ảnh hưởng Backend." -->

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | JS render danh sách folder/tag tại tab Tag (detail friend) | Frontend JS màn `/basic/friendlist/my_page` | Direct | Đổi trạng thái mặc định folder chứa tag → xổ sẵn |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | (Không có) | — | Dev xác nhận **không ảnh hưởng Backend** — chỉ sửa JS frontend |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Detail friend — tab Tag (現在ついているタグ): hiển thị folder/tag đang gắn | F1 | Medium |
| T2 | Add / gỡ tag cho friend (web, app, chat 1:1, multi action) | F1 | Medium |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
