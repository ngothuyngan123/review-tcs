# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Thanh Duy Nguyen` |
| Commit / Pull Request | `01c6631` |
| Branch | `m_202609_form_googlesheet_change_title_40604` |
| Ngày submit đánh giá | `2026-09-15` (Journal #136470) |
| Auto-filled | `2026-09-15 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

- Vòng lặp ghi lại câu trả lời cũ (`HandleFormAnswerSyncGoogleSheetTask.java:767`) map đáp án vào cột bằng so chuỗi `item.getName()` == title của `form_detail` hiện tại. Khi title bị đổi (cột K 参加希望日時), data câu trả lời cũ vẫn lưu title cũ nên không match được header → ô để trống. Chỉ xảy ra ở nhánh sync lại từ đầu (sheet rỗng / chưa có cột 回答ID), nên KH tạo lại sheet vẫn thấy trống.
- `parseValueCell` (`:1052`) cũng tra settings của câu hỏi `select*` theo cặp `name + title` nên sau khi đổi title không tìm được cấu hình map value → label.

## 2. Cách fix

- Header mỗi cột nay mang kèm `form_detail_id` (`getArrayTitle` đổi return `List<String>` → `List<TitleColumn>`), map câu trả lời theo `form_detail_id` trước, không có thì fallback so title như logic cũ. `parseValueCell` cũng tra `form_detail` theo id trước rồi mới fallback `name + title`.
- `DataFormAnswerResult` thêm field `form_detail_id` + `getFormDetailIdCustom()` (trả `null` khi data cũ không có field hoặc không parse được số) → data cũ tự đi nhánh fallback theo title, không đổi hành vi.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `HandleFormAnswerSyncGoogleSheetTask.getArrayTitle` | Đổi return type `List<String>` → `List<TitleColumn>` | Chỉ có **1 caller tại `:721`** — đã update |
| 2 | `TitleColumn`, `getArrayHeaderTitle`, `getTitleRow`, `findItemByFormDetailId`, `findItemByTitle` | Thêm mới (private trong cùng class) | Không có caller ngoài |
| 3 | `HandleFormAnswerSyncGoogleSheetTask.parseValueCell` | Giữ nguyên signature (2 caller: `:1045`, `:1210`) | Không phá caller |
| 4 | `DataFormAnswerResult` | Thêm field `form_detail_id` + getter/setter + `toString` | Grep toàn `src/main/java` chỉ dùng ở 1 file là `HandleFormAnswerSyncGoogleSheetTask` |
| 5 | `RetryErrorGoogleSheetTask` | Không sửa | Chỉ reset trạng thái record để đẩy về task chính → không ảnh hưởng caller ngoài, scope local |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `handle` | `HandleFormAnswerSyncGoogleSheetTask` | Direct | Entry point của job sync form answer lên Google Sheet |
| F2 | `getArrayTitle` (+ mới: `getArrayHeaderTitle`, `getTitleRow`, `findItemByFormDetailId`, `findItemByTitle`, inner class `TitleColumn`) | `HandleFormAnswerSyncGoogleSheetTask` | Direct | Đổi return type; sinh header kèm `form_detail_id` |
| F3 | `parseValueCell` | `HandleFormAnswerSyncGoogleSheetTask` | Direct | Tra `form_detail` theo id trước, fallback `name + title` (ảnh hưởng câu hỏi `select*`) |
| F4 | `getFormDetailIdCustom` (thêm field `form_detail_id` + getter/setter + `toString`) | `DataFormAnswerResult` | Direct | Trả `null` khi data cũ không có field hoặc không parse được số |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | *(Không có)* | — | `form_detail_id` chỉ thêm vào `DataFormAnswerResult` — class parse JSON bằng Gson, **không phải entity JPA**; không có SQL / migration / DDL / config / constant nào đổi |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Sync form answer lên Google Sheet — **nhánh sync lại từ đầu** (sheet rỗng / chưa có cột 回答ID): đổi title 1 câu hỏi rồi cho sync lại, check cột đó ở các câu trả lời cũ ra data, không còn trống | F1, F2, F4 | High |
| T2 | **Nhánh append dòng mới** (sheet đã có data): fix không đụng logic map cột ở nhánh này, test regression trả lời form mới → dòng append vẫn đúng cột, không lệch thứ tự | F1, F2 | Medium |
| T3 | Câu hỏi **select / radio / checkbox / dropdown**: sau khi đổi title, check cell vẫn ra đúng label (không ra raw value hay rỗng), test cả 2 nhánh trên | F3 | High |
| T4 | **Câu trả lời cũ không có `form_detail_id` trong data**: check vẫn map được theo title như cũ, không mất data; form có **2 câu hỏi trùng title** thì không ghi đè lẫn nhau | F4, F2 | High |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
