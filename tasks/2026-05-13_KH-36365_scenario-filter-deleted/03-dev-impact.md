# 03 — Đánh giá ảnh hưởng từ Dev

> Trích nguyên văn từ sheet `Testcase` row 965.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | _<chưa rõ — verify Redmine / PR>_ |
| Commit / Pull Request | _<chưa có link>_ |
| Branch | _<chưa rõ>_ |
| Ngày submit đánh giá | 2026-05-11 (suy luận từ ngày bug `[11-05-2026]`) |

---

## 1. Nguyên nhân

Do user tạo step có **filter manager đã bị xóa** ở tab khác, nhưng GUI tab hiện tại không phản ánh trạng thái xóa (state stale). Function `createScenarioStep` không validate filter_id còn tồn tại trước khi insert.

## 2. Cách fix

- Khi tạo step, **check filter manager có tồn tại** không. Nếu không tồn tại → throw error + báo msg `フィルターが削除されたため、画面を再読み込みしてください`.
- **Xóa try/catch** swallow exception để **notify chatwork** khi có lỗi xảy ra.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

> Dev không liệt kê chi tiết → ngầm hiểu chỉ sửa F1 + caller flow của F1.

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `createScenarioStep` | `app/Http/Controllers/Basic/ScenarioController.php` | Direct | Function chính bị sửa — thêm validate filter + remove try/catch |

### 4.2. List data bị update khi fix bug

| # | Data | Ghi chú |
|---|---|---|
| _ | _**không có**_ — fix chỉ thay đổi validation logic, không động data schema | Theo dev report |

### 4.3. List tính năng bị ảnh hưởng

| # | Tính năng | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Tạo mới step message** (trong modal scenario) | F1 | High |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng — OK
- [ ] Mục 2 (cách fix) trace về code — **chưa có snippet code**. Leader nên hỏi dev: validate tại layer nào (controller / service / model)? Sử dụng query nào để check filter exist?
- [ ] Mục 3 đã check đủ caller — **dev report bỏ trống mục 3** → đáng nghi: có thực sự chỉ 1 function bị ảnh hưởng?
  - Câu hỏi: `updateScenarioStep` (EDIT step) có cùng vấn đề không? Function gì check khi scenario chạy step (lúc send message)?
  - Có function nào khác đang gọi `createScenarioStep`?
- [ ] Mục 4.1 không thiếu function — **nghi vấn**: chỉ liệt kê 1 function quá ít cho 1 bug Production.
- [ ] Mục 4.2 không thiếu data — dev khẳng định "k có" OK.
- [ ] Mục 4.3 cover happy + edge case — **chỉ "tạo mới step message"** — không cover:
  - **Send message lifecycle**: bug gốc là "duplicate send" → cần regression test send step → đảm bảo không gửi 2 lần.
  - **Edit step message** (nếu cùng vấn đề).
  - **Notify chatwork** (dev mention xóa try/catch để notify) — đây là behavior change cần TC verify.
- [ ] **Nghi vấn cần hỏi dev**:
  1. Validate ở layer nào? Có dùng transaction để tránh TOCTOU race (check filter exist → insert step → trong gap đó filter có thể bị xóa)?
  2. Filter có **soft delete** không (chỉ flag is_deleted=1) hay hard delete? Logic check dùng `WHERE id = ?` hay `WHERE id = ? AND is_deleted = 0`?
  3. Có cascade behavior khi xóa filter trong khi có step đang dùng filter đó? Hoặc block delete?
  4. Notify chatwork chi tiết payload gì khi exception?
  5. `updateScenarioStep` có cùng validation chưa?
