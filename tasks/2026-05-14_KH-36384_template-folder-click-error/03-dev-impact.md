# 03 — Đánh giá ảnh hưởng từ Dev

> Nội dung này được lấy nguyên văn từ journal #118361 (Redmine #36384) của Ngô Thúy Ngần — 2026-05-14 09:35 UTC.
> Journal mix cả reproduction + dev impact. Phần reproduction đã chuyển vào `01-bug-task.md`; phần dev impact giữ ở đây.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | (chưa rõ — journal viết bởi Ngô Thúy Ngần — QA tổng hợp lại). Cần leader xác nhận dev owner. |
| Commit / Pull Request | `<chưa có link trong Redmine>` |
| Branch | `<chưa rõ>` |
| Ngày submit đánh giá | `2026-05-14` |

---

## 1. Nguyên nhân

User sử dụng link với hậu tố query string khác thường để **edit** template, ví dụ:

```
/basic/template-v2/add-template?template_group_id=13305886&template_child_id=13305944/?utm_source=line&utm_medium=social&utm_id=syanai20260515
```

→ `template_child_id` bị parse sai (lấy nguyên cả phần `13305944/?utm_source=line` thay vì chỉ `13305944`).
→ Khi save, `content` của template group bị lưu sai dạng `13305887,13305944/?utm_source=line` (đáng lẽ phải là `13305887,13305944`).
→ Lần sau click vào folder template để load list template con → parse `content` → fail → render error.

Template ID lỗi cụ thể trong production (journal #117993 — Kieu Son Tung):
- `template_group_id = 13305886`
- `content lỗi = 13305887,13305944/?utm_source=line`
- Update lần cuối: `2026-05-12 10:34:17`

## 2. Cách fix

- **Ép kiểu `int`** với `template_group_id` và `template_child_id` ngay khi nhận từ request (loại bỏ phần `/?utm_*` thừa).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `createTemplate` — `app/Http/Controllers/Basic/TemplateV2Controller.php` | Ép `int` cho `template_group_id` & `template_child_id` từ request | Root fix — chặn nguồn ô nhiễm |

> **Note QA**: journal chỉ liệt kê 1 function. Cần Leader xác nhận xem các action **save / edit / list / clone template** có dùng chung helper / cùng controller không — nếu có thì phải check thêm.

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `createTemplate` | `app/Http/Controllers/Basic/TemplateV2Controller.php` | Direct | Function được sửa trực tiếp (ép int) |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | (none) | — | Journal ghi rõ: "k có" → không có migration / mass-update khi deploy fix |

> Lưu ý: data đã hỏng trong production (`template_group_id=13305886`) đã được Ngọc Ánh **recover thủ công** ngày 2026-05-13 (journal #118251), không nằm trong scope fix code.

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Edit template (template con) | F1 | Medium — input ép int có thể reject case template_child_id hợp lệ nhưng truyền dạng string |
| T2 | Save template (template con) | F1 | Medium — flow chính bị chạm trực tiếp |

> **GAP có thể có** (Leader review):
> - **List template / Click folder template** — chính là trigger user-visible của bug. Journal không list trong 4.3 vì view-only không bị sửa code. Nhưng cần TC verify rằng sau khi fix createTemplate, không tồn tại data hỏng mới và view không còn crash.
> - **Add new template** (không qua edit) — cùng controller `TemplateV2Controller` có thể có function khác (vd `storeTemplate`) chưa được ép int → cần Leader hỏi Dev.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code — **cần xác nhận chỉ ép int ở `createTemplate` là đủ, hay có function khác cùng nhận `template_*_id` từ request?**
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót — đặc biệt `storeTemplate`, `updateTemplate`, `cloneTemplate`)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (recovery data production có cần verify lại không?)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** — cần thêm "List template (folder click)" như **trigger user-visible** dù view không bị sửa code
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
