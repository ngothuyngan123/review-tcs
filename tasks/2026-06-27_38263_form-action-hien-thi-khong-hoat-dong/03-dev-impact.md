# 03 — Đánh giá ảnh hưởng từ Dev

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-url>` → Claude parse section "Đánh giá ảnh hưởng" trong Redmine, fill các mục bên dưới. Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — Dev paste nguyên văn đánh giá theo format 4 mục.
>
> **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI Auto-fixbug LME` (journal "AI LME Fix bug") |
| Commit / Pull Request | `commit c782c2a7af` (1 file) — `<chưa có link PR>` |
| Branch | `ai_fixbug_38263` (repo sns-line, gốc `release_step_20260623`) |
| Ngày submit đánh giá | `2026-06-27` |
| Auto-filled | `2026-06-27 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- Dev mô tả root cause. Càng cụ thể càng tốt: file nào, function nào, logic sai ở đâu. -->

Action gắn vào sự kiện mở/hiển thị form (loại "chỉ chạy lần đầu" — là loại mặc định) không bao giờ kích hoạt. Bản cập nhật ngày 08/05/2026 (thêm tính năng multi-capture) đã nạp lại record "lượt mở form" vừa tạo NGAY TRƯỚC khi kiểm tra điều kiện "đây có phải lần đầu mở không", khiến điều kiện luôn sai → action không bao giờ được gửi khi khách mở form.

(Bằng chứng: git blame xác nhận regression do commit `2f61dfd316` ngày 08/05/2026 gán lại `$userClick` trước khi check `empty()`.)

## 2. Cách fix

<!-- Dev mô tả cách fix. Nếu có snippet code thì càng tốt. -->

Lưu lại cờ 'lần đầu mở form' (`isFirstOpenForm`) TRƯỚC khi tạo/nạp lại record lượt mở, rồi dùng cờ này cho nhánh action loại 'chỉ lần đầu' thay vì kiểm tra biến đã bị ghi đè. Khôi phục việc gửi action khi khách mở form lần đầu. Chỉ sửa 1 file, không ảnh hưởng nhánh action loại 'mọi lần'.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Dev liệt kê các nơi đã được check & update khi fix bug (caller functions, data dependencies). -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `userOpenFormanswer` — `app/Http/Controllers/Basic/FormAnswerController.php` | Tách cờ `isFirstOpenForm` trước khi nạp lại record; nhánh 'mọi lần' (else) không đổi | Xử lý khi khách mở form, gửi `action_open_id` |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Mọi function Dev đã sửa HOẶC có thể bị ảnh hưởng gián tiếp. -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `userOpenFormanswer` | `app/Http/Controllers/Basic/FormAnswerController.php` | Direct | Xử lý khi khách mở form, gửi `action_open_id`. File DUY NHẤT bị sửa. |

### 4.2. List data bị update khi fix bug

<!-- Mọi bảng DB, field, cache, config, migration,... bị chạm tới. -->

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | (Không có) | — | Dev xác nhận chỉ sửa luồng điều kiện, KHÔNG đổi cấu trúc/dữ liệu bảng `user_open_formanswer`. Không cần recover data. |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

<!-- Dev suy ra từ 4.1 và 4.2: tính năng end-user nào có nguy cơ regression. -->

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Form Builder (FA-011) — action kích hoạt khi khách mở/hiển thị form lần đầu (`action_open_type` loại 'chỉ lần đầu') | F1 | High — đây là behavior được khôi phục |
| T2 | Form Builder — action loại 'mọi lần' (else branch) | F1 | Low — Dev xác nhận nhánh else không đổi, cần regression |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

---

<!-- Tự review AI (journal #38263): Fix tối thiểu đúng root cause: tách cờ lần-đầu khỏi biến bị reassign. Nhánh 'mọi lần' (else) không đổi. $userClick->id vẫn hợp lệ vì luôn được set trước khi dùng. Rủi ro khi test: nếu một form đang dựa vào hành vi 'không chạy action lần đầu' (do bug) thì sau fix action sẽ chạy đúng như cấu hình — đây là hành vi mong muốn. Mức verify: lint (php -l: No syntax errors). -->
