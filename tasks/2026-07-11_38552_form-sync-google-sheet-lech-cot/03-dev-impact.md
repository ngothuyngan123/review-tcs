# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Thanh Phương` (người submit report ảnh hưởng) — assigned_to trên Redmine: `Kieu Son Tung` |
| Commit / Pull Request | `14ce35a952412dbcb1887a26f16dd5513bc07510` |
| Branch | `m_202607_form_google_sheet_lechcot_38552` |
| Ngày submit đánh giá | `2026-07-10` |
| Auto-filled | `2026-07-11 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

> Nguyên văn từ Redmine (journal Thanh Phương, 2026-07-10):

- Khi insert bản ghi trả lời mới vào sheet đã có dữ liệu, `appendRowData` gọi Google Sheets API `values.append` với range chỉ là tên sheet (`rangeDefine = null`). Google tự dò "table" và tự quyết cột bắt đầu ghi, nên trên sheet bị lệch cột (cột A không có dữ liệu do KH sửa) thì dòng mới ghi lệch sang phải, làm câu trả lời hiển thị sai/thiếu (13 câu nhưng chỉ thấy 4).

## 2. Cách fix

> Nguyên văn từ Redmine:

- Truyền `rangeDefine = "A1"` cho lần append ở case sheet không rỗng (dòng 429) để neo append vào cột A, luôn ghi bắt đầu từ cột A.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

> Nguyên văn từ Redmine:
>
> - Không đổi signature `appendRowData`, chỉ đổi giá trị tham số `rangeDefine` tại 1 call site. `appendRowData` có 2 chỗ gọi trong `HandleFormAnswerSyncGoogleSheetTask.handle()` (case sheet rỗng dòng 389 đã `"A1"` từ trước, case sheet không rỗng dòng 429 vừa sửa), scope cục bộ, không ảnh hưởng caller khác.

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `HandleFormAnswerSyncGoogleSheetTask.handle()` — call `appendRowData` **dòng 429** (case sheet KHÔNG rỗng) | `rangeDefine`: `null` → `"A1"` | Neo append vào cột A, tránh Google tự dò table và ghi lệch cột |
| 2 | `HandleFormAnswerSyncGoogleSheetTask.handle()` — call `appendRowData` **dòng 389** (case sheet rỗng) | Không đổi — đã truyền `"A1"` từ trước | Đối chiếu để đồng nhất behavior 2 nhánh |
| 3 | `appendRowData` (signature) | Không đổi | Chỉ đổi giá trị tham số truyền vào tại 1 call site → không ảnh hưởng caller khác |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `HandleFormAnswerSyncGoogleSheetTask.handle()` — nhánh append bản ghi mới vào sheet **không rỗng** (call `appendRowData` dòng 429) | `HandleFormAnswerSyncGoogleSheetTask` (job sync Java) | Direct | Chỗ duy nhất bị sửa: `rangeDefine = "A1"` |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| — | Không có | — | Dev ghi rõ: **không đụng SQL / config / schema / constant** |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Đồng bộ câu trả lời form lên Google Sheet (`form_answer` sync) — cụ thể case **insert bản ghi mới vào sheet đã có dữ liệu** | F1 | `<Dev không ghi mức risk>` |

**Test note của Dev (nguyên văn):** submit 1 câu trả lời mới cho form có sheet đã có sẵn dòng, verify dòng mới ghi bắt đầu từ cột A, không lệch cột, hiển thị đủ các câu trả lời. Kiểm tra cả **form 1 trang (シート1)** và **form nhiều trang (form_type = 2)**.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

<!-- Source: auto-filled từ Redmine #38552, journal id 125573 (Thanh Phương, 2026-07-10) section "** Report ảnh hưởng dev". Mục 5 (Commit/Branch) của Dev đã map vào bảng "Thông tin" phía trên. -->
