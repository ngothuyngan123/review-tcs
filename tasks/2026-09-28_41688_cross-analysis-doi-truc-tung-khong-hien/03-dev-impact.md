# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-fill từ Redmine #41688 qua `/new-task`. Nguồn: Journal #139074 (AI Reader) — nội dung đánh giá ảnh hưởng theo đúng format 4 mục; Journal #139076 (Do Van Tu TuDV) — branch code.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Do Van Tu TuDV (theo Journal #139076)` |
| Commit / Pull Request | `<chưa có>` |
| Branch | `ai_fixbug_41688` |
| Ngày submit đánh giá | `2026-09-28` |
| Auto-filled | `2026-09-28 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Journal #139074 trên Redmine #41688 và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

- Khi lưu cross analysis, FE gửi kèm toàn bộ `line_user_id` của filter gốc (bot KH ~68,000 người) → request vượt `max_input_vars` của PHP → PHP cắt mất các param phía sau, trong đó có `filter_by` (tiêu chí phân tích).
- Backend mặc định `filter_by = 1` (友だち情報) khi thiếu → tiêu chí tag/ngày bị ghi đè thành friend info rỗng → danh sách phân tích không có dòng nào.

## 2. Cách fix

- FE: không gửi `line_user_ids` khi lưu (backend không dùng dữ liệu này cho phân tích).
- BE: bỏ mặc định `filter_by = 1`; `filter_by` không hợp lệ → trả lỗi 400 và không lưu, tránh ghi đè sai tiêu chí.
- FE: hiển thị message lỗi khi lưu thất bại.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | Xác nhận bằng request thật | (không phải sửa code) | 12,466 input vars, `line_user_ids` 12,450 phần tử đứng trước `filter_by` |
| 2 | `line_ids_parent` (đọc lại cho tính toán) | không sửa | Xác nhận `line_ids_parent` không được đọc cho tính toán (`initDataCross` / `resultCrossAnalysis` / command đều tính lại) |
| 3 | `filter_by` giá trị hợp lệ trong luồng bình thường | không sửa | Xác nhận `filter_by` luôn có giá trị hợp lệ trong luồng bình thường (FE default 2, DB default 1) |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `saveCross()` | `public/js/cross_analysis/create.js` | Direct | FE — bỏ gửi `line_user_ids` khi lưu |
| F2 | `saveCrossAnalysis()` | `app/Http/Controllers/Basic/CrossAnalysisController.php` | Direct | BE — bỏ default `filter_by = 1`, trả 400 khi invalid |
| F3 | `initDataCross()`, `initAnalysis()`, `getDataCrossReset()`, `copyCross()` | `app/Http/Controllers/Basic/CrossAnalysisController.php` | Indirect | Đọc dữ liệu lưu, không sửa — nhưng đọc data đã lưu bởi F1/F2 nên nằm trong vùng regression |
| F4 | `HandelCrossAnalysisScreen`, `HandelCrossAnalysis` | `app/Console/Commands/` | Indirect | Không sửa — job nền đọc cross analysis đã lưu |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `cross_analysis.line_ids_parent` | UPDATE (lưu `[]` từ lần lưu sau) | Không được sử dụng ở đâu (xác nhận mục 3) — chỉ đổi giá trị lưu, không đổi logic đọc |
| D2 | `cross_analysis.filter_by` (gián tiếp — không update code path mới, nhưng là root cause) | không CREATE/UPDATE mới bởi fix | Cross analysis đã bị hỏng **trước khi fix** (filter_by bị ghi đè sai) **không tự phục hồi** → khách hàng cần chọn lại tiêu chí phân tích |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Cross analysis: tạo mới | F1, F2 | High |
| T2 | Cross analysis: chỉnh sửa / lưu | F1, F2, D1 | High |
| T3 | Cross analysis: phân tích lại (re-run) | F3 | Medium |
| T4 | Copy cross analysis | F3 (`copyCross()`) | Medium |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
