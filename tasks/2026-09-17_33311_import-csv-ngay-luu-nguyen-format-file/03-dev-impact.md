# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Thanh Duy Nguyen (assignee Redmine) — báo cáo ghi "AI tạo tự động" |
| Commit / Pull Request | commit `044f472f2668555796cc15a3c56ee19d7dcee2ff` |
| Branch | `m_202608_import-csv-date-format_33311` (base branch `release-t07-2026`) |
| Ngày submit đánh giá | 2026-08-21 (Journal #132130) |
| Auto-filled | `2026-09-17 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

- Job `HandleImportCsvTask` lưu nguyên chuỗi ngày trong file CSV xuống DB: nhánh friend info kiểu lịch (`typeData=3`) mới chỉ có `LOGGER.debug` placeholder, chưa port đoạn `Carbon::parse()->format('Y-m-d')` của bản PHP nên value dạng `yyyy/MM/dd`, `yyyy/M/d` giữ nguyên, MH chat 11 không đọc được date picker và báo sai format khi click ra ngoài.
- `csvValidate` chỉ check `line_id`, không validate ngày; `LocalDate.parse` mặc định `ResolverStyle.SMART` nên `2025-02-29` bị nắn về `2025-02-28`, còn `2025-13-01` / `2025-00-10` lọt xuống DB và hiển thị `Invalid date`.

## 2. Cách fix

- Thêm `DateTimeUtils.normalizeDateCsvImport()`: parse 4 định dạng cho phép (`yyyy-MM-dd`, `yyyy/MM/dd`, `yyyy-M-d`, `yyyy/M/d`) bằng pattern `uuuu` + `ResolverStyle.STRICT` rồi trả về `yyyy-MM-dd`, ngày không tồn tại trả `null`.
- `HandleImportCsvTask`: dựng danh sách cột ngày (birthday + friend info `typeData=3`) theo header, `csvValidate` chặn row có ngày sai/không tồn tại (row không được import, message lỗi ghi vào `csv_filter_upload_history.message_error` tối đa 50 row), và chuẩn hoá value về `yyyy-MM-dd` trước khi ghi `line_user.birthday` / `friend_info_value.value`.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `HandleImportCsvTask.csvValidate` | Đổi signature (thêm tham số `dateColumns`) | Chỉ 1 caller trong cùng class là `readFileCSVV2`, đã update |
| 2 | `HandleImportCsvTask.readFileCSVV2` | Giữ nguyên signature (update lời gọi `csvValidate`) | Caller duy nhất là `startImport` |
| 3 | `DateTimeUtils.normalizeDateCsvImport` | Hàm mới | Không đụng hàm cũ |
| 4 | `BotLineUserModel.parseBirthDay` | Giữ nguyên, chỉ bỏ dùng ở nhánh import CSV | Các flow landing/liff không đổi |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

> Dev chỉ liệt kê tên function, **không ghi file path và không ghi Direct/Indirect**. Cột "Mức độ ảnh hưởng" dưới đây suy từ mục 2 + 3 của Dev (function có sửa code = Direct).

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `DateTimeUtils.normalizeDateCsvImport` (mới) | `DateTimeUtils` — Dev không ghi path | Direct | Parse 4 định dạng + STRICT, ngày không tồn tại trả `null` |
| F2 | `HandleImportCsvTask.buildDateColumns` (mới) | `HandleImportCsvTask` — Dev không ghi path | Direct | Dựng danh sách cột ngày (birthday + friend info `typeData=3`) theo header |
| F3 | `HandleImportCsvTask.csvValidate` | `HandleImportCsvTask` | Direct | Đổi signature, thêm chặn row có ngày sai/không tồn tại |
| F4 | `HandleImportCsvTask.readFileCSVV2` | `HandleImportCsvTask` | Direct | Caller của `csvValidate`; caller duy nhất của nó là `startImport` |
| F5 | `HandleImportCsvTask.readDataCSVV1` | `HandleImportCsvTask` | Direct | Chuẩn hoá value trước khi ghi DB (theo mục 2) |

### 4.2. List data bị update khi fix bug

> Dev: **Không có thay đổi schema/config**; chỉ đổi giá trị ghi vào các field dưới đây.

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `line_user.birthday` | UPDATE | Luôn `yyyy-MM-dd` |
| D2 | `friend_info_value.value` | UPDATE | Luôn `yyyy-MM-dd` (friend info kiểu lịch) |
| D3 | `csv_filter_upload_history.message_error` | UPDATE | Nay có nội dung khi row bị loại (tối đa 50 row) |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

> Dev **không ghi mức High/Medium/Low**; cột "Nguy cơ regression" giữ nguyên hướng test Dev ghi.

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Import CSV friend | F1, F2, F5, D1, D2 | Dev không ghi mức — test file có cột 生年月日 và 友だち情報 kiểu lịch ở cả 4 định dạng, DB phải ra `yyyy-MM-dd` |
| T2 | Import CSV với ngày không tồn tại (`2025-02-29`, `2025-13-01`, `2025-00-10`) | F1, F3, F4, D3 | Dev không ghi mức — row bị bỏ qua, không lưu DB, `message_error` hiện lỗi của đúng row đó |
| T3 | MH chat 11 friend info date | D2 | Dev không ghi mức — click vào date phải hiện đúng ngày trên date picker, click ra ngoài không báo sai format |
| T4 | Action theo ngày (`EventModel.csvSettingActionFriendInfoDate`) và `friend_info_history` | F5, D2 | Dev không ghi mức — check `event_step_time` / history ghi theo value đã chuẩn hoá |
| T5 | Import CSV cột trống | F1, F5, D1, D2 | Dev không ghi mức — để trống ngày vẫn phải xoá value như cũ, không bị coi là lỗi |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
