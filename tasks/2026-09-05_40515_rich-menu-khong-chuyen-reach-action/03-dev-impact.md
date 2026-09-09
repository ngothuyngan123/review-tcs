# 03 — Đánh giá ảnh hưởng từ Dev

> ⚠️ **INPUT THIẾU: Redmine #40515 chưa có "Đánh giá ảnh hưởng phía dev".**
> Ticket đang ở status `New`, **chưa assign Dev** (`assigned_to: null`), description chỉ có nội dung hỏi từ khách (WSSJ / OEM — TY-12071) và 3 journal, **không có** mục 1 Nguyên nhân / 2 Cách fix / 3 Function caller / 4 Đánh giá ảnh hưởng.
> `/write-tc` và `/review-tc` sẽ **thiếu căn cứ coverage** nếu chạy với input này. **Yêu cầu Dev bổ sung trước khi tiếp tục.**
>
> Toàn bộ nội dung dưới đây là **skeleton rỗng** — `/new-task` KHÔNG tự suy diễn root cause.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `<chưa rõ>` — Redmine `assigned_to` = null |
| Commit / Pull Request | `<chưa có>` — không tìm thấy link Github/Gitlab/Bitbucket trong description hoặc journals |
| Branch | `<chưa rõ>` |
| Ngày submit đánh giá | `<chưa rõ>` — chưa có journal nào chứa đánh giá ảnh hưởng |
| Auto-filled | `2026-09-05 by /new-task` (skeleton — Redmine không có Section "Đánh giá ảnh hưởng") |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- Dev mô tả root cause. Càng cụ thể càng tốt: file nào, function nào, logic sai ở đâu. -->

`<Input thiếu — Dev chưa cung cấp>`

> Ghi chú: đây là bug **xác suất ~2〜3%**, khách **nghi ngờ** (chưa xác nhận) 2 hướng — (a) xung đột do 「ステップ停止」「ステップ開始」「タグ付与/解除」 chạy đồng thời trong cùng QR code action, (b) lỗi tạm thời phía LINE API mà không được retry. **Đây là giả thuyết của khách, KHÔNG phải root cause đã xác định.**

## 2. Cách fix

<!-- Dev mô tả cách fix. Nếu có snippet code thì càng tốt. -->

`<Input thiếu — Dev chưa cung cấp>`

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Dev liệt kê các nơi đã được check & update khi fix bug (caller functions, data dependencies). -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `<Input thiếu — Dev chưa cung cấp>` | | |
| 2 | | | |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Mọi function Dev đã sửa HOẶC có thể bị ảnh hưởng gián tiếp. -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `<Input thiếu — Dev chưa cung cấp>` | | Direct / Indirect | |
| F2 | | | | |
| F3 | | | | |

### 4.2. List data bị update khi fix bug

<!-- Mọi bảng DB, field, cache, config, migration,... bị chạm tới. -->

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `<Input thiếu — Dev chưa cung cấp>` | CREATE / UPDATE / DELETE / MIGRATE | Journal #134203 có gợi ý bảng `action_lineuser` (query điều tra `WHERE bot_id = 153327 AND line_user_id = 41160486`) — **là query điều tra của người báo bug, KHÔNG phải data impact do Dev xác nhận** |
| D2 | | | |
| D3 | | | |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

<!-- Dev suy ra từ 4.1 và 4.2: tính năng end-user nào có nguy cơ regression. -->

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | `<Input thiếu — Dev chưa cung cấp>` | F1, D1 | High / Medium / Low |
| T2 | | | |
| T3 | | | |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
