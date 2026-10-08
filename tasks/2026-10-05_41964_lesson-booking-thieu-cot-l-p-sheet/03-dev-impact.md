# 03 — Đánh giá ảnh hưởng từ Dev

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-id>` → Claude fetch issue qua Redmine REST API (`scripts/redmine_fetch.py`) rồi parse section "Đánh giá ảnh hưởng", fill các mục bên dưới. Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — Dev paste nguyên văn đánh giá theo format 4 mục.
>
> **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Thanh Duy Nguyen (tác giả Journal #139997 — đánh giá ảnh hưởng; Redmine `assigned_to` để trống) |
| Commit / Pull Request | `115a02a87fb889949c19c290e914b56880daa966` |
| Branch | `m_202609_sync_google_sheet_lesson_40194_40904` |
| Ngày submit đánh giá | 2026-10-05 (Journal #139997) |
| Auto-filled | 2026-10-05 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

- Booking tạo từ màn quản trị lưu `calendar_course_bookings.friend_info` dạng JSON **object** `{"0":{...},"2":{...}}` (PHP `json_encode` ra object khi key array khuyết do câu hỏi ẩn/tắt bị bỏ key), còn booking qua link form lưu dạng **array** nên không bị.
- Job java đọc bằng `JsonParser.fromStringToArray` chỉ nhận JSON array nên parse lỗi trả list rỗng ⇒ dòng lên sheet trống từ cột L.

## 2. Cách fix

- Thêm `JsonParser.fromStringToArrayOrObject()` đọc được cả 2 dạng array và object, giữ thứ tự xuất hiện trong JSON đúng bằng thứ tự `foreach` của PHP.
- `parseFriendInfo` dùng hàm mới, log kèm `bookingId` khi có dữ liệu nhưng không đọc được dòng nào (bỏ qua `[]` / `{}` / `null` để không báo động giả).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Dev để trống mục này trong Journal #139997 (chỉ ghi dấu "-"). Input thiếu — chưa có list caller đã check tường minh. -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | *(Dev không ghi — Input thiếu)* | | |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `JsonParser.fromStringToArrayOrObject` (mới) | linect-service (Java) | Direct | Hàm mới, đọc cả array + object |
| F2 | `HandleCalendarSyncGoogleSheetTask.parseFriendInfo` | linect-service (Java) | Direct | Đổi sang dùng F1 |
| F3 | `HandleCalendarSyncGoogleSheetTask.mappingFriendInfo` | linect-service (Java) | Direct | |
| F4 | `HandleCalendarSyncGoogleSheetTask.handleInsert` / `rebuildWholeSheet` / `handleUpdate` | linect-service (Java) | Indirect (call site) | type_sync 1 (insert), 4 (update), rebuildWholeSheet (sheet rỗng / tab bị xoá) |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | Không có thay đổi DB / config / constant do fix | — | Dev xác nhận không đổi schema |
| D2 | **Ghi bù dữ liệu đã mất**: enqueue `calendar_sync_googles` type_sync = 4 cho các booking có `friend_info` bắt đầu bằng ký tự `{` | CREATE (hàng đợi) | Để ghi lại cột L trở đi cho booking cũ bị thiếu — cần Dev/leader chốt script trước khi chạy trên production (xem note TC Studio NEW-5) |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Đặt lịch lesson từ màn quản trị: thêm booking với form có câu hỏi ẩn/tắt ở giữa, check cột L trở đi trên sheet đã có giá trị | F1, F2, F3, F4 | High (đây là bug chính) |
| T2 | Đặt lịch lesson qua link form: check vẫn ghi đủ như trước, không regression | F2, F3 | Medium |
| T3 | Cập nhật friend info của booking (type_sync = 4): đổi câu trả lời rồi check ô L..N được ghi, log không còn dòng friend_info empty | F3, F4, D2 | Medium |
| T4 | Dựng lại sheet khi sheet rỗng hoặc tab 「シート1」 bị xoá: check header và cột friend info của mọi dòng không bị mất | F4 | High |
| T5 | Sync google sheet của form answer: không đụng tới `fromStringToArray` nên chỉ cần smoke test 1 form | — (Dev khẳng định không đổi) | Low |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót) — ⚠️ **Dev để trống mục này, cần hỏi lại**
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
