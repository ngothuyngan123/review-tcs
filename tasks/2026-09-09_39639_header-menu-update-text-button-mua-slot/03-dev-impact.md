# 03 — Đánh giá ảnh hưởng từ Dev

> ⚠️ **INPUT THIẾU: Redmine #39639 chưa có section "Đánh giá ảnh hưởng phía dev"** (không có mục 1 nguyên nhân / 2 cách fix / 3 caller đã check / 4.1-4.2-4.3).
> Dev input duy nhất là **1 dòng journal #135417**: `ảnh hưởng: text button upgrade plan khi có bot free và chưa có bot free`.
> `/write-tc` và `/review-tc` chạy với input này sẽ **thiếu chiều coverage `dev-impact`** (BƯỚC 2 chiều (a)). **Yêu cầu Dev bổ sung đánh giá ảnh hưởng 4 mục trước khi tiếp tục.**

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Ngọc Ánh` (assignee Redmine) — note ảnh hưởng do `Tuấn Anh Trần` ghi |
| Commit / Pull Request | `<chưa có — Redmine không có link commit/PR; custom field "Commit Date" để trống>` |
| Branch | `<chưa rõ — Redmine không ghi; Studio task #112 ghi branch \`ai-feature-39639\` (branch của pipeline AI, KHÔNG chắc là branch dev)>` |
| Ngày submit đánh giá | `2026-09-09` (journal #135417 — chỉ 1 dòng, không đủ 4 mục) |
| Auto-filled | `2026-09-09 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

`<Input thiếu — Dev chưa cung cấp>`

Ghi chú: ticket là **Feature** (yêu cầu đổi text theo design), không có root cause bug.

## 2. Cách fix

`<Input thiếu — Dev chưa cung cấp>`

Yêu cầu từ ticket (không phải Dev mô tả cách fix):
- Case **chưa có bot free** → button hiển thị 「フリープランでLINE公式アカウント追加」
- Case **đã có bot free** → button hiển thị 「有料プランを契約してLINE公式アカウント追加」 + dòng ghi chú dưới button 「※フリープランはすでにご利用中のため、ご選択いただけません。」

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

`<Input thiếu — Dev chưa cung cấp>`

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `<Input thiếu>` | | |
| 2 | `<Input thiếu>` | | |

---

## 4. Đánh giá ảnh hưởng

> Nguyên văn phần Dev cung cấp (journal #135417 — 2026-09-09):
> ```
> ảnh hưởng: text button upgrade plan khi có bot free và chưa có bot free
> ```
> Dev **không** tách 4.1 / 4.2 / 4.3. Các bảng dưới đây chỉ ghi lại đúng phạm vi Dev nêu, phần còn lại để `<Input thiếu>` — **KHÔNG suy diễn thêm impact**.

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | Render text button upgrade plan / thêm LOA theo trạng thái có/chưa có bot free | `<Input thiếu — Dev chưa nêu file>` | Direct | Đúng phạm vi journal #135417 |
| F2 | `<Input thiếu — Dev chưa cung cấp>` | | | |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `<Input thiếu — Dev chưa cung cấp>` | | Dev không nêu data impact. Thay đổi text UI thường chỉ **đọc** số bot free (`bots.plan_type=2, is_deleted=0`) — cần Dev xác nhận, KHÔNG tự kết luận |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Button thêm LOA / upgrade plan (2 nhánh: đã có bot free / chưa có bot free) | F1 | `<Dev chưa đánh giá>` |
| T2 | `<Input thiếu — Dev chưa cung cấp>` | | |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

### Câu hỏi cần hỏi Dev (do input thiếu)

1. File/view nào bị sửa? (Studio task #112 ghi `resources/views/admin/index_v3.blade.php`, `public/css/admin/index_v3.css`, `app/Http/Controllers/Admin/UserController.php:363-367` — **cần Dev xác nhận**, đây là dữ liệu Studio chứ không phải Dev khai)
2. Điều kiện tính "đã có bot free" là gì? (đếm `plan_type=2, is_deleted=0`?)
3. Button có bị **disable** khi đã có bot free không? Text 「ご選択いただけません」 dễ hiểu là bị chặn — nhưng chặn thì admin mất đường thêm LOA trả phí.
4. Màn 「アカウント選択」 (`/admin/pre-select-bot`) dùng chung cờ này có bị đổi text theo không?
5. Admin đăng ký **trước 2021-07-01** (được có nhiều bot free) thì hiển thị nhánh nào?
