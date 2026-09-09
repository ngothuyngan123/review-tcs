# 03 — Đánh giá ảnh hưởng từ Dev

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-url>` → Claude parse section "Đánh giá ảnh hưởng" trong Redmine, fill các mục bên dưới. Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — Dev paste nguyên văn đánh giá theo format 4 mục.
>
> **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Do Van Tu (TuDV)` (assigned_to) — đánh giá ảnh hưởng post bởi `Kim Cúc`; `@tudovan2026` confirm phần đánh giá |
| Commit / Pull Request | `https://bitbucket.org/snstool/linect-service/commits/ef7f3cbadb01abd4dbe1281882521758d66b54cb`<br>AI review bổ sung: `https://bitbucket.org/snstool/linect-service/commits/61e86cb0827252f3bf6a9e52905d7fef3612a65a` |
| Branch | `<chưa rõ>` |
| Ngày submit đánh giá | `2026-06-13` |
| Auto-filled | `2026-06-13 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- Dev mô tả root cause. Càng cụ thể càng tốt: file nào, function nào, logic sai ở đâu. -->

- Trường hợp URL của KH **không setting param info nào** thì thiếu `forward_param` — chưa được set vào URL.

## 2. Cách fix

<!-- Dev mô tả cách fix. Nếu có snippet code thì càng tốt. -->

- Set bổ sung thêm `forward_param` nếu có.
- Ví dụ về giá trị `forward_param`: `sid=YmlaNXEzZk1q&test=true`

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Dev liệt kê các nơi đã được check & update khi fix bug (caller functions, data dependencies). -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `HandlePostbackTask.doHandleFollowEvent` | Bổ sung thêm `forward_param` vào URL | Set param KH tự nhập vào URL callback (xem mục 4.1) |

> ⚠️ Dev chỉ ghi tiêu đề mục 3 ("Đã check và sửa các function..."), **không liệt kê chi tiết** caller khác. Leader cần hỏi lại Dev: ngoài `doHandleFollowEvent` còn flow nào build URL callback (vd new friend / old friend / unblock / đang friend) bị ảnh hưởng không?

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Mọi function Dev đã sửa HOẶC có thể bị ảnh hưởng gián tiếp. -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `HandlePostbackTask.doHandleFollowEvent` | `<chưa rõ — Dev không ghi path>` | Direct | Bổ sung thêm `forward_param` vào URL callback |

### 4.2. List data bị update khi fix bug

<!-- Mọi bảng DB, field, cache, config, migration,... bị chạm tới. -->

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | Không có | — | Dev xác nhận không có data bị update |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

<!-- Dev suy ra từ 4.1 và 4.2: tính năng end-user nào có nguy cơ regression. -->

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Callback URL (Parameter Export) — case URL **đã có** setting param info (`forward_param`, `mail`, `friend_name`, `friend_type`, `line_id`) → chỉ replace những param được truyền vào | F1 | Medium |
| T2 | Callback URL (Parameter Export) — case URL **không** setting param info → set hết `forward_param`, `mail`, `friend_name`, `friend_type`, `line_id` | F1 | High |

**Các điểm Dev tự đánh dấu cần confirm (mục 4.3 raw):**
- Case URL **đã có** setting param info: `forward_param`, `mail`, `friend_name`, `friend_type`, `line_id` ⇒ chỉ replace những param được truyền vào.
- Case URL **không** setting: set hết `forward_param`, `mail`, `friend_name`, `friend_type`, `line_id`.
  - ❓ Case `forward_param` rỗng hoặc null có cần set không?
  - ❓ (AI bổ sung) Kiểm tra case đã có param sẵn trong URL rồi thì bỏ qua param đó? VD: URL chứa sẵn param `sid`, và trong `forward_param` cũng có `sid`?

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
